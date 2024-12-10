from strategies import *
from argparse import ArgumentParser


class OptionsParser:

    def __init__(self, args):
        parser = ArgumentParser()

        parser.add_argument("-r", "--removeold", action="store_true",
                            help="Remove old folder structure")
        parser.add_argument("-d", "--datenames", action="store_true",
                            help="Use date in file names")
        parser.add_argument("-y", "--yearandmonth", action="store_true",
                            help="Create a folder per year, and a subfolder per month")

        parser.add_argument("-i", "--inputfolder", type=str, required=True,
                            help="Path to the input folder")

        self._parsed = parser.parse_args(args)

    def strategies(self) -> list[OutputStrategy]:
        strategies = []

        if self._parsed.removeold:    strategies.append(RemoveOldFolderStructure())
        if self._parsed.datenames:    strategies.append(DateFileNames())
        if self._parsed.yearandmonth: strategies.append(FolderPerYearAndMonth())

        return strategies

    def input_folder(self) -> str:
        return self._parsed.inputfolder
