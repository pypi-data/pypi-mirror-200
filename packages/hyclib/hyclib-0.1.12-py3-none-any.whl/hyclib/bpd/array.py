import collections
import functools
import numbers

import torch
import numpy as np
import numpy.ma as ma

from ..np import isconst
from .. import pt

def unpack_args(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        args = [arg.data if isinstance(arg, Array) else arg for arg in args]
        kwargs = {k: v.data if isinstance(v, Array) else v for k, v in kwargs.items()}
        return f(self, *args, **kwargs)
    return wrapper

def concat(arrs, dim=0):
    if len(arrs) == 0:
        raise ValueError(f"arrs must be at least length 1, but {len(arrs)=}.")

    is_tensor = [Array(arr).is_tensor for arr in arrs]
    if not isconst(is_tensor):
        raise TypeError(f"Underlying data of arrs must either all be torch.Tensor or all be np.ndarray, but {is_tensor=}.")

    is_tensor = is_tensor[0]
    arrs = [arr.data for arr in arrs]
    return Array(torch.cat(arrs, dim=dim)) if is_tensor else Array(np.concatenate(arrs, axis=dim))

class Array:
    def __init__(self, data):
        """
        A simple wrapper class that provides some unified operators for np.ndarray and torch.Tensor.
        This class is NOT meant to be used externally.
        Data is NOT copied upon construction (a shallow copy will be constructed if input is a list of objects)
        """
        writeable = True
        if isinstance(data, Array):
            _data, writeable = data.data, data.writeable
        elif isinstance(data, np.ndarray):
            _data, writeable = data, data.flags.writeable
        elif isinstance(data, torch.Tensor):
            _data = data
        elif (isinstance(data, collections.abc.Iterable) and isinstance(data, collections.abc.Sized)) and not isinstance(data, str):
            if all(isinstance(x, numbers.Number) for x in data):
                _data = np.array(data)
            else:
                _data = np.empty((len(data),), dtype=object)
                for i, data_i in enumerate(data):
                    _data[i] = data_i
        else:
            _data = np.array(data)

        self._data = _data
        self._is_tensor = isinstance(_data, torch.Tensor)
        self._device = _data.device if self.is_tensor else torch.device('cpu')
        self._is_masked_array = isinstance(_data, ma.MaskedArray)
        self._writeable = writeable
        
    @property
    def writeable(self):
        return self._writeable
    
    @writeable.setter
    def writeable(self, value):
        # Note: setting writeable to True is probably not a good idea, you probably want to create a copy instead.
        if not self._is_tensor:
            self._data.setflags(write=value)
        self._writeable = value
    
    @classmethod
    def empty(cls, shape, masked=True, is_tensor=False, dtype=None, device=None):
        if not is_tensor:
            if not (device is None or device.type == 'cpu'):
                raise ValueError(f"device must be None or 'cpu' when is_tensor is False, but {device=}")
                
            arr = np.full(shape, np.nan, dtype=dtype)
            
            if masked:
                return cls(ma.array(arr, mask=True, dtype=dtype))
            return cls(arr)
        
        # TODO: return MaskedTensor if masked=True
        return cls(torch.full(shape, torch.nan, device=device))
        
    @property
    def data(self):
        return self._data
    
    @property
    def is_tensor(self):
        return self._is_tensor
    
    @property
    def is_masked_array(self):
        return self._is_masked_array
    
    @property
    def ndim(self):
        return self._data.ndim
    
    @property
    def shape(self):
        return self._data.shape
    
    @property
    def dtype(self):
        return self._data.dtype
    
    @property
    def nbytes(self):
        if self.is_tensor:
            return self.data.storage().nbytes()
        else:
            data = self.data
            while data.base is not None:
                data = data.base
            return data.nbytes
    
    @property
    def device(self):
        return self._device
    
    def __repr__(self):
        return f"Array({repr(self.data)})"
    
    def __str__(self):
        return f"Array({str(self.data)})"
    
    def __len__(self):
        return len(self.data)
    
    @unpack_args
    def __getitem__(self, key):
        if isinstance(key, torch.Tensor) and key.device != self.device:
            key = key.to(self.device)
        # key = Array(key).like(self, dtype=False) # convert to same object type as self.data and move to device if necessary
        arr = Array(self.data[key])
        if self.is_tensor and arr.data.storage().data_ptr() == self.data.storage().data_ptr():
            arr.writeable = self.writeable # same writeable flag since memory is shared
        return arr
    
    @unpack_args
    def __setitem__(self, key, value):
        if isinstance(key, torch.Tensor) and key.device != self.device:
            key = key.to(self.device)
        # key = Array(key).like(self, dtype=False) # convert to same object type as self.data and move to device if necessary
        if not self.writeable:
            raise ValueError("cannot call self.__setitem__ since self.writeable is set to False. Please copy Array first.")
        if self.is_tensor and isinstance(value, torch.Tensor):
            value = value.type(self.dtype) # pytorch bug on mps: tensor assignment is incorrect when value dtype is not the same as data dtype
        self.data[key] = value
        
    def __iter__(self):
        yield from self.data
        
    @unpack_args
    def __add__(self, other):
        return Array(self.data + other)
    
    @unpack_args
    def __sub__(self, other):
        return Array(self.data - other)
    
    @unpack_args
    def __mul__(self, other):
        return Array(self.data * other)
        
    @unpack_args
    def __truediv__(self, other):
        return Array(self.data / other)
    
    @unpack_args
    def __pow__(self, other):
        return Array(self.data ** other)
    
    @unpack_args
    def __radd__(self, other):
        return Array(other + self.data)
    
    @unpack_args
    def __rsub__(self, other):
        return Array(other - self.data)
    
    @unpack_args
    def __rmul__(self, other):
        return Array(other * self.data)
        
    @unpack_args
    def __rtruediv__(self, other):
        return Array(other / self.data)
    
    @unpack_args
    def __rpow__(self, other):
        return Array(other ** self.data)
    
    def astype(self, dtype):
        if self.is_tensor:
            arr = Array(self.data.type(dtype))
            if arr.data.storage().data_ptr() == self.data.storage().data_ptr():
                arr.writeable = self.writeable # same writeable flag since memory is shared
        else:
            arr = Array(data.astype(dtype))
        
        return arr
    
    def asnumpy(self):
        """
        Coerces underlying data to be np.ndarray. Underlying data is not copied.
        """
        if self.is_tensor:
            arr = Array(self.data.numpy())
            arr.writeable = self.writeable # same writeable flag since memory is shared (.numpy() does not copy data)
            return arr
        return self
    
    def astensor(self):
        """
        Coerces underlying data to be torch.Tensor. Underlying data is not copied.
        """
        if self.is_tensor:
            return self
        arr = Array(torch.from_numpy(self.data))
        arr.writeable = self.writeable # same writeable flag since memory is shared (from_numpy() does not copy data)
        return arr

    @unpack_args
    def like(self, other, dtype=True, device=True):
        if self.is_tensor:
            # torch -> torch
            if isinstance(other, torch.Tensor):
                arr = self
                if dtype:
                    arr = arr.astype(other.dtype)
                if device:
                    arr = arr.to(other.device)
                 
            # torch -> numpy
            else:
                if not device and self.device.type != 'cpu':
                    raise ValueError(f"device must True if converting to np.ndarray and self is not on cpu, but {device=}.")
                    
                arr = self.detach().cpu().asnumpy()
                if dtype:
                    arr = arr.astype(other.dtype)
            
        else:
            # numpy -> torch
            if isinstance(other, torch.Tensor):
                arr = self.astensor()
                if dtype:
                    arr = arr.astype(other.dtype)
                if device:
                    arr = arr.to(other.device)
               
            # numpy -> numpy
            else:
                arr = self
                if dtype:
                    arr = arr.astype(other.dtype)
                
        return arr

    def copy(self):
        return Array(self.data.clone()) if self.is_tensor else Array(self.data.copy())
    
    def detach(self):
        if self.is_tensor:
            arr = Array(self.data.detach())
            arr.writeable = self.writeable # same writeable flag since memory is shared
        else:
            arr = self
        return arr
    
    def to(self, device):
        if self.is_tensor:
            arr = Array(self.data.to(device))
            if arr.data.storage().data_ptr() == self.data.storage().data_ptr():
                arr.writeable = self.writeable # same writeable flag since memory is shared
        else:
            arr = self
        return arr
    
    def cpu(self):
        return self.to('cpu')
    
    def numpy(self):
        return self.data.numpy() if self.is_tensor else self.data
    
    def tolist(self):
        return self.data.tolist()
    
    def broadcast_to(self, shape):
        if self.is_tensor:
            arr = Array(self.data.broadcast_to(shape))
            arr.writeable = False # not writeable after broadcasting, just like numpy
        else:
            arr = Array(np.broadcast_to(self.data, shape, subok=True)) # subok=False turns ma.MaskedArray into an np.ndarray
            if arr.is_masked_array:
                mask = np.broadcast_to(self.data.mask, shape) # mask is not automatically broadcasted, so we have to do it ourselves
                arr.data.mask = mask
        return arr
    
    def isna(self):
        if self.is_tensor:
            return Array(self.data.isnan())
        else:
            if isinstance(self.data, np.floating):
                na = np.isnan(self.data)
            else:
                na = np.zeros(self.shape, dtype=bool)
            if self.is_masked_array:
                if isinstance(na, ma.MaskedArray):
                    na = na.data
                na[self.data.mask] = True
            return Array(na)
    
    def unique(self, return_inverse=False, return_counts=False, dim=None):
        if dim is not None:
            raise NotImplementedError(f"unique is not implemented for dim is not None due to ma.MaskedArray bug, but {dim=}.")
        
        if self.is_tensor:
            out = self.data.unique(return_inverse=return_inverse, return_counts=return_counts, dim=dim)
        else:
            out = np.unique(self.data, return_inverse=return_inverse, return_counts=return_counts, axis=dim)
            
        if isinstance(out, tuple):
            return [Array(out_i) for out_i in out]
        return Array(out)
    
    @unpack_args
    def bincount(self, weights=None):
        if self.is_tensor:
            # arr = Array(self.data.bincount(weights=weights))
            ### torch.bincount derivative is not implemented as of torch==1.13.1, so use my custom bincount instead. ###
            arr = Array(pt.bincount(self.data, weights=weights))
        else:
            arr = Array(np.bincount(self.data, weights=weights))
            
        return arr
    
    def argsort(self, descending=False, dim=-1):
        if self.is_tensor:
            return Array(self.data.argsort(descending=descending, dim=dim))
        else:
            arr = Array(np.argsort(self.data, axis=dim))
            if descending:
                arr = arr[::-1]
            return arr