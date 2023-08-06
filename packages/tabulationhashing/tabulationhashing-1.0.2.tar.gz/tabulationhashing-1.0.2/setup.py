from setuptools import setup

from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

# To generate the .c files and compile the .so libraries, run:
# python setup.py build_ext --inplace
#
# This requires cython and a compiler to be installed in the host machine
#
# TODO: how to avoid requiring cython?

setup(
    ext_modules=cythonize([
      Extension('tabulationhashing.c_tabulationhashing',
                sources=["tabulationhashing/c_tabulationhashing.pyx"],
                extra_compile_args=['-O3', '-g'],
                language='c'
                ),
      ],
      compiler_directives={'language_level' : "3"},
      annotate=True
      ),

    cmdclass = {'build_ext': build_ext}
)


