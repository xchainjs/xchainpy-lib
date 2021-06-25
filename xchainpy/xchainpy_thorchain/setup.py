from setuptools import setup , find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='xchainpy_thorchain',
    packages=find_packages(),
    version='0.1.8',
    license='MIT',
    description='Thorchain wrapper',
    author='THORChain',
    author_email='',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/xchainjs/xchainpy-lib',
    keywords=["THORChain", "XChainpy","xchainpy_thorchain"],
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