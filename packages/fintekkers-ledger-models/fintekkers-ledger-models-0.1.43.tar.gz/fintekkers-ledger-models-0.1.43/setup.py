from setuptools import setup, find_packages

import os

version = '0.0.0'

if 'BUILD_VERSION' in os.environ:
    print("******************************************")
    print("************OVERRIDING VERSION FROM ENVIRONMENT******************")
    print("******************************************")
    version = os.environ.get('BUILD_VERSION')

print("******************************************")
print("******************************************")
print("******************************************")
print(f"********VERSION={version}***************************")
print("******************************************")
print("******************************************")
print("******************************************")

setup(
    name = "fintekkers-ledger-models",
    version=version,
    license='MIT',
    author="David Doherty",
    author_email='davidjdoherty@gmail.com.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/fintekkers/ledger-models',
    keywords='example project',
    install_requires=[
      ],

)