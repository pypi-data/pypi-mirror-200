from setuptools import setup, find_packages

setup(
    name='multidirectional_graph',
    version='0.1.0',
    description='Package for plotting multidirectional graphs',
    author='Seu nome',
    author_email='seuemail@example.com',
    packages=find_packages(exclude=["fonts", "images"]),
    package_data={'multidirectional_graph': ['fonts/*.ttf']},
    install_requires=['matplotlib'],
)