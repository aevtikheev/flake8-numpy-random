import ast
import sys
from typing import Any, Generator, List, Tuple, Type, Set


if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


NPR001 = 'NPR001 do not use numpy.random()'


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.np_random_calls: List[Tuple[int, int]] = []
        self._numpy_imports: Set[str] = set()
        self._random_imports: Set[str] = set()

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Catch importing random from numpy."""
        if node.module == 'numpy':
            for name in node.names:
                alias = name.asname if name.asname is not None else name.name
                self._random_imports.add(alias)

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """Catch importing numpy."""
        for name in node.names:
            if name.name == 'numpy':
                alias = name.asname if name.asname is not None else name.name
                self._numpy_imports.add(alias)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Catch calling numpy.random and store line number and offset."""
        if hasattr(node.func, 'value') and hasattr(node.func.value, 'id'):
            if node.func.value.id in self._numpy_imports and node.func.attr == 'random':
                self.np_random_calls.append((node.lineno, node.col_offset))
        else:
            if hasattr(node.func, 'id') and node.func.id in self._random_imports:
                self.np_random_calls.append((node.lineno, node.col_offset))

        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col in visitor.np_random_calls:
            yield line, col, NPR001, type(self)
