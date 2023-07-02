from setuptools import setup, find_packages
from PredefinedS3 import __version__
setup(
    name="PredefinedS3",
    version= __version__,
    packages=find_packages(),
   # py_modules=['common_buckets_config'],
)