from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='xchainpy_bitcoincash',
    packages=['xchainpy_bictioncash'],
    version='0.1',
    license='MIT',
    description='Bitcoincash Module for XChainPy Clients',
    author='THORChain',
    author_email='',
    url='https://github.com/xchainjs/xchainpy-lib',
    download_url='https://github.com/xchainjs/xchainpy-lib/archive/v_01.tar.gz',
    keywords=["THORChain", "XChainpy","XChainpy_bitcoincash"],
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