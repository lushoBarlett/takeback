import sys
from options import OptionsParser
from folderio import GoogleTakeoutReader, FileSystemWriter
from inode import Folder, File, Metadata
from cli import CLI
from exif import check_exiftool_is_installed


if __name__ == "__main__":
    parser = OptionsParser(sys.argv[1:])

    check_exiftool_is_installed()

    if not GoogleTakeoutReader.exists(parser.input_folder()):
        CLI.warning(f"Folder {parser.input_folder()} does not exist")
        sys.exit(1)

    folder = GoogleTakeoutReader.read(parser.input_folder())

    for strategy in parser.strategies():
        CLI.out(f"Applying strategy {strategy}")
        folder = strategy.go(folder)

    success, message = FileSystemWriter.write(folder)

    if not success:
        CLI.warning(message)
        sys.exit(2)

    CLI.out("Done")
