from io import BytesIO

from fabric.operations import get


def get_remote_file(remote_path: str) -> str:
    """Fetches remote file as string.

        :param remote_path: Remote file path

    """
    file = BytesIO()
    get(remote_path, file)
    contents = file.getvalue().decode()
    return contents
