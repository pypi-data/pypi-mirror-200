# from distutils.core import setup

from setuptools import setup


def read_file():
    with open('README.rst') as f:
        LONG_DESCRIPTION = f.read()
        return LONG_DESCRIPTION


VERSION = "1.0.0"

setup(name="spidertoolKits",
      version=VERSION,
      description="The first package",
      long_description=read_file(),
      author="Karson",
      license="MIT"
      )
