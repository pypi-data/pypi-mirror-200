from .c_tabulationhashing import hash_x, hash_vec_full, hash_vec_batch
import numpy as np

def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance

    If seed is None, return the RandomState singleton used by np.random.
    If seed is an int, return a new RandomState instance seeded with seed.
    If seed is already a RandomState instance, return it.
    Otherwise raise ValueError.

    Note: this implementation was borrowed from sklearn
    (from sklearn/utils/validation.py) to avoid an unnecessary dependency
    with sklearn.
    See https://github.com/scikit-learn/scikit-learn/blob/9aaed4987/sklearn/utils/validation.py#L1207
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (int, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError('%r cannot be used to seed a numpy.random.RandomState'
                     ' instance' % seed)


class TabulationHashing:
    def __init__(self, input_bits, hash_bits, random_state=None, batch_len=0):
        # If the table fits in the cache next with some part of the input
        # and output vectors, use batch_len=1 (no batch) which has less
        # conditionals
        # But if the table does not fit in the cache, tweak batch_len > 1
        assert input_bits in (32, 64)
        assert hash_bits in (32, 64)
        assert batch_len >= 0

        self.input_dtype = np.uint32 if input_bits == 32 else np.uint64
        self.hash_dtype = np.uint32 if hash_bits == 32 else np.uint64

        dtype_sig = (
                ("uint32_t" if input_bits == 32 else "uint64_t"),
                ("uint32_t" if hash_bits == 32 else "uint64_t"),
                )

        # Ensure that we are going to call the correct specialized versions
        self._hash_x = hash_x[dtype_sig]
        self._hash_vec = hash_vec_full[dtype_sig] if not batch_len else hash_vec_batch[dtype_sig]

        random_state = check_random_state(random_state)

        table_size = 256 * 4
        if input_bits == 64:
            table_size *= 2

        self.table = random_state.randint(0, (2**hash_bits)-1, size=table_size, dtype=self.hash_dtype)
        self.table = np.ascontiguousarray(self.table) # just to ensure it is contiguous

        self.batch_len = batch_len

    def hash(self, x):
        ''' Compute the hash of a single x scalar '''
        return self._hash_x(x, self.table)

    def hash_vec(self, xvec, out=None):
        ''' Compute the hash of every number of xvec and save the hashes
            into out if one was provided.

            In any case, the results are returned.
            '''
        if out is None:
            out = np.empty_like(xvec, dtype=self.hash_dtype)

        # If wrong types, fail
        if xvec.dtype != self.input_dtype:
            raise

        if out.dtype != self.hash_dtype:
            raise

        # Ensure the out (dst) buffer is large enough
        if xvec.shape[0] > out.shape[0]:
            raise Exception

        # Ensure the arrays are C contiguous
        if not xvec.flags['C_CONTIGUOUS']:
            raise Exception

        if not out.flags['C_CONTIGUOUS']:
            raise Exception

        if self.batch_len:
            self._hash_vec(xvec, self.table, out, self.batch_len)
        else:
            self._hash_vec(xvec, self.table, out)
        return out

