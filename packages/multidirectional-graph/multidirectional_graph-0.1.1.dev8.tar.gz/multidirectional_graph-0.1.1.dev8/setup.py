from setuptools import setup, find_packages

setup(
    name="multidirectional_graph",
    version="0.1.1dev08",
    description="Package for plotting multidirectional graphs",
    author="Seu nome",
    author_email="seuemail@example.com",
    packages=["multidirectional_graph"],
    package_data={
        "multidirectional_graph": [
            "multidirectional_graph/fonts/Oswald/*.ttf",
            "multidirectional_graph/fonts/Roboto/*.ttf",
            "multidirectional_graph/fonts/SourceSerif/*.ttf",
        ]
    },
    data_files=[
        (
            "config",
            [
                "multidirectional_graph/fonts/Oswald/Oswald-Regular.ttf",
                "multidirectional_graph/fonts/SourceSerif/SourceSerifPro-Light.ttf",
            ],
        )
    ],
    include_package_data=True,
    install_requires=["matplotlib"],
)
