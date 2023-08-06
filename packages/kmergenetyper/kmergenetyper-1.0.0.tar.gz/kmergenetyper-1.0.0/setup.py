from setuptools import setup, find_packages

setup(
    name='kmergenetyper',
    version='1.0.0',
    packages=find_packages(),
    data_files=[],
    include_package_data=True,
    url='https://https://github.com/MBHallgren/KGT',
    license='',
    install_requires=(),
    author='Malte B. Hallgren',
    scripts=['bin/kgt'],
    author_email='malhal@food.dtu.dk',
    description='KGT - K-mer Gene Typer',
)