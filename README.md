# KAIST - CS420 Compiler Design - Term project
Semi C compiler implemented in python using PLY.

## Requirements
The parser uses the python ply module. On Ubuntu, this is found in the packet:

    python3-ply

, which leads to the next requirement:

**PYTHON VERSIONS LOWER THAN PYTHON3 IS NOT SUPPORTED!**

## Usage
The compiler is run using the `cmmc.py` file as:

    ./cmmc.py [c-source-file-path]

This will lex and parse the file, and if no syntax errors exists, drop the user into a simple shell. Here the following actions are supported:

    Commands:
        next
        next [x]
        print [variable]
        trace [variable]
        quit (CTRL+D)
        help

    >[main]>

The prompt describes the current function and lets the user input a command from the list above.

## Testing
The code has been tested with the provided c source file, as well as a small simpler c source file. Both these are included within this project.