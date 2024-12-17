import os, sys
from typing import Tuple
from inode import Folder, File, Metadata
from cli import CLI


class GoogleTakeoutReader:

    def exists(folder_path: str) -> bool:
        return os.path.exists(folder_path)

    def read(folder_path: str) -> Folder:
        if not GoogleTakeoutReader.exists(folder_path):
            raise ValueError(f"Folder {folder_path} does not exist")

        folder = Folder(folder_path.strip("/").split("/")[-1])

        entries = [name for name in os.listdir(folder_path)]

        files = [name for name in entries if os.path.isfile(os.path.join(folder_path, name))]
        normal_files = [name for name in files if not name.endswith(".json")]
        meta_files = [name for name in files if name.endswith(".json")]

        dirs = [name for name in entries if os.path.isdir(os.path.join(folder_path, name))]

        prepared_files = {}
        for name in normal_files:
            CLI.vanishing(f"@ Reading file {name}")
            file = File(name)
            file.copy_contents_from(os.path.join(folder_path, name))
            if name in prepared_files:
                CLI.warning(f"File {name} found with duplicate name, we don't support this yet")
            prepared_files[name] = file
            folder.add_file(file)

        for name in meta_files:
            CLI.vanishing(f"@ Reading meta file {name}")
            meta = Metadata(name)
            meta.read_from(os.path.join(folder_path, name))

            referred_name = name[:-5]
            if referred_name in prepared_files:
                prepared_files[referred_name].merge(meta)
            else:
                CLI.warning(f"Metadata file {name} has no corresponding file")

        for name in dirs:
            CLI.vanishing(f"@ Entering folder {name}")
            folder.add_folder(GoogleTakeoutReader.read(os.path.join(folder_path, name)))

        return folder


class FileSystemWriter:

    def write(folder: Folder) -> Tuple[bool, str]:
        CLI.out(f"Copying folder {folder.fullname()}")

        if GoogleTakeoutReader.exists(folder.fullname()):
            return False, f"Folder {folder.name()} already exists"

        os.mkdir(folder.fullname())

        for file in folder.files():
            CLI.vanishing(f"@ Writing file {file.name()}")

            if os.path.exists(file.fullname()):
                return False, f"File {file.name()} already exists"

            with open(file.fullname(), "wb") as f:
                f.write(file.contents())

        for subfolder in folder.folders():
            r = FileSystemWriter.write(subfolder)
            if not r[0]:
                return r

        return True, ""
