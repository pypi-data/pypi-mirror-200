# from setuptools import setup, find_packages
from distutils.core import setup

setup(
    name='multidirectional_graph',
    version='0.1.1dev04',
    description='Package for plotting multidirectional graphs',
    author='Seu nome',
    author_email='seuemail@example.com',
    packages=["multidirectional_graph"],
    package_data={'multidirectional_graph': ['multidirectional_graph/fonts/*']},
    include_package_data=True,
    install_requires=['matplotlib'],
)