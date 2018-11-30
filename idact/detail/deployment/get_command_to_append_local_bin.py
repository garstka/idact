def get_command_to_append_local_bin() -> str:
    """Returns a command that prepends the pip local binary installation dir
        (usually `~/.local/bin`). It may not be in `PATH` for a non-login
        shell."""
    return 'export PATH="$PATH:$(python -m site --user-base)/bin"'
