from glob import glob
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Dragline',
      version='0.8',
      description='Spider framework',
      author='Ashwin Rajeev, Shimil Rahman',
      author_email='ashwin@inzyte.com, shimil@inzyte.com',
      maintainer='Ashwin Rajeev',
      maintainer_email='ashwin@inzyte.com',
      url='http://www.inzyte.com',
      packages=['dragline'],
      scripts=glob("scripts/*"),
      data_files=[('templates', glob("templates/*"))],
      include_package_data=True,
      install_requires=[i.strip() for i in open('requirements.txt').xreadlines()],
      test_suite='tests'
      )
