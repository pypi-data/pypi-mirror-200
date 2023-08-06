from typing import List


def humanise_list(items: List[str]) -> str:
    """
    Humanise a list of items

    :param items: List of items
    :return: Humanised string
    """

    if len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return f"{items[0]} and {items[1]}"
    else:
        return ", ".join(items[:-1]) + f" and {items[-1]}"
