from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_ethereum',
    packages=find_packages(),
    package_data={
        "xchainpy_ethereum": ["resources/*"],
    },
    include_package_data=True,
    version='0.2.1',
    license='MIT',
    description='Custom Ethereum client and utilities used by XChainPY clients',
    author='THORChain',
    author_email='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xchainjs/xchainpy-lib/tree/main/xchainpy/xchainpy_ethereum',
    keywords=["ETH", "Ethereum", "XChainpy_ethereum","THORChain", "web3"],
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