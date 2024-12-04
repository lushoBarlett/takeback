# Take Back

What's rightfully mine!

## Motivation

Google Takeout is a service that allows you to export your data from Google products. It's a great service, but it doesn't export the data in its original format, the pictures don't have their original names or metadata.

## Solution

This repository attempts to read the exported data from Google Takeout, as it was exported, and organize it in a way that's more natural. This works for Google Photos at the moment.

## Features

- Read the exported data from Google Takeout "as is"
- Merge the metadata with the original files
- Output in a more natural folder structure, as desired by the user

## Software Design

The items of change are the following:

1. The folder structure outputted by Google Takeout.
2. The metadata contained in the JSON files.
3. File types.
4. The desired folder structure.

The software will have the following modules. These are an approximation to UML classes.

```plantuml
@startuml

class INode {
    + name(): str
    + setName(name: str)
    + parent(): INode
    + setParent(parent: INode)
    + children(): list[INode]
    + addChild(child: INode)
    + removeChild(child: INode)
}

class Folder : INode {
    + files(): list[File]
    + addFile(file: File)
    + folders(): list[Folder]
    + addFolder(folder: Folder)
}

class File : INode {
    + merge(metadata: Metadata)
}

class Metadata : INode {
    + properties(): list[str]
    + value(property: str): str
}

class FileIterator {
    + __init__(folder: Folder)
    + __iter__(): FileIterator
    + __next__(): File
}

class OutputStrategy {
    + go(inputFolder: Folder): Folder
}

class RemoveOldFolderStructure : OutputStrategy {}
class DateFileNames : OutputStrategy {}
class FolderPerYearAndMonth : OutputStrategy {}

class GoogleTakeoutReader {
    + canRead(folder: src): bool
    + read(folder: src): Folder
}

class FileSystemWriter {
    + canWrite(folder: Folder): bool
    + write(folder: Folder)
}

class OptionsParser {
    + parse(args: list[str]): list[OutputStrategy]
}
```

The `GoogleTakeoutReader` reads the exported data from Google Takeout. The `OutputStrategy` classes are responsible for organizing the data in a more natural way. One can apply many of them in a sequential manner. The `FileSystemWriter` writes the data to the file system. The `FileIterator` is a helper class to iterate over the files in a recursive folder structure. The `INode` interface is a common interface for `Folder`, `File`, and `Metadata`. Finally, the `OptionsParser` is responsible for parsing the command-line arguments and interpret which stragegies to apply and in which order.

