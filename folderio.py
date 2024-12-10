import os
from typing import Tuple

from inode import Folder, File


class GoogleTakeoutReader:

    def exists(folder_path: str) -> bool:
        return os.path.exists(folder_path)

    def read(folder_path: str) -> Folder:
        if not GoogleTakeoutReader.exists(folder_path):
            raise ValueError(f"Folder {folder_path} does not exist")

        folder = Folder(folder_path.strip("/").split("/")[-1])

        for name in os.listdir(folder_path):
            fullname = os.path.join(folder_path, name)
            if os.path.isdir(fullname):
                folder.add_folder(GoogleTakeoutReader.read(fullname))
            else:
                file = File(name)
                file.copy_contents_from(fullname)
                folder.add_file(file)

        return folder


class FileSystemWriter:

    def write(folder: Folder) -> Tuple[bool, str]:
        if GoogleTakeoutReader.exists(folder.fullname()):
            return False, f"Folder {folder.name()} already exists"

        os.mkdir(folder.fullname())

        for file in folder.files():

            if os.path.exists(file.fullname()):
                return False, f"File {file.name()} already exists"

            with open(file.fullname(), "wb") as f:
                f.write(file.contents())

        for subfolder in folder.folders():
            r = FileSystemWriter.write(subfolder)
            if not r[0]:
                return r

        return True, ""
