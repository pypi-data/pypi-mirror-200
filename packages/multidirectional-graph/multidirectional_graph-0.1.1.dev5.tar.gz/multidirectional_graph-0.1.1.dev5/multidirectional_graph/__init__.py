from multidirectional_graph._graph import MultidirectionalGraph
from pkg_resources import resource_filename

font_path = resource_filename('multidirectional_graph', 'fonts')

# data = resource_filename(Requirement.parse("main_package"), 'mypackage/data')

print(font_path)

__all__ = [
    "MultidirectionalGraph"
]