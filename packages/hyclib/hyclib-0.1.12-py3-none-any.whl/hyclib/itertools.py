import itertools

import numpy as np

def flatten_seq(s, depth=-1, dtypes=[list, tuple]):
    """
    Recursively flattens a sequence (defined as an instance
    of one of the DTYPES) up to depth DEPTH.
    Will try to cast the result to type(s) if possible, otherwise returns a list.
    depth=0 returns the sequence unchanged, depth=-1 returns a fully flattened sequence
    TypeError is raised if s is not an instance of any of the dtypes.
    
    >>> s = [[1,2,[3]],[],(4,5),6]
    >>> flatten_seq(s, depth=1)
    [1,2,[3],4,5,6]
    >>> flatten_seq(s, depth=-1)
    [1,2,3,4,5,6]
    >>> flatten_seq(tuple(s), depth=-1)
    (1,2,3,4,5,6)
    
    """
    if not any([isinstance(s, dtype) for dtype in dtypes]):
        raise TypeError(f"The arugment to flatten_list must be one of {dtypes}, not {type(s)}")
    flattened_s = []
    for elem in s:
        if depth == 0 or not any([isinstance(elem, dtype) for dtype in dtypes]):
            flattened_s.append(elem)
        else:
            flattened_s += flatten_seq(elem, depth=depth-1, dtypes=dtypes)
    try:
        return type(s)(flattened_s)
    except Exception:
        return flattened_s
    
def flatten_dict(d, depth=-1):
    """
    Recursively flattens dict up to depth DEPTH. Keys are concatenated into a tuple key.
    depth=0 returns the dictionary unchanged, depth=-1 returns a fully flattened dictionary
    depth=n means the first n layers of the dictionary is flattened, so a depth k dict becomes a depth k-1 dict.
    TypeError is raised if d is not a dict.
    
    >>> d = {'a': {'b': {'c': 'd'}}}
    >>> flatten_dict(d, depth=1)
    {'a.b': {'c': 'd'}}
    >>> flatten_dict(d, depth=-1)
    {'a.b.c':'d'}
    
    """
    if not isinstance(d, dict):
        raise TypeError(f"The arugment to flatten_dict must be a dict, not {type(d)}")
    flattened_dict = {}
    for k, v in d.items():
        if '.' in k:
            raise ValueError("dictionary should not contain '.' in any of its keys")
        if depth == 0 or not isinstance(v, dict) or v == {}: # if depth == 0 or v is leaf
            flattened_dict[k] = v
        else:
            for new_k, new_v in flatten_dict(v, depth=depth-1).items():
                flattened_dict['.'.join([k, new_k])] = new_v
    return flattened_dict

def dict_iter(d, delimiter='.'):
    """
    Iterates over all leaf nodes of a dictionary in (key, value) pairs
    If delimiter is None, key is a tuple of the nested keys
    Otherwise, key is a string with the nested keys joined by delimiter
    """
    assert isinstance(d, dict)
    
    for k, v in d.items():
        if isinstance(v, dict):
            for ki, vi in dict_iter(v, delimiter=delimiter):
                if delimiter is None:
                    yield ((k, *ki), vi)
                else:
                    yield (delimiter.join([k, ki]), vi)
        
        else:
            if delimiter is None:
                yield ((k,), v)
            else:
                yield (k, v)
            
def dict_get(d, k, delimiter='.'):
    if delimiter is None:
        ks = k
    else:
        ks = k.split(delimiter)
        
    for ki in ks:
        d = d[ki]
    return d

# more general version of assign_dict
def dict_set(d, k, v, delimiter='.'):
    if delimiter is None:
        ks = k
    else:
        ks = k.split(delimiter)
        
    for ki in ks[:-1]:
        d = d.setdefault(ki, {})
    d[ks[-1]] = v
    
def dict_update(d, new_d):
    for k, v in dict_iter(new_d, delimiter=None): # might get very slow if new_d is very large, but I can't think of a better way
        dict_set(d, k, v, delimiter=None)
        
def dict_union(d, new_d):
    d = d.copy()
    dict_update(d, new_d)
    return d

def assign_dict(d, keys, value):
    """
    Assign (potentially nested) value to dictionary using a list/tuple of keys
    This is an in-place operation.
    
    >>> d = {}
    >>> assign_dict(d, ['a', 'b'], 'c')
    >>> d
    {'a': {'b': 'c'}}
    
    """
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value
    
def product(*ls, enum=False):
    """
    Like itertools.product, but has an enum keyword that
    returns the nd-index along with the elements. Note, however, it
    assumes that the inputs are sequences, not iterables, since len() is used.
    """
    if not enum:
        return itertools.product(*ls)
    return zip(np.ndindex(tuple(len(l) for l in ls)), itertools.product(*ls))
    
def dict_zip(*dicts, mode='strict', **kwargs):
    if mode == 'strict':
        return _dict_zip_strict(*dicts, **kwargs)
    if mode == 'intersect':
        return _dict_zip_intersection(*dicts, **kwargs)
    if mode == 'union':
        return _dict_zip_union(*dicts, **kwargs)
    raise NotImplementedError("mode must be either 'strict', 'intersect', or 'union'")
            
def _dict_zip_strict(*dicts):
    if not dicts:
        return

    n = len(dicts[0])
    if any(len(d) != n for d in dicts):
        raise ValueError('arguments must have the same length')

    for key, first_val in dicts[0].items():
        yield key, first_val, *(other[key] for other in dicts[1:])


def _dict_zip_intersection(*dicts):
    if not dicts:
        return

    keys = set(dicts[0]).intersection(*dicts[1:])
    for key in keys:
        yield key, *(d[key] for d in dicts)


def _dict_zip_union(*dicts, fillvalue=None):
    if not dicts:
        return

    keys = set(dicts[0]).union(*dicts[1:])
    for key in keys:
        yield key, *(d.get(key, fillvalue) for d in dicts)
