import numpy as np

from ..itertools import flatten_seq

__all__ = [
    'isconst',
    'meshgrid_dd',
    'meshgrid',
    'inv_perm',
    'unique_rows',
    'intersect_rows',
    'repeat',
]

def isconst(x, axis=None, **kwargs):
    x = np.asanyarray(x)
    
    if axis is None:
        x = x.reshape(-1)
    else:
        if isinstance(axis, int):
            axis = [axis]
        axis = sorted([d % x.ndim for d in axis])[::-1]
        for d in axis:
            x = np.moveaxis(x, d,-1)
        x = x.reshape(*x.shape[:-len(axis)],-1)
        
    if isinstance(x, np.floating):
        return np.isclose(x[...,:-1], x[...,1:], **kwargs).all(axis=-1)
    return (x[...,:-1] == x[...,1:]).all(axis=-1)

def meshgrid_dd(*arrs):
    """
    Generalized np.meshgrid
    Mesh together list of arrays of shapes (n_1_1,...,n_1_{M_1},N_1), (n_2_1,...,n_2_{M_2},N_2), ..., (n_P_1, ..., n_P_{M_P},N_P)
    Returns arrays of shapes 
    (n_1_1,...,n_1_{M_1},n_2_1,...,n_2_{M_2},...,n_P_1, ..., n_P_{M_P},N_1),
    (n_1_1,...,n_1_{M_1},n_2_1,...,n_2_{M_2},...,n_P_1, ..., n_P_{M_P},N_2),
    ...
    (n_1_1,...,n_1_{M_1},n_2_1,...,n_2_{M_2},...,n_P_1, ..., n_P_{M_P},N_P)
    
    IMPORTANT: Data is NOT copied, unlike numpy which copies by default
    """
    sizes = [list(arr.shape[:-1]) for arr in arrs] # [[n_1,...,n_{M_1}],[n_1,...,.n_{M_2}],...]
    Ms = np.array([arr.ndim - 1 for arr in arrs]) # [M_1, M_2, ...]
    M_befores = np.cumsum(np.insert(Ms[:-1],0,0))
    M_afters = np.sum(Ms) - np.cumsum(Ms)
    Ns = [arr.shape[-1] for arr in arrs]
    shapes = [[1]*M_befores[i]+sizes[i]+[1]*M_afters[i]+[Ns[i]] for i, arr in enumerate(arrs)]
    expanded_arrs = [np.broadcast_to(arr.reshape(shapes[i]), flatten_seq(sizes)+[Ns[i]]) for i, arr in enumerate(arrs)]
    return expanded_arrs

def meshgrid(*arrs, **kwargs):
    """
    Generalized np.meshgrid
    Mesh together list of arrays of shapes (n_1_1,...,n_1_{M_1}), (n_2_1,...,n_2_{M_2}), ..., (n_P_1, ..., n_P_{M_P})
    Returns arrays of shapes 
    (n_1_1,...,n_1_{M_1},n_2_1,...,n_2_{M_2},...,n_P_1, ..., n_P_{M_P}),
    (n_1_1,...,n_1_{M_1},n_2_1,...,n_2_{M_2},...,n_P_1, ..., n_P_{M_P}),
    ...
    (n_1_1,...,n_1_{M_1},n_2_1,...,n_2_{M_2},...,n_P_1, ..., n_P_{M_P})
    
    IMPORTANT: By default, indexing='ij' rather than 'xy' as in np.meshgrid. This follows the pytorch convention.
    IMPORTANT: Data is NOT copied, unlike numpy which copies by default
    """
    default_kwargs = {
        'indexing': 'ij',
    }
    kwargs = default_kwargs | kwargs
    invalid_keys = set(kwargs.keys()) - {'indexing'}
    if len(invalid_keys) > 0:
        raise TypeError(f"meshgrid() got an unexpected keyword argument '{invalid_keys.pop()}'")
    indexing = kwargs['indexing']    
        
    arrs = (arr[...,None] for arr in arrs)
    arrs = meshgrid_dd(*arrs)
    arrs = [arr.squeeze() for arr in arrs]
    
    if indexing == 'xy':
        arrs = [np.swapaxes(arr, 0, 1) for arr in arrs]
        
    return arrs

def inv_perm(p):
    """
    Code taken from: https://stackoverflow.com/questions/11649577/how-to-invert-a-permutation-array-in-numpy
    Return an array s with which np.array_equal(arr[p][s], arr) is True.
    The array_like argument p must be some permutation of 0, 1, ..., len(p)-1.
    """
    p = np.asanyarray(p) # in case p is a tuple, etc.
    s = np.empty_like(p)
    s[p] = np.arange(p.size)
    return s

def unique_rows(arr, sorted=True, return_index=False, return_inverse=False, return_counts=False):
    """
    Code modified from https://github.com/scikit-image/scikit-image/blob/main/skimage/util/unique.py
    Much faster than np.unique(arr, axis=0)
    See https://github.com/numpy/numpy/issues/11136
    Set sorted=False for maximum speed.
    In this implementation, equal_nan=True.
    
    For speed comparison:
    N, M = 100000,100
    arr = np.random.randint(M, size=(N,2)).astype(float)
    
    %timeit unique_rows(arr, sorted=False, return_index=True, return_inverse=True)
    25.9 ms ± 386 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    
    %timeit np.unique(arr, return_index=True, return_inverse=True, axis=0)
    85.8 ms ± 240 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
    """
    if arr.ndim != 2:
        raise ValueError("unique_rows() only makes sense for 2D arrays, "
                         f"got {arr.ndim}")
    # the view in the next line only works if the array is C-contiguous
    arr = np.ascontiguousarray(arr)
    # np.unique() finds identical items in a raveled array. To make it
    # see each row as a single item, we create a view of each row as a
    # byte string of length itemsize times number of columns in `ar`
    arr_row_view = arr.view(f"|S{arr.itemsize * arr.shape[1]}")
    out = np.unique(arr_row_view, return_index=True, return_inverse=return_inverse, return_counts=return_counts)
    out = list(out)
    out[0] = arr[out[1]]
    
    if sorted:
        idx = np.lexsort(out[0].T[::-1])
        out[0] = out[0][idx]
        if return_index:
            out[1] = out[1][idx]
        if return_inverse:
            out[2] = inv_perm(idx)[out[2]]
        if return_counts:
            i = 3 if return_inverse else 2
            out[i] = out[i][idx]
    
    if not return_index:
        out.pop(1)

    if len(out) == 1:
        return out[0]
    return out

def intersect_rows(larr, rarr, return_indices=False, **kwargs):
    """
    intersect1d but for 2D arrays. Uses the same trick as unique_rows.
    """
    if larr.ndim != 2 or rarr.ndim != 2:
        raise ValueError("intersect_rows() only makes sense for 2D arrays, "
                         f"got {larr.ndim=}, {rarr.ndim=}")
    if larr.shape[1] != rarr.shape[1]:
        raise ValueError(f"larr and rarr must both have same number of columns, but {larr.shape[1]=}, {rarr.shape[1]=}.")
        
    N_cols = larr.shape[1]
    larr, rarr = np.ascontiguousarray(larr), np.ascontiguousarray(rarr)
    larr_row_view, rarr_row_view = larr.view(f"|S{larr.itemsize * N_cols}"), rarr.view(f"|S{rarr.itemsize * N_cols}")
    
    out = np.intersect1d(larr_row_view, rarr_row_view, return_indices=True, **kwargs)
    out = list(out)
    out[0] = larr[out[1]]
    
    if not return_indices:
        return out[0]
    return out
    
def repeat(arr, repeats, chunks=None):
    """
    Generalized np.repeat
    Copied from @MadPhysicist's solution: https://stackoverflow.com/questions/63510977/repeat-but-in-variable-sized-chunks-in-numpy
    
    Example due to @MadPhysicist in the same link:
    arr = np.array([0, 1, 2, 10, 11, 20, 21, 22, 23])
    #               >     <  >    <  >            <
    chunks = np.array([3, 2, 4])
    repeats = np.array([1, 3, 2])
    
    print(repeat(arr, repeats, chunks=chunks))
    >>>      [0, 1, 2, 10, 11, 10, 11, 10, 11, 20, 21, 22, 23, 20, 21, 22, 23])
    # repeats:>  1  <  >         3          <  >              2             <
    """
    if chunks is None:
        return np.repeat(arr, repeats)
    
    arr, repeats, chunks = np.asanyarray(arr), np.asanyarray(repeats), np.asanyarray(chunks)
    
    if arr.ndim != 1 or repeats.ndim != 1 or chunks.ndim != 1:
        raise ValueError(f"arr, repeats, and chunks must all be 1D, but {arr.ndim=}, {repeats.ndim=} and {chunks.ndim=}.")
    if len(repeats) != len(chunks):
        raise ValueError(f"repeats and chunks must have the same length, but {len(repeats)=} and {len(chunks)=}.")
    if chunks.sum() != len(arr):
        raise ValueError(f"sum of chunks must be the length of arr, but {chunks.sum()=} and {len(arr)=}.")

    regions = chunks * repeats
    index = np.arange(regions.sum())

    segments = np.repeat(chunks, repeats)
    resets = np.cumsum(segments[:-1])
    offsets = np.zeros_like(index)
    offsets[resets] = segments[:-1]
    offsets[np.cumsum(regions[:-1])] -= chunks[:-1]

    index -= np.cumsum(offsets)

    out = arr[index]
    
    return out
