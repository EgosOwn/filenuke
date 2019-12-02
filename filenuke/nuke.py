import os
import sys
import secrets
import string
from typing import NewType

NewPath = NewType('NewPath', str)

def _overwrite_file(file_path: str, passes: int, zeros=False):
    """overwrite a single file with secure random data passes times
    uses secrets library or zeros is zeros is set to true"""
    file_size: int = os.path.getsize(file_path)

    for _ in range(passes):
        if zeros:
            new_data = b'0' * file_size
        else:
            new_data = secrets.token_bytes(file_size)

        with open(file_path, 'wb') as top_secret_file:
            top_secret_file.write(new_data)


def _rename_inode(path: str, zeros=False) -> NewPath:
    """renames file randomly, or with zeros if zeros is true"""
    name_len = len(os.path.basename(path))
    new_name = ''
    path = os.path.abspath(path)
    assert os.path.exists(path)

    if zeros:
        new_name = '0' * name_len
    else:
        for _ in range(name_len):
            new_name += secrets.choice(string.ascii_letters)

    new_path = os.path.dirname(path) + '/' + new_name
    os.rename(path, new_path)

    return new_path


def clean_tree(directory: str):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(subdir, file))

def nuke(path: str):
    os.remove(path)
