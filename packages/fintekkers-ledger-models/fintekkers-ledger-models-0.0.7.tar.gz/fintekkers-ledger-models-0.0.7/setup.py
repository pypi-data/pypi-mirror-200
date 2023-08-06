from setuptools import setup, find_packages

setup(
    name = "fintekkers-ledger-models",
    version='0.0.7',
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