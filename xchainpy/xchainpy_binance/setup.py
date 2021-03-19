from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_binance',
    packages=['xchainpy_binance'],
    version='0.1',
    license='MIT',
    description='Custom Binance client and utilities used by XChainJS clients',
    author='Thorchain',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xchainjs/xchainpy-lib',
    keywords=["BNB", "Binance", "XChainpy_binance","Thorchain"],
    install_requires=required,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python'
    ],
)
