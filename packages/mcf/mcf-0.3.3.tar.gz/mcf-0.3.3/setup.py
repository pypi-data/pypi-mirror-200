from distutils.core import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = 'mcf',
  packages = ['mcf'],
  version = '0.3.3',
  license='MIT',
  description = 'mcf is a powerful package to estimate heterogeneous treatment effects for multiple treatment models in a selection-on-observables setting and learn optimal policy rules',
  author = 'mlechner',
  author_email = 'michael.lechner@unisg.ch',
  url = 'https://github.com/MCFpy/mcf',
  keywords = ['causal machine learning, heterogeneous treatment effects, causal forests, optimal policy learning'],
  long_description=read('README.txt'),
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10'
  ],
  install_requires=[
   'numpy>=1.23.5',
   'pandas>=1.5.3',
   'matplotlib>=3.7.1',
   'scipy>=1.10.1',
   'ray>=2.3.0',
   'numba>=0.56.4',
   'scikit-learn>=1.2.2',
   'psutil>=5.9.0',
   'importlib>=1.0.4',
   'sympy>=1.11.1',
   'pathlib>=1.0.1',
   'dask>=2023.3.1']
)
