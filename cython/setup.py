from distutils.core import setup
from Cython.Build import cythonize

setup(
        name = "Hello world 3 App",
        ext_modules = cythonize("example.pyx")
        )
