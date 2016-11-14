from pip.req import parse_requirements
from setuptools import setup, find_packages

parsed_reqs = parse_requirements('requirements.txt', session=False)
install_requires = [str(ir.req) for ir in parsed_reqs]

setup(name='Gnosis',
      version='1.0',
      description='EVE Online Formulas and Simulations',
      author='Ebag Trescientas',
      author_email='ebagola@gmail.com',
      url='https://github.com/Ebag333/Gnosis',
      packages=find_packages(exclude='tests'),
      )