from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "pysim_accelerators",
        ["src/antenna_designer/pysim_accelerators.cpp"],
        extra_compile_args=["-fopenmp", "-g", "-std=gnu++11"],
        extra_link_args=["-fopenmp", "-lpthread"],
    ),
]

setup(
    name='pysim_accelerators',
    ext_modules=ext_modules,
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
