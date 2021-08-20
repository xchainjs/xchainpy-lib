from setuptools import setup , find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_litecoin',
    packages=find_packages(),
    version='0.2',
    license='MIT',
    description='Litecoin Module for XChainPy Clients',
    author='THORChain',
    author_email='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xchainjs/xchainpy-lib/tree/main/xchainpy/xchainpy_litecoin',
    keywords=["THORChain", "XChainpy","xchainpy_litecoin"],
    install_requires=['bitcoinlib>=0.5.2', 'http3>=0.6.7', 'xchainpy_client>=0.1.5', 'xchainpy_crypto>=0.1.7', 'xchainpy_util>=0.1.7', 'bip_utils>=1.11.1'],
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