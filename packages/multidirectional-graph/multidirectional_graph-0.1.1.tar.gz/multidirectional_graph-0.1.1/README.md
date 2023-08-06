# Multidirectional Graph

[![PyPI version](https://badge.fury.io/py/multidirectional-graph.svg)](https://badge.fury.io/py/multidirectional-graph)
[![codecov](https://codecov.io/gh/username/multidirectional-graph/branch/main/graph/badge.svg?token=abc123def456)](https://codecov.io/gh/username/multidirectional-graph)

Multidirectional Graph is a Python package that allows you to easily create graphs with multiple evaluation criteria, such as good, neutral, and bad.

## Installation

You can install Multidirectional Graph using pip:

```bash
pip install multidirectional-graph
```

## Usage

Here is an example of how to use Multidirectional Graph:

```python
from multidirectional_graph import MultidirectionalGraph

data = {
    "Leitura": {
        "categ 1A": 5,
        "categ 1B": 9,
        "categ 1C": 5,
    },
    "Escrita": {
        "categ 2A": 2,
        "categ 2B": 4,
        "categ 2C": 9,
        "categ 2D": 3,
    },
    "Fluência": {
        "categ 3A": 6,
        "categ 3B": 7,
    },
    "Listening": {
        "categ 4A": 2,
        "categ 4B": 3,
    },
}

graph = MultidirectionalGraph(
    data,
    tipo_avaliacao = "Lingua Inglesa",
    good_color="green",
    figsize=(4,15)
)

fig = graph.plot()

```

![](images/teste.png)