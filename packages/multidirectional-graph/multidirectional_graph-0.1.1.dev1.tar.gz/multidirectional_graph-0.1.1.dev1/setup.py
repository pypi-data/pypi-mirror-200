from setuptools import setup, find_packages

setup(
    name='multidirectional_graph',
    version='0.1.1dev01',
    description='Package for plotting multidirectional graphs',
    author='Seu nome',
    author_email='seuemail@example.com',
    packages=find_packages(),
    package_data={'multidirectional_graph': ['fonts/*']},
    include_package_data=True,
    install_requires=['matplotlib'],
)