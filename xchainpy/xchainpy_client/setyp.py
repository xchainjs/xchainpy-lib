from setuptools import setup

setup(
    name='xchainpy',
    packages=['xchainpy'],
    version='0.1',
    license='MIT',
    description='A specification for a generalised interface for crypto wallets clients, to be used by XChainPY implementations. The client should not have any functionality to generate a key, instead, the `asgardex-crypto` library should be used to ensure cross-chain com',
    author='THORChain',
    author_email='',
    url='https://github.com/xchainjs/xchainpy-lib',
    download_url='https://github.com/xchainjs/xchainpy-lib/archive/v_01.tar.gz',
    keywords=["BNB", "Binance", "XChain"],
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
