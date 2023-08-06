import os
import sys
import subprocess as sp
import errno
import tempfile

try:
    from bare_estate.config import configs, HOME
except ImportError:
    from config import configs, HOME


class NotARepositoryError(NotADirectoryError):
    pass


cli_args = sys.argv[1:]
bare_cmd = ["git",
            f"--git-dir={configs['history_location']}",
            f"--work-tree={HOME}"]


log_err = lambda message: print(message, file=sys.stderr)


def validate_file_type(file_stats):
    file_entry, file_type = file_stats
    error_message = f"{configs['history_location']} is not a bare repository"

    if file_type == "file" and not file_entry.is_file():
        raise NotARepositoryError(
            errno.ENOTDIR,
            error_message,
            configs["history_location"]
        )
    if file_type == "directory" and not file_entry.is_dir():
        raise NotARepositoryError(
            errno.ENOTDIR,
            error_message,
            configs["history_location"]
        )


def get_file_stats(bare_repo_files):
    stats_list = []
    for file in bare_repo_files:
        if file.name in ["HEAD", "config", "description"]:
            stats_list.append([file, "file"])
        elif file.name in ["branches", "hooks", "info", "objects", "refs"]:
            stats_list.append([file, "directory"])

    return stats_list


def history_dir_exists():
    bare_repo_files = []
    for file in os.scandir(configs["history_location"]):
        bare_repo_files.append(file)

    bare_repo_files.sort(key=lambda file: file.name)
    file_stats = get_file_stats(bare_repo_files)

    for file in file_stats:
        validate_file_type(file)


def init():
    init_cmd = ["git", "init", "--bare", configs["history_location"]]
    config_cmd = [*bare_cmd, "config", "status.showUntrackedFiles", "no"]

    status = sp.run(init_cmd).returncode
    status += sp.run(config_cmd).returncode

    return status


def clone():
    status = 1
    repository = cli_args[1]

    with tempfile.TemporaryDirectory() as tmp_dir:
        clone_cmd = ["git",
                     "clone",
                     "--bare",
                     "--quiet",
                     f"--separate-git-dir={configs['history_location']}",
                     repository,
                     f"{tmp_dir}/dotfiles"]

        rsync_cmd = ["rsync",
                     "--recursive",
                     "--verbose",
                     "--exclude",
                     ".git",
                     f"{tmp_dir}/dotfiles/",
                     f"{HOME}/"]

        config_cmd = [*bare_cmd, "config", "status.showUntrackedFiles", "no"]

        status = sp.run(clone_cmd).returncode
        status += sp.run(rsync_cmd).returncode
        status += sp.run(config_cmd).returncode

    return status


def git():
    history_dir_exists()

    status = sp.run([*bare_cmd, *cli_args]).returncode

    return status
