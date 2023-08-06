import os
import pathlib


def escape_windows_path(filepath):
    return os.path.normpath(
        r"\\".join(
            [
                f'"{x}"' if i != 0 else x
                for i, x in enumerate(
                    pathlib.Path(os.path.normpath(os.path.abspath(filepath))).parts
                )
            ]
        )
    )



