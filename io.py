import os

class GoogleTakeoutReader:

    def exists(folder_path: str) -> bool:
        return os.path.exists(folder_path)

    def read(folder_path: str) -> Folder:
        if not exists(folder_path):
            raise ValueError(f"Folder {folder_path} does not exist")

        folder = Folder()

        for file in os.listdir(folder_path):
            if os.path.isdir(file):
                folder.add_folder(read(os.path.join(folder_path, file))
            else:
                folder.add_file(File(file))

        return folder


class FileSystemWriter {

    def write(folder: Folder): bool, str {
        if exists(folder.name()):
            return False, f"Folder {folder.name()} already exists"

        os.mkdir(folder.name())

        for file in folder.files():

            if os.path.exists(os.path.join(folder.name(), file.name())):
                return False, f"File {file.name()} already exists"

            with open(os.path.join(folder.name(), file.name()), "w") as f:
                f.write(file.contents())

        for subfolder in folder.folders():
            if not r := write(subfolder):
                return r

        return True, ""
    }
}
