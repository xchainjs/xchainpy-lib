from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xchainpy_util',
    packages=['xchainpy_util'],
    version='0.1.5',
    license='MIT',
    description='Utility helpers for XChain clients',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='THORChain',
    author_email='',
    url='https://github.com/xchainjs/xchainpy-lib/tree/main/xchainpy/xchainpy_util',
    keywords=["THORChain", "XChainpy","xchainpy_util"],
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