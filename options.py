from output_strategy import *
from argparse import ArgumentParser


class OptionsParser {

    def parse(self, args): list[OutputStrategy]

        parser = ArgumentParser()

        parser.add_argument("-r", "--removeold", action="store_true")
        parser.add_argument("-d", "--datenames", action="store_true")
        parser.add_argument("-y", "--yearandmonth", action="store_true")

        args = parser.parse_args(args)

        strategies = []

        if args.removeold:    strategies.append(RemoveOldFolderStructure())
        if args.datenames:    strategies.append(DateFileNames())
        if args.yearandmonth: strategies.append(FolderPerYearAndMonth())

        return strategies
}

