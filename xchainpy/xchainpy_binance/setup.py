from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_binance',
    packages=find_packages(),
    version='0.2.1',
    license='MIT',
    description='Custom Binance client and utilities used by XChainPY clients',
    author='THORChain',
    author_email='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xchainjs/xchainpy-lib/tree/main/xchainpy/xchainpy_binance',
    keywords=["BNB", "Binance", "XChainpy_binance","THORChain"],
    install_requires=['py_binance_chain>=0.2', 'xchainpy_client>=0.1.5', 'xchainpy_crypto>=0.1.7', 'xchainpy_util>=0.1.7'],
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
