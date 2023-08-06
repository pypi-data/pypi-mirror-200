# from setuptools import setup, find_packages
from distutils.core import setup

setup(
    name='multidirectional_graph',
    version='0.1.1dev05',
    description='Package for plotting multidirectional graphs',
    author='Seu nome',
    author_email='seuemail@example.com',
    packages=["multidirectional_graph"],
    package_data={
    'multidirectional_graph': [
            'multidirectional_graph/fonts/Oswald/*',
            'multidirectional_graph/fonts/Roboto/*',
            'multidirectional_graph/fonts/SourceSerif/*',
        ]
    },
    include_package_data=True,
    install_requires=['matplotlib'],
)