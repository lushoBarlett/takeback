from abc import ABC, abstractmethod


class OutputStrategy(ABC):

    @abstractmethod
    def go(self, folder: Folder) -> Folder:
        pass


class RemoveOldFolderStructure(OutputStrategy):

    def go(self, folder: Folder) -> Folder:
        # implement
        pass


class DateFileNames(OutputStrategy):

    def go(self, folder: Folder) -> Folder:
        # implement
        pass


class GeographicalAppendFileNames(OutputStrategy):

    def go(self, folder: Folder) -> Folder:
        # implement
        pass


class FolderPerYearAndMonth(OutputStrategy):

    def go(self, folder: Folder) -> Folder:
        # implement
        pass

