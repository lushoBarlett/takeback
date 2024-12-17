from abc import ABC, abstractmethod
from inode import Folder


class OutputStrategy(ABC):

    @abstractmethod
    def go(self, folder: Folder) -> Folder:
        pass

    def __repr__(self):
        return self.__class__.__name__


class DateFileNames(OutputStrategy):

    def go(self, folder: Folder) -> Folder:
        # implement
        return folder


class GeographicalAppendFileNames(OutputStrategy):

    def go(self, folder: Folder) -> Folder:
        # implement
        return folder


class FolderPerYearAndMonth(OutputStrategy):

    def go(self, folder: Folder) -> Folder:
        # implement
        return folder
