from __future__ import annotations
import json
from typing import Union


class INode:
    def __init__(self, name: str, parent: Union[INode, None] = None):
        self._name = name
        self._parent = parent
        self._children = []

    def name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def parent(self) -> Union[INode, None]:
        return self._parent

    def set_parent(self, parent: Union[INode, None]) -> None:
        self._parent = parent

    def children(self) -> list[INode]:
        return self._children

    def add_child(self, child: INode) -> None:
        self._children.append(child)
        child._parent = self

    def remove_child(self, child: INode) -> None:
        self._children.remove(child)
        child._parent = None


def _build_path_recursive(node: INode) -> list[str]:
    path = []
    while node is not None:
        path.append(node._name)
        node = node.parent()
    path.reverse()
    return path


class Folder(INode):
    def __init__(self, name: str, parent: Union[INode, None] = None):
        super().__init__(name, parent)

    def fullname(self) -> str:
        return "/".join(_build_path_recursive(self) + [""])

    def files(self) -> list[File]:
        return [child for child in self.children() if isinstance(child, File)]

    def __validate_type(self, inode: INode, t: type) -> None:
        if not isinstance(inode, t):
            raise ValueError(f"inode must be of type {t}")

        if inode.parent() is not None:
            raise ValueError("inode already has a parent")

    def add_file(self, file: File) -> None:
        self.__validate_type(file, File)
        self.add_child(file)
        file.set_parent(self)

    def folders(self) -> list[Folder]:
        return [child for child in self.children() if isinstance(child, Folder)]

    def add_folder(self, folder: Folder) -> None:
        self.__validate_type(folder, Folder)
        self.add_child(folder)
        folder.set_parent(self)

    def __repr__(self):
        return (
            self._name + "/\n" +
            "\n".join([
                "  |  " + child._name + ("/" if isinstance(child, Folder) else "")
                for child in self.children()
            ])
        )


class File(INode):
    def __init__(self, name: str, parent: Union[INode, None] = None):
        super().__init__(name, parent)
        self._metadata = None
        self._original = None

    def fullname(self) -> str:
        return "/".join(_build_path_recursive(self))

    def copy_contents_from(self, file_path: str) -> None:
        self._original = file_path

    def contents(self) -> bytes:
        if self._original is None:
            raise ValueError("No original file to copy contents from")

        with open(self._original, "rb") as f:
            return f.read()

    def add_child(self, child: INode) -> None:
        pass

    def children(self) -> list[INode]:
        return []

    def merge(self, md: Metadata) -> None:
        self._metadata = md

    def __repr__(self):
        return self._name


class Metadata(INode):
    def __init__(self, name: str, parent: Union[INode, None] = None):
        super().__init__(name, parent)
        self._data = {}

    def read_from(self, name: str) -> None:
        with open(name, "r") as f:
            self._data = json.load(f)

    def properties(self) -> list[str]:
        return list(self._data.keys())

    def value(self, key: str) -> str:
        return self._data[key]


class FileIterator:
    def __init__(self, folder: Folder):
        self._folder = folder

    def __iter__(self):
        def dfs(node: INode):
            yield node
            for child in node.children():
                yield from dfs(child)

        self._iterator = dfs(self._folder)

        return self

    def __next__(self):
        return next(self._iterator)
