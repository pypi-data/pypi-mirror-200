from setuptools import setup, find_namespace_packages

setup(
    name='abv',
    version='1.0.0',
    description='Very helpful assistant bot',
    url='https://github.com/VadimTrubay/abv.git',
    author='Trubay_Vadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['numexpr'],
    entry_points={'console_scripts': ['abv=abv.main:main']},
    package_data={'abv': ['abv/*.txt', 'abv/*.bin']}
)