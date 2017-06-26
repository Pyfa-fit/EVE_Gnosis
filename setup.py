from pip.req import parse_requirements
from setuptools import setup, find_packages

parsed_reqs = parse_requirements('requirements.txt', session=False)
install_requires = [str(ir.req) for ir in parsed_reqs]

setup(name='EVE_Gnosis',
      version='2017.06.27',  # Year.Month.Day (use post# if multiple releases in 1 day)
      description='EVE Online Formulas and Simulations',
      author='Ebag Trescientas',
      author_email='ebagola@gmail.com',
      url='https://github.com/Pyfa-fit/EVE_Gnosis',
      packages=find_packages(exclude='tests'),
      )
