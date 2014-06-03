from glob import glob
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Dragline',
      version=open('dragline/VERSION').read().strip(),
      description='Spider framework',
      author='Ashwin Rajeev, Shimil Rahman',
      author_email='ashwin@inzyte.com, shimil@inzyte.com',
      url='http://www.inzyte.com',
      packages=['dragline'],
      scripts=glob("scripts/*"),
      data_files=[('templates', glob("templates/*"))],
      include_package_data=True,
      install_requires=['gevent>=1.0.0', 'httplib2>=0.9', 'redis>=2.9.0'],
      test_suite='tests',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX :: Linux',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Environment :: Console',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet :: WWW/HTTP',
      ]
      )
