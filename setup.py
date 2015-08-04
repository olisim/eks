from setuptools import setup, find_packages

setup(
    name='eks',
    version='0.1',
    packages=find_packages("src", exclude=["*.tests", "*.tests.*", "tests.*", "tests", "demo.*"]),
    package_dir = {'':'src'},
    url='https://github.com/olisim/eks',
    license='MIT',
    author='Oliver Simon',
    author_email='simon@dajool.com',
    install_requires=[],
    description='...',
    platforms='any',
)
