class INode {
    def __init__(self):
        self._name = None
        self._parent = None
        self._children = []

    def name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    def parent(self):
        return self._parent

    def set_parent(self, parent: INode|None):
        self._parent = parent

    def children(self):
        return self._children

    def add_child(self, child: INode):
        self._children.append(child)
        child._parent = self

    def remove_child(self, child: INode):
        self._children.remove(child)
        child._parent = None
}


def _build_path_recursive(node: INode):
    path = []
    while node is not None:
        path.append(node.name())
        node = node.parent()
    path.reverse()
    return path


class Folder(INode) {
    def __init__(self):
        super().__init__()

    def name(self):
        return "/".join(__build_path_recursive(self) + [""])

    def files(self):
        return child for child in self.children() if isinstance(child, File)

    def __validate_type(self, inode: INode, t: type):
        if not isinstance(inode, t):
            raise ValueError(f"inode must be of type {t}")

        if inode.parent() is not None:
            raise ValueError("inode already has a parent")

    def add_file(self, file: File):
        self.__validate_type(file, File)
        self.add_child(file)
        file.set_parent(self)

    def folders(self):
        return child for child in self.children() if isinstance(child, Folder)

    def add_folder(self, folder: Folder):
        self.__validate_type(folder, Folder)
        self.add_child(folder)
        folder.set_parent(self)
}


class File(INode) {
    def __init__(self):
        super().__init__()
        self._metadata = None

    def name(self):
        return "/".join(__build_path_recursive(self))

    def add_child(self, child: INode):
        pass

    def children(self):
        return []

    def merge(self, md: Metadata):
        self._metadata = md
}


class Metadata(INode) {
    def __init__(self):
        super().__init__()
        self._data = {}

    def properties(self) -> list[str]:
        return list(self._data.keys())

    def value(self, key: str) -> str:
        return self._data[key]
}


class FileIterator {
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
}
