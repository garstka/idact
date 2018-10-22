import sys


def ensure_stdin_has_fileno():
    """Replaces :`sys.stdin.fileno` to make the program compatible with Click
        isolation. This is a fix for Fabric requiring a real file to back
        :attr:`sys.stdin` on Linux. See also :func:`.disable_pytest_stdin`.

        Fabric's approach clashes with `Click` replacing
        :attr:`sys.stdin` with a :class:`io.TextIOWrapper`, when testing
        in isolation.

    """

    def fake_stdin_fileno():
        return 0

    sys.stdin.fileno = fake_stdin_fileno
