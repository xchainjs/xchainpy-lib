from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_bitcoincash',
    packages=find_packages(),
    version='0.2.2',
    license='MIT',
    description='Bitcoincash Module for XChainPy Clients',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='THORChain',
    author_email='',
    url='https://github.com/xchainjs/xchainpy-lib/tree/main/xchainpy/xchainpy_bitcoincash',
    keywords=["THORChain", "XChainpy","XChainpy_bitcoincash"],
    install_requires=['mnemonic>=0.18', 'bitcash>=0.6.1', 'cashaddress_regtest>=1.1.0', 'cashaddress>=1.0.6', 'http3>=0.6.7', 'xchainpy_client>=0.1.6', 'xchainpy_crypto>=0.1.7', 'xchainpy_util>=0.1.8', 'bip_utils>=1.11.1'],
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