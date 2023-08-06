#!/usr/bin/env python3
import sys

try:
    from bare_estate.commands import cli_args, log_err, init, clone, git, NotARepositoryError
except ImportError:
    from commands import cli_args, log_err, init, clone, git, NotARepositoryError


def main():
    status = 0

    try:
        if cli_args[0] == "init":
            status = init()
        elif cli_args[0] == "clone":
            status = clone()
        else:
            status = git()

    except FileNotFoundError:
        log_err("Error: the repository has not been initialized yet.")
        log_err("You can create a new repository using the command:\n")
        log_err("bare init")
        status = 2

    except NotARepositoryError as error:
        message = error.strerror
        log_err(message)
        status = 3

    except NotADirectoryError as error:
        file = error.filename
        log_err(f"Error: A file with the name {file} already exists.")
        status = 3

    except IndexError:
        log_err("Error: no command was provided to git")
        status = 4

    return status


if __name__ == "__main__":
    sys.exit(main())
