# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)


def extract_name(path):
    """
    Extract the name from a path
    :param str: Path, having in the end of the line the name to extract with the .conf format
    :return: name
    """
    import os
    head_tail = os.path.split(path)
    name = head_tail[1].replace(".conf", "")
    del head_tail
    return name
