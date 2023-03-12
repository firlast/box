def enumerate_lines(file_lines: list) -> dict:
    lines = enumerate(file_lines)
    return dict(lines)


def difference_lines(older_enum_lines: dict, new_enum_lines: dict) -> dict:
    difference = {}

    # get deleted or existent lines difference
    for number, line in older_enum_lines.items():
        new_line = new_enum_lines.get(number)

        if not new_line:
            difference[number] = None
        elif new_line != line:
            difference[number] = line

    # get new lines
    for number, line in new_enum_lines.items():
        if not older_enum_lines.get(number):
            difference[number] = line

    return difference
