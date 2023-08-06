#!python

import pathlib
import os

import exploration

import argparse


def pickExistingFile(kind: str) -> pathlib.Path:
    """
    Uses `input` to prompt the user to select an existing file in the
    current directory (or a custom path they type in). Continues
    prompting until an existing file is named. The `kind` argument is
    used before the word 'file' to describe what is being requested; it
    should normally include an article, e.g., 'a source' or 'an input'.
    """
    options = os.listdir('.')
    prompt = f"""\
Select {kind} file:
  """ + '\n  '.join(
    f"[{n}] '{options[n]}'"
    for n in range(len(options))
) + f"""[{len(options)}] Other...
Pick a number from the list above (default 0): """
    selection = 'a'
    while selection.strip() and not selection.strip().isdigit():
        selection = input(prompt)

    if selection.strip() == '':
        index = 0
    else:
        index = int(selection.strip())

    if index < len(options):
        return pathlib.Path(options[index])

    path = None
    prompt = "Write the path you want to use as {kind} file: "
    while path is None or not path.isfile():
        if path is not None:
            if path.exists():
                print("You must pick a regular file, not a directory.")
            else:
                print("The file '{path!s}' does not exist.")
        pathStr = input(prompt)
        path = pathlib.Path(pathStr)

    return path


def pickOutputFile(
    purpose: str,
    preferNew: bool = True
) -> pathlib.Path:
    """
    Uses `input` to prompt the user for a filename to be used for the
    given purpose. If `preferNew` is set to `True`, a confirmation
    prompt will be displayed when the user picks a file that already
    exists, which warns that the file may be overwritten. The resulting
    path will not be an existing directory.
    """
    result = None
    prompt = f"Write the path to the file you want to use for {purpose}: "
    while result is None or result.is_dir():
        if result is not None:
            print(
                f"'{result!s} is a directory, so it can't be used for"
                f" {purpose}."
            )
        result = pathlib.Path(input(prompt))

        if preferNew and result.exists():
            overwrite = input(
                f"File '{result!s}' already exists. Are you sure you"
                f" want to use it for {purpose} (it may be"
                f" overwritten)? [y/N] "
            )
            if overwrite.strip().lower() in ('y', 'yes'):
                print(
                    f"Okay, we will use '{result!s}' for {purpose} even"
                    f" though it already exists."
                )
            else:
                print(f"Okay, pick another file to use for {purpose}...")
                result = None

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        argument_default=None,
        description='''\
Displays, converts, or analyzes `DecisionGraph` and/or `Exploration`
objects created by the `exploration` python library. Understands the
following file formats:

- '.dcg' A `core.DecisionGraph` stored in JSON format.
- '.dot' A `core.DecisionGraph` stored as a GraphViz DOT file.
- '.exp' A `core.Exploration` stored in JSON format.
- '.exj' A `core.Exploration` stored as a journal (see
    `journal.JournalObserver`; TODO: writing this format).
''',
        epilog='''\
The program will prompt interactively for information when arguments are
omitted.
'''
    )
    parser.add_argument('command', help='''\
Which command to run:
    - 'display' for displaying a graph using matplotlib,
    - 'convert' for converting between graph/journal formats, or
    - 'analyze' for analyzing a graph'''
    )  # noqa
    parser.add_argument('inputFile', help='The input filename.')
    parser.add_argument(
        'outputFile',
        help="The output filename, when using 'convert' or 'analyze'."
    )
    parsed = parser.parse_args()

    command = parsed.command
    if command is None:
        command = input("""\
Choose the command:
  [0] display a decision graph
  [1] analyze an exploration or decision graph
  [2] convert an exploration or decision graph
What would you like to do? (enter a number; default is 0) """)
        if command.strip() == '1':
            command = "analyze"
        elif command.strip() == '2':
            command = "convert"
        else:
            if command.strip() not in ('0', ''):
                print(
                    f"Invalid command '{command}' assuming you meant 0"
                    f" (display a graph)"
                )
            command = "display"

    inputFile = parsed.inputFile
    if (
        inputFile is None
     or not os.path.exists(inputFile)
     or not os.path.isfile(inputFile)
    ):
        print("No source file (or invalid source file) specified...")
        source = pickExistingFile('a source')
    else:
        source = pathlib.Path(inputFile)

    try:
        sourceType = exploration.main.determineFileType(str(source))
    except ValueError:
        print(
            f"We didn't recognize the file extension of"
            f" '{source!s}' so we assume it's a journal."
        )
        sourceType = "journal"

    if command.strip() == "show":
        exploration.main.show(source, formatOverride=sourceType)

    if command.strip() == 'analyze':
        exploration.main.analyze(source, formatOverride=sourceType)

    elif command.strip() == "convert":
        outputFile = parsed.outputFile
        if (
            outputFile is None
         or os.path.isdir(outputFile)
        ):
            print("Invalid output file (or directory) provided...")
            output = pickOutputFile('output')
        else:
            output = pathlib.Path(outputFile)

        try:
            outputType = exploration.main.determineFileType(str(output))
        except ValueError:
            print(
                f"We didn't recognize the file extension of"
                f" '{output!s}'."
            )
            if sourceType == "graph":
                print(
                    "We assume you wanted to convert the input graph"
                    " into GraphViz DOT format."
                )
                outputType = "dot"
            elif sourceType == "dot":
                print(
                    "We assume you wanted to convert the input graph"
                    " into JSON format."
                )
                outputType = "graph"
            elif sourceType == "exploration":
                print(
                    "We assume you wanted to convert the input"
                    " exploration into journal format."
                )
                outputType = "journal"
            else:
                print(
                    "We assume you wanted to convert the input"
                    " exploration into JSON format."
                )
                outputType = "exploration"

        exploration.main.convert(
            source,
            output,
            inputFormatOverride=sourceType,
            outputFormatOverride=outputType
        )

    else:
        print(f"Unrecognized command '{command}'.\n")
        parser.print_help()
        exit(1)
