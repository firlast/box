# 0.1.0 (April 13, 2023)

- [PyPI Release](https://pypi.org/project/box-vcs/0.1.0)
- [GitHub Release](https://github.com/firlast/box/releases/tag/v0.1.0)
- [Version documentation](https://github.com/firlast/box/blob/master/docs/0.1.0.md)

## Features

- Create `Commit` class.
- Create `Tracker` class.
- Create file ignoring system from the `.ignore` file
- Create CLI commands:
  - Add `init` command.
  - Add `commit` command.
  - Add `add` command.
  - Add `integrity` command.
  - Add `config` command.
  - Add `diff` command.
  - Add `log` command.
  - Add `status` command.

# 0.2.0 (May 22, 2023)

- [PyPI Release](https://pypi.org/project/box-vcs/0.2.0)
- [GitHub Release](https://github.com/firlast/box/releases/tag/v0.2.0)
- [Version documentation](https://github.com/firlast/box/blob/master/docs/0.2.0.md)

## Features

- Ignore files that end with such an extension.
- New CLI flags to:
  - Filter commits log by author name
  - Filter commits log by author email

# 0.2.1 (May 22, 2023)

- [PyPI Release](https://pypi.org/project/box-vcs/0.2.1)
- [GitHub Release](https://github.com/firlast/box/releases/tag/v0.2.1)
- [Version documentation](https://github.com/firlast/box/blob/master/docs/0.2.0.md)

## Fixes

- Allow setting name and email before creating a repository

# 0.3.0 (June 09, 2023)

- [PyPI Release](https://pypi.org/project/box-vcs/0.3.0)
- [GitHub Release](https://github.com/firlast/box/releases/tag/v0.3.0)
- [Version documentation](https://github.com/firlast/box/blob/master/docs/0.3.0.md)

## Features

- Filter commits logs by commit date
- Improve logs filter

## Fixes

- Preventing the root directory (./) from being accidentally ignored because of whitespace in the `.ignore` file
- Preventing use of `-am` flag when files as parameter in `commit` command.