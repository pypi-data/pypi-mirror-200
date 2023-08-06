from libc.stdint cimport uint32_t, uint64_t
import cython


# We support uint32_t and uint64_t input and output (hashes)
# without much trouble.
# However take into account that the count of functions generated and compiled
# will be the cross product of these fused types and the functions.
#
# With 2 functions (hash and hash_vec), 2 input types (uint32_t, uint64_t)
# and 2 output/hashes types (uint32_t, uint64_t) we will end up with
# 2x2x2 = 8 functions in total
ctypedef fused hash_dtype:
    uint32_t
    uint64_t

ctypedef fused key_dtype:
    uint32_t
    uint64_t

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.infer_types(True)
cdef inline hash_dtype c_hash_x(key_dtype k, hash_dtype[::1] table) nogil:
    cdef:
        hash_dtype h = 0, h0, h1, h2, h3, h4, h5, h6, h7
        key_dtype k0, k1, k2, k3, k4, k5, k6, k7

    k0 = k & 0x000000ff
    k1 = (k >> 8) & 0x000000ff
    k2 = (k >> 16) & 0x000000ff
    k3 = (k >> 24) & 0x000000ff

    # Note: table is assumed to be C-contiguous array of
    # 256 k (4 or 8) hash_dtype numbers. This is declared in the
    # function signature as 'hash_dtype[::1]'
    # With this, we can avoid the multiplication required
    # manage non-one strides (aka non-contiguous arrays)
    h0 = table[k0]
    h1 = table[k1 + 256]
    h2 = table[k2 + 256 * 2]
    h3 = table[k3 + 256 * 3]

    h = h0 ^ h1 ^ h2 ^ h3

    if key_dtype is uint64_t:
        k4 = (k >> 32) & 0x000000ff
        k5 = (k >> 40) & 0x000000ff
        k6 = (k >> 48) & 0x000000ff
        k7 = (k >> 56) & 0x000000ff

        h4 = table[k4 + 256 * 4]
        h5 = table[k5 + 256 * 5]
        h6 = table[k6 + 256 * 6]
        h7 = table[k7 + 256 * 7]

        h ^= h4 ^ h5 ^ h6 ^ h7

    return h

# Make c_hash_x callable from Python
def hash_x(key_dtype k, hash_dtype[::1] table):
    return c_hash_x(k, table)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.infer_types(True)
@cython.cdivision(True)
def hash_vec_full(key_dtype[::1] kvec, hash_dtype[::1] table, hash_dtype[::1] out):
    # Hash a vector of numbers and save the hashes into another.
    #
    # Call this if you know that the full table fits in the cache
    # In general this is OK for uint32_t/uint32_t input/hash datatypes
    #
    # If that is the case we should expect to some misses for accessing
    # table only once.
    #
    # If the table does not fully fit, there will be cache misses along
    # the way and repeatedly. Use hash_vec_batch in that case.
    cdef:
        hash_dtype hi, h
        key_dtype k, xi

        uint32_t vec_size = kvec.shape[0]
        uint32_t row, shift, rebase
        uint32_t nrows

    # Disable the GIL as this loop will not interact with the Python VM
    with nogil:
        for i in range(0, vec_size):
            k = kvec[i]

            # The C compiler should be smart enough to inline this call
            # (in the Cython definition I marked it as 'inline')
            #
            # Note: it should not be necessary but just to make it explicit
            # I'm telling Cython which specialization of c_hash_x I want to call
            h = c_hash_x[key_dtype, hash_dtype](k, table)
            out[i] = h


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.infer_types(True)
@cython.cdivision(True)
def hash_vec_batch(key_dtype[::1] kvec, hash_dtype[::1] table, hash_dtype[::1] out, uint32_t batch_len):
    cdef:
        hash_dtype hi
        key_dtype k, xi

        uint32_t batch_start = 0, batch_end = batch_len, vec_size = kvec.shape[0]
        uint32_t row, shift, rebase
        uint32_t nrows

    # This 'if' will disappear after the compilation by Cython
    # and the number of rows should be propagated (no variable at all)
    # by the C compiler
    if key_dtype is uint32_t:
        nrows = 4
    elif key_dtype is uint64_t:
        nrows = 8
    else:
        assert False

    # Calculate the position of the last "complete" batch
    # We'll handle the (possible) last incomplete batch later
    last_batch_end = vec_size - (vec_size % batch_len)

    # Disable the GIL as this loop will not interact with the Python VM
    with nogil:
        # Perform 2 rounds:
        #   - the first round will process all the complete batches
        #   - the second round will process the last incomplete batch, if any
        while (1):
            # Hash the input vector by batches.
            # The idea is that a batch of the input vector and output vector
            # will be fit in the cache next with at least 1 single full row
            # of the table.
            #
            # The inner for-loop (see below) will compute a partial hash
            # reusing the in-cache batch and in-cache row table per iteration
            #
            # On each iteration misses will occur to load the next row table
            # but it is expected to not have any miss on the input/hash batch
            #
            # Once the particular batch finishes, the while-loop iterates again
            # and processes the next batch
            #
            # Note: cython cannot handle range-loops with steps unknown in compile-time
            # See https://github.com/cython/cython/issues/1106
            while batch_start < last_batch_end:
                # Process the batch with the first row (partial hash).
                # This allows us to initialize the out vector
                for i in range(batch_start, batch_end):
                    k = kvec[i]

                    xi = (k) & 0x000000ff
                    hi = table[xi]

                    out[i] = hi

                # The C compiler should be smart enough to unroll this for loop
                # as nrows is known in compilation type and
                # it is quite small (4-1 o 8-1)
                #
                # With this for-loop we are using 1 single table row at the
                # same time per batch.
                # If a single row fits in the cache, we will have a constant
                # amount of misses.
                for row in range(1, nrows):
                    shift = row * 8
                    rebase = row * 256
                    for i in range(batch_start, batch_end):
                        k = kvec[i]

                        xi = (k >> shift) & 0x000000ff
                        hi = table[xi + rebase]

                        out[i] ^= hi

                batch_start = batch_end
                batch_end += batch_len

            # Last, probably partial batch. This even handles the case that
            # the input vector is smaller than a single
            #
            # Note: batch_start should be set to last_batch_end by now
            # so if there is another partial batch to hash, update last_batch_end
            # and batch_end too
            batch_end = batch_start + (vec_size - batch_start)
            last_batch_end = batch_end

            # If the last batch is complete it means that it was already
            # processed it in the previous iteration (first round) and
            # we can finish, otherwise do a second round
            #
            # With this trick we have 1 branch check (aka if) per batch
            # (well technically more due the for loops)
            if batch_start == batch_end:
                break
