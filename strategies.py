from abc import ABC, abstractmethod
from inode import Folder, FileIterator
import copy
import datetime
import requests
from cli import CLI
from collections import defaultdict


class OutputStrategy(ABC):

    @abstractmethod
    def go(self, folder: Folder) -> Folder:
        pass

    def __repr__(self):
        return self.__class__.__name__


class DateFileNames(OutputStrategy):

    def go(self, folder: Folder) -> Folder:
        folder = copy.deepcopy(folder)

        for file in FileIterator(folder):
            timestamp = file._metadata.timestamp()
            dt = datetime.datetime.fromtimestamp(timestamp)
            file.set_name(dt.strftime("%Y-%m-%d %H:%M:%S." + file.extesion()))

        return folder


class FolderPerYearAndMonth(OutputStrategy):

    def _convert_dicts_to_folders(self, structure: dict) -> Folder:
        folder = Folder("Timeline")

        for year, month in structure.items():
            year_folder = Folder(str(year))

            for month, files in month.items():
                month_name = datetime.datetime(year, month, 1).strftime("%B")
                month_folder = Folder(str(month) + "." + month_name)

                for file in files:
                    month_folder.add_file(file)

                year_folder.add_folder(month_folder)

            folder.add_folder(year_folder)

        return folder

    def go(self, folder: Folder) -> Folder:
        folder = copy.deepcopy(folder)

        structure = defaultdict(dict)

        for file in FileIterator(folder):
            file.set_parent(None)
            timestamp = file._metadata.timestamp()

            dt = datetime.datetime.fromtimestamp(timestamp)
            year, month = dt.year, dt.month

            if month not in structure[year]:
                structure[year][month] = []
            structure[year][month].append(file)

        return self._convert_dicts_to_folders(structure)
