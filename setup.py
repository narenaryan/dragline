try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Dragline',
      version='0.7',
      description='Spider framework',
      author='Ashwin Rajeev, Shimil Rahman',
      author_email='ashwin@quadloops.com, shimil@inzyte.com',
      url='http://www.quadloops.com',
      packages=['dragline', 'dragline.templates'],
      scripts=['scripts/dragline','scripts/dragline-init','scripts/dragline-deploy'],
      install_requires=['gevent', 'httplib2','redis'],
      test_suite='tests'
      )
