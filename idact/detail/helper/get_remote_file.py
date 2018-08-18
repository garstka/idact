"""This module contains a function for downloading a file from cluster
    in a Fabric task."""

from io import BytesIO

from fabric.operations import get


def get_remote_file(remote_path: str) -> str:
    """Fetches remote file as a string.

        Expects authentication to have been performed already.

        :param remote_path: Remote file path.

    """
    file = BytesIO()
    get(remote_path, file)
    contents = file.getvalue().decode()
    return contents
