from scipy.sparse import csc_matrix
import numpy as np
import scipy
import sys
import os

TYPES = [
    scipy.sparse.csc.csc_matrix,
    scipy.sparse.csr.csr_matrix
]
NPZ_EXT = ".edit.npz"

def name_npz(path):
    """ Concat NPZ_EXT to a filenmae
    
    Arguments
    ----------
    path: str
        The path to a whole datasource volume

    Returns
    --------
    str
       The filename for all edits  

    """
    return path.rstrip(os.sep)+NPZ_EXT
    
def count_bytes(v):
    """ Count bytes in sparse matrix
    
    Arguments
    ----------
    v: csc_matrix|csr_matrix

    Returns
    ---------
    int
        Number of bytes in v
    """
    d_bytes = v.data.nbytes + v.indices.nbytes + v.indices.nbytes 
    p_bytes = sys.getsizeof(v)
    return d_bytes + p_bytes

#######
# Input and Generation
#######
def sparse_1d(data, rows):
    """ Make a 1D sparse vector of max length

    Arguments
    ----------
    data : np.ndarray
        values for each row given
    rows : np.ndarray
        all rows with a given value

    Returns
    --------
    csc_matrix
        Vector of all 64-bit unsigned ints
    """
    T_SHAPE = (sys.maxsize, 1)
    T_SHAPE = (2**30, 1)
    sparse = (data, rows, [0, len(rows)])
    out_vec = csc_matrix(sparse, T_SHAPE, dtype=np.int64)
    out_vec.sort_indices()
    return out_vec

def load(path):
    """ Read all sparse matrices in edits file

    Arguments
    -----------
    path: str
        The path to a whole datasource volume

    Returns
    ---------
    csc_matrix
        The current merges
    """
    npz_path = name_npz(path)
    if not os.path.exists(npz_path):
        merges = sparse_1d([],[])
        return (merges,)
    with np.load(npz_path) as d:
        merges = sparse_1d(d['merge'], d['rows'])
        return (merges,)

def to_sparse(sv_new):
    """ Make a sparse merge table from disjoint sets

    Arguments
    ----------
    sv_new: [[str]]
        List of all merged lists of ids

    Returns
    --------
    csc_matrix
        The new merges
    """
    data = [int(m[0]) for m in sv_new for _ in m]
    rows = [int(i) for m in sv_new for i in m]
    # Make new sparse merge table
    return sparse_1d(data, rows)

#######
# Update and output
#######
def update(t_now, t_new):
    """ Write to one sparse matrix from another

    Arguments
    ----------
    t_now: csc_matrix
        The matrix to write
    t_new: csc_matrix
        The matrix to read 
    """
    # Write each new value to current key
    for k,v in zip(t_new.indices, t_new.data):
        # All merged to k now merge to v
        t_now.data[t_now.data == k] = t_now[v,0]
        # Merge k to v
        t_now[k] = t_now[v]
    t_now.sort_indices()

def safe_makedirs(path):
    """ Make a directory if doesn't exist

    Arguments
    ----------
    path: str
    """
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def save(path, mt_now):
    """ Save the current edits to a file

    Arguments
    ----------
    path: str
    mt_now: csc_matrix
        Contains all current merges
    """
    npz_path = name_npz(path)
    keywords = {
        'merge': mt_now.data,
        'rows': mt_now.indices,
    }
    try: 
        path_error = safe_makedirs(path)
        np.savez(npz_path, **keywords)
    except OSError as e:
        return str(e)
    return ''

def from_sparse(mt_now):
    """ Make disjoint sets from a sparse merge table 

    Arguments
    ----------
    mt_now: csc_matrix
        All merges in 1D sparse array

    Returns
    --------
    [[str]]
        List of all merged lists of ids
    """
    merge_dict = {}
    # All entries in sparse array
    for k,v in zip(mt_now.indices, mt_now.data):
        # Add to the merge list or an empty list
        v_list = merge_dict.get(v, [])
        v_list.append(str(k))
        # Add new list to dictionary
        merge_dict[v] = v_list

    # Return all lists of values
    return merge_dict.values()
