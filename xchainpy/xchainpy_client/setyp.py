from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_client',
    packages=['xchainpy_client'],
    version='0.1',
    license='MIT',
    description='A specification for a generalised interface for crypto wallets clients, to be used by XChainPY implementations. The client should not have any functionality to generate a key, instead, the `asgardex-crypto` library should be used to ensure cross-chain com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='THORChain',
    author_email='',
    url='https://github.com/xchainjs/xchainpy-lib/tree/main/xchainpy/xchainpy_client',
    keywords=["THORChain", "XChainpy","xchainpy_client"],
    install_requires=[],
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
