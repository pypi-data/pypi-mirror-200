from distutils.core import setup
from setuptools import find_packages
import os

setup(
    name='cvbot',
    package=find_packages(','),
    version='2.4.0',
    license='LICENSE',
    description='An Assistant to help and make computer vision tasks easier',
    author='Hisham Moe',
    install_requires=[
        'opencv-python',
        'numpy',
        'mss',
        'pynput',
        'pywin32',
        'easyocr',
        'thefuzz[speedup]'
        ]
    )
