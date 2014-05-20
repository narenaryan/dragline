try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Dragline',
      version='0.4',
      description='Spider framework',
      author='Ashwin Rajeev, Shimil Rahman',
      author_email='ashwin@quadloops.com, shimil@inzyte.com',
      url='http://www.quadloops.com',
      packages=['dragline'],
      include_package_data=True,
      package_data={'': ['logging.conf']},
      scripts=['scripts/dragline'],
      install_requires=['gevent']
      )
