import subprocess
from cli import CLI
from inode import File, Metadata
from datetime import datetime


def check_exiftool_is_installed():
    try:
        subprocess.run(["exiftool", "-ver"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        CLI.fatal("ExifTool is not installed. Find installation instructions at https://exiftool.org/")


def write_exif_metadata(file: File, metadata: Metadata):
    check_exiftool_is_installed()

    exif_args = [
        "-DateTimeOriginal=" + str(datetime.fromtimestamp(metadata.timestamp()).isoformat()),
        "-GPSLongitude=" + str(metadata.longitude()),
        "-GPSLatitude=" + str(metadata.latitude()),
        "-GPSAltitude=" + str(metadata.altitude()),
    ]

    if len(exif_args) > 0:
        exif_args.append("-overwrite_original")
        exif_args.append(file.fullname())
        subprocess.run(["exiftool"] + exif_args)
