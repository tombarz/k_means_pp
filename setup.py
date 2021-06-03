from setuptools import setup, Extension

"""
A minimalist setup is shown.
"""


setup(name='mykmeanssp',
      version='1.0',
      description='my kmeans sp for sp class',
      ext_modules=[Extension('mykmeanssp', sources=['kmeans.c'])])
