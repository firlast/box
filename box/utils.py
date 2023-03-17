from hashlib import sha1
from secrets import token_hex


def enumerate_lines(file_lines: list) -> dict:
    lines = enumerate(file_lines)
    return dict((str(ln), l) for ln, l in lines)


def difference_lines(older_enum_lines: dict, new_enum_lines: dict) -> dict:
    difference = {}

    # get deleted or existent lines difference
    for number, line in older_enum_lines.items():
        new_line = new_enum_lines.get(number)

        if not new_line:
            difference[number] = None
        elif new_line != line:
            difference[number] = new_line

    # get new lines
    for number, line in new_enum_lines.items():
        if not older_enum_lines.get(number):
            difference[number] = line

    return difference


def generate_id(*complements: str) -> str:
    id_parts = ''.join((
        token_hex(16),
        *complements
    ))
    return sha1(id_parts.encode()).hexdigest()


def divide_list(parts: int, iterable: list) -> list:
    if parts > 1:
        q, r = divmod(len(iterable), parts)
        split_list = []
        stop = 0

        for i in range(1, parts + 1):
            start = stop
            stop += q + 1 if i <= r else q
            split_list.append(iterable[start:stop])

        return split_list
    else:
        raise ValueError('"parts" must be at least 1')
