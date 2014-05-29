try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Dragline',
      version='0.6',
      description='Spider framework',
      author='Ashwin Rajeev, Shimil Rahman',
      author_email='ashwin@quadloops.com, shimil@inzyte.com',
      url='http://www.quadloops.com',
      packages=['dragline'],
      scripts=['scripts/dragline'],
      install_requires=['gevent', 'httplib2'],
      test_suite='tests'
      )
