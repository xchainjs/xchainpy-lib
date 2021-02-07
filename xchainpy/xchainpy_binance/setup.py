from setuptools import setup

def install_requires():
    requires = [
        'secp256k1==0.13.2',
        'pytest==6.1.2',
        'mnemonic==0.19',
        'python_binance_chain==0.1.20',
        'pywallet==0.1.0',
        'binance_chain==1.0.0'
    ]
    return requires

setup(
    name='xchainpy',
    packages=['xchainpy'],
    version='0.1',
    license='MIT',
    description='Custom Binance client and utilities used by XChainJS clients',
    author='Thorchain',
    author_email='',
    url='https://github.com/xchainjs/xchainpy-lib',
    download_url='https://github.com/xchainjs/xchainpy-lib/archive/v_01.tar.gz',
    keywords=["BNB", "Binance", "XChain"],
    install_requires=install_requires(),
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
