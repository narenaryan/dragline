try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Dragline',
      version='0.2',
      description='Spider framework',
      author='Ashwin Rajeev, Shimil Rahman',
      author_email='ashwin@quadloops.com, shimil@inzyte.com',
      url='http://www.quadloops.com',
      packages=['dragline'],
      install_requires=['redisdatastucture>=0.3'],
      dependency_links=[
          "http://code.quadloops.com/inzyte/redisdatastructure.git#egg=redisdatastucture"
      ]
      )
