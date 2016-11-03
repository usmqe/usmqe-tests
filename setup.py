# setup.py file for tox to be able to run unit tests


from setuptools import setup, find_packages


setup(
    name='usmqe-tests',
    license='GNU GPL v3.0',
    packages=find_packages(exclude=['doc', 'usmqe_tests', 'conf']),
    )
