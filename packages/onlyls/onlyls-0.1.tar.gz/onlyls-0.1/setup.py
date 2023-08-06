from setuptools import setup, find_packages

setup(
    name='onlyls',
    version='0.1',
    packages=find_packages(),
    author='Aadya Chinubhai',
    author_email='aadyachinubhai@gmail.com',
    description='A package for performing OLS regression for numpy, pandas, and dask',
    install_requires=['numpy', 'pandas', 'dask', 'scipy'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
