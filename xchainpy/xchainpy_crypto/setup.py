from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_crypto',
    packages=find_packages(),
    version='0.1.10',
    license='MIT',
    description='XCHAIN-CRYPTO encrypts a master phrase to a keystore',
    author='THORChain',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xchainjs/xchainpy-lib/tree/main/xchainpy/xchainpy_crypto',
    keywords=["THORChain", "XChainpy","XChainpy_crypto"],
    install_requires=['mnemonic>=0.18', 'bip_utils ==1.11.1, <=2.0.0', 'pycryptodome >= 3.10.1, <=4.0.0'],
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