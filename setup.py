from setuptools import setup, find_packages

setup(
    name='eks',
    version='0.1.1',
    packages=find_packages(".", exclude=["*.tests", "*.tests.*", "tests.*", "tests", "demo.*"]),
    package_dir = {'':'src'},
    url='https://github.com/olisim/eks',
    license='MIT',
    author='Oliver Simon',
    author_email='simon@dajool.com',
    maintainer='Jochen Breuer',
    maintainer_email='breuer@dajool.com',
    install_requires=[],
    description='A Python library to communicate with an Euchner Electronic-Key-System (EKS).',
    keywords='eks Euchner Electronic Key System keysystem',
    platforms='any',
)
