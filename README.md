# KAIST - CS420 Compiler Design - Term project
Semi C compiler implemented in python using PLY.

## Requirements
The parser uses the python ply module. On Ubuntu, this is found in the packet:

    python3-ply

, which leads to the next requirement:

**PYTHON VERSIONS LOWER THAN PYTHON3 ARE NOT SUPPORTED!**

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

The prompt describes the current function. The user can run commands from the list above by entering them into the terminal and pressing enter.

### Details of usage

- As a piece of code comes to its end, the context and variable stacks of the `main` function are kept for inspection using the debugger.
- When searching a variable using `print`, the current scope, including all parent scopes within the same function are searched for the variable. The first hit will return the searched variable. If the function scopes does not have a reference to the variable, the *global scope* is searched for the variable. The same goes for the `trace` function.

## Testing
The code has been tested with the provided c source file, as well as a small simpler c source file. Both these are included within this project.

## Additional features
Additional features implemented are:

- **Global variables** - It is not only possible to have access to local variables in the scopes within the function, but also to a global variable table. Variables accessed here are treated the same way as if they existed in the local scope.
