import os
from setuptools import setup, find_packages

setup(
   name='kinjax',
   version='0.0.1', 
   description='This module calculates FK and Jacobian, accelerated by Jax to utilize JIT and GPU parallelization',
   author='Kanghyun Kim',
   author_email='kh11kim@kaist.ac.kr',
   packages=find_packages(),  #same as name
   install_requires=[
      "jax",
      "sympy",
      "scipy",
   ]
)

# python setup.py sdist bdist_wheel
# twine upload dist/*
