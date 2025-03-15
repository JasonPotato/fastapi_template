"""simple tool to scrape data out of pyroject.toml"""

import argparse
import toml


def parse_script_args():
    """define script arguments this tool accepts"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pyproject_file",
        "-p",
        default="pyproject.toml",
        type=str,
        help="the path to pyproject.toml",
    )
    parser.add_argument(
        "--group",
        "-g",
        default="project",
        type=str,
        help="the group to parse from the target toml file",
    )
    parser.add_argument(
        "key", type=str, help="the key to parse from the target toml file"
    )
    return parser.parse_args()


def main():
    """main driver"""
    script_args = parse_script_args()
    with open("pyproject.toml", "r", encoding="utf-8") as toml_file_handle:
        pyproject = toml.load(toml_file_handle)
    print(pyproject[script_args.group][script_args.key])


if __name__ == "__main__":
    main()
