from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_bitcoin',
    packages=find_packages(),
    version='0.2.3',
    license='MIT',
    description='Bitcoin Module for XChainPy Clients',
    author='THORChain',
    author_email='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xchainjs/xchainpy-lib',
    keywords=["THORChain", "XChainpy","XChainpy_bitcoin","BTC","Bitcoin"],
    install_requires=['bitcoinlib>=0.5.2', 'http3>=0.6.7', 'xchainpy_client>=0.1.6', 'xchainpy_crypto>=0.1.11', 'xchainpy_util>=0.1.8', 'bip_utils==1.11.1'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python'
    ],
)