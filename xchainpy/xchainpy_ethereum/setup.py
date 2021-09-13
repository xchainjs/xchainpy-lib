from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_ethereum',
    packages=find_packages(),
    package_data={
        "xchainpy_ethereum": ["resources/*"],
    },
    include_package_data=True,
    version='0.2.2',
    license='MIT',
    description='Custom Ethereum client and utilities used by XChainPY clients',
    author='THORChain',
    author_email='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xchainjs/xchainpy-lib/tree/main/xchainpy/xchainpy_ethereum',
    keywords=["ETH", "Ethereum", "XChainpy_ethereum","THORChain", "web3"],
    install_requires=["web3>=5.22.0", "websockets>=9.1",'xchainpy_client>=0.1.6',
                      'xchainpy_crypto>=0.1.7', 'xchainpy_util>=0.1.8'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)