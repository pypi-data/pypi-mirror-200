import unittest
from tabulationhashing.tabulationhashing import TabulationHashing
import numpy as np

class TestTabulationHashing(unittest.TestCase):
    def test_hash_32_32(self):
        thashing = TabulationHashing(32, 32, 0)

        self.assertEqual(thashing.hash(0x0000000f), 4173605066)
        self.assertEqual(thashing.hash(0x00000f00), 1585277234)
        self.assertEqual(thashing.hash(0x000f0000), 4114509127)
        self.assertEqual(thashing.hash(0x0f000000), 3668260514)

        self.assertEqual(thashing.hash(0x00000000), 2050990014)

    def test_hash_32_64(self):
        thashing = TabulationHashing(32, 64, 0)

        self.assertEqual(thashing.hash(0x0000000f), 15073582232772869078)
        self.assertEqual(thashing.hash(0x00000f00), 2756157967122003842)
        self.assertEqual(thashing.hash(0x000f0000), 1907689711309795780)
        self.assertEqual(thashing.hash(0x0f000000), 7871975025262679071)

        self.assertEqual(thashing.hash(0x00000000), 5404617006697334381)

    def test_hash_64_32(self):
        thashing = TabulationHashing(64, 32, 0)

        self.assertEqual(thashing.hash(0x000000000000000f), 3055806466)
        self.assertEqual(thashing.hash(0x0000000000000f00), 278571514)
        self.assertEqual(thashing.hash(0x00000000000f0000), 3151605135)
        self.assertEqual(thashing.hash(0x000000000f000000), 2487416426)

        self.assertEqual(thashing.hash(0x0000000f00000000), 3428964583)
        self.assertEqual(thashing.hash(0x00000f0000000000), 200091360)
        self.assertEqual(thashing.hash(0x000f000000000000), 3088311817)
        self.assertEqual(thashing.hash(0x0f00000000000000), 2053879205)

        self.assertEqual(thashing.hash(0x0000000000000000), 886595446)

    def test_hash_64_64(self):
        thashing = TabulationHashing(64, 64, 0)

        self.assertEqual(thashing.hash(0x000000000000000f), 15910577336771117138)
        self.assertEqual(thashing.hash(0x0000000000000f00), 3153207991220833286)
        self.assertEqual(thashing.hash(0x00000000000f0000), 1694724861014231616)
        self.assertEqual(thashing.hash(0x000000000f000000), 6972550189924495259)

        self.assertEqual(thashing.hash(0x0000000f00000000), 529974843499224314)
        self.assertEqual(thashing.hash(0x00000f0000000000), 16963154343544958504)
        self.assertEqual(thashing.hash(0x000f000000000000), 405316215084986108)
        self.assertEqual(thashing.hash(0x0f00000000000000), 5666169142463988920)

        self.assertEqual(thashing.hash(0x0000000000000000), 5115148471677337065)

    def test_hash_32_32_vec_batch(self):
        thashing = TabulationHashing(32, 32, 0, batch_len=4)
        xvec = np.array([
            0x0000000f,
            0x00000f00,
            0x000f0000,
            0x0f000000,
            0x00000000,
            ], dtype=np.uint32
            )

        expected = np.array([
                4173605066,
                1585277234,
                4114509127,
                3668260514,
                2050990014,
            ], dtype=np.uint32
            )

        # len: 5 > batch_len: 4
        out = thashing.hash_vec(xvec)
        self.assertTrue((out == expected).all())

        # len: 4 = batch_len: 4
        out = thashing.hash_vec(xvec[:-1])
        self.assertTrue((out == expected[:-1]).all())

        # len: 3 < batch_len: 4
        out = thashing.hash_vec(xvec[:-2])
        self.assertTrue((out == expected[:-2]).all())

    def test_hash_64_32_vec_batch(self):
        thashing = TabulationHashing(64, 32, 0, batch_len=8)
        xvec = np.array([
            0x000000000000000f,
            0x0000000000000f00,
            0x00000000000f0000,
            0x000000000f000000,

            0x0000000f00000000,
            0x00000f0000000000,
            0x000f000000000000,
            0x0f00000000000000,

            0x0000000000000000,
            ], dtype=np.uint64
            )

        expected = np.array([
            3055806466,
            278571514,
            3151605135,
            2487416426,

            3428964583,
            200091360,
            3088311817,
            2053879205,

            886595446,
            ], dtype=np.uint32
            )

        # len: 9 > batch_len: 8
        out = thashing.hash_vec(xvec)
        self.assertTrue((out == expected).all())

        # len: 8 = batch_len: 8
        out = thashing.hash_vec(xvec[:-1])
        self.assertTrue((out == expected[:-1]).all())

        # len: 7 < batch_len: 8
        out = thashing.hash_vec(xvec[:-2])
        self.assertTrue((out == expected[:-2]).all())

    def test_hash_32_32_vec_batch_callers_out(self):
        thashing = TabulationHashing(32, 32, 0, batch_len=4)
        xvec = np.array([
            0x0000000f,
            0x00000f00,
            0x000f0000,
            0x0f000000,
            0x00000000,
            ], dtype=np.uint32
            )

        expected = np.array([
                4173605066,
                1585277234,
                4114509127,
                3668260514,
                2050990014,
            ], dtype=np.uint32
            )

        # Just a "dirty" out buffer: hash_vec should override it
        # And it should work even if the input vector is smaller
        out = np.ones_like(expected)

        # len: 5 > batch_len: 4
        out = thashing.hash_vec(xvec, out=out)
        self.assertTrue((out == expected).all())

        # len: 4 = batch_len: 4
        out = thashing.hash_vec(xvec[:-1], out=out)
        self.assertTrue((out[:-1] == expected[:-1]).all())

        # len: 3 < batch_len: 4
        out = thashing.hash_vec(xvec[:-2], out=out)
        self.assertTrue((out[:-2] == expected[:-2]).all())

    def test_hash_32_64_vec_batch_callers_out(self):
        thashing = TabulationHashing(32, 64, 0, batch_len=4)
        xvec = np.array([
            0x0000000f,
            0x00000f00,
            0x000f0000,
            0x0f000000,
            0x00000000,
            ], dtype=np.uint32
            )

        expected = np.array([
            15073582232772869078,
            2756157967122003842,
            1907689711309795780,
            7871975025262679071,

            5404617006697334381,
            ], dtype=np.uint64
            )

        # Just a "dirty" out buffer: hash_vec should override it
        # And it should work even if the input vector is smaller
        out = np.ones_like(expected)

        # len: 5 > batch_len: 4
        out = thashing.hash_vec(xvec, out=out)
        self.assertTrue((out == expected).all())

        # len: 4 = batch_len: 4
        out = thashing.hash_vec(xvec[:-1], out=out)
        self.assertTrue((out[:-1] == expected[:-1]).all())

        # len: 3 < batch_len: 4
        out = thashing.hash_vec(xvec[:-2], out=out)
        self.assertTrue((out[:-2] == expected[:-2]).all())

    def test_hash_32_32_vec_full(self):
        thashing = TabulationHashing(32, 32, 0, batch_len=1)
        xvec = np.array([
            0x0000000f,
            0x00000f00,
            0x000f0000,
            0x0f000000,
            0x00000000,
            ], dtype=np.uint32
            )

        expected = np.array([
                4173605066,
                1585277234,
                4114509127,
                3668260514,
                2050990014,
            ], dtype=np.uint32
            )

        out = thashing.hash_vec(xvec)
        self.assertTrue((out == expected).all())


    def test_hash_64_32_vec_full(self):
        thashing = TabulationHashing(64, 32, 0, batch_len=1)
        xvec = np.array([
            0x000000000000000f,
            0x0000000000000f00,
            0x00000000000f0000,
            0x000000000f000000,

            0x0000000f00000000,
            0x00000f0000000000,
            0x000f000000000000,
            0x0f00000000000000,

            0x0000000000000000,
            ], dtype=np.uint64
            )

        expected = np.array([
            3055806466,
            278571514,
            3151605135,
            2487416426,

            3428964583,
            200091360,
            3088311817,
            2053879205,

            886595446,
            ], dtype=np.uint32
            )

        out = thashing.hash_vec(xvec)
        self.assertTrue((out == expected).all())


if __name__ == '__main__':
    unittest.main()
