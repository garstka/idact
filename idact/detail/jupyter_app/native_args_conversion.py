from typing import Dict, Optional, List


# pylint: disable=bad-continuation
def convert_native_args_from_command_line_to_dict(
    native_args: List[List[str]]) -> Dict[str, Optional[str]]:  # noqa
    """Converts allocation native args from command line to the format
        expected by :meth:`.Cluster.allocate_nodes`.

        :param native_args: Native args to convert.

    """
    return {key: (value if value != 'None' else None)
            for (key, value) in zip(native_args[0], native_args[1])}
