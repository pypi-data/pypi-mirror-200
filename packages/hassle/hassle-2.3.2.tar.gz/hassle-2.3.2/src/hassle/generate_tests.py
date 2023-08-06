import argparse
import os
import tokenize
from pathlib import Path

root = Path(__file__).parent


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "package_name",
        type=str,
        default=".",
        nargs="?",
        help=""" The name of the package or project to generate tests for,
        assuming it's a subfolder of your current working directory.
        Can also be a full path to the package. If nothing is given,
        the current working directory will be used.""",
    )

    args = parser.parse_args()

    return args


def get_function_names(filepath: Path) -> list[str]:
    """Returns a list of function names from a .py file."""
    with filepath.open("r") as file:
        tokens = list(tokenize.generate_tokens(file.readline))
    functions = []
    for i, token in enumerate(tokens):
        # If token.type is "name" and the preceeding token is "def"
        if (
            token.type == 1
            and tokens[i - 1].type == 1
            and tokens[i - 1].string == "def"
        ):
            functions.append(token.string)
    return functions


def write_placeholders(package_path: Path, pyfile: Path | str, functions: list[str]):
    """Write placeholder functions to the
    tests/test_{pyfile} file if they don't already exist.
    The placeholder functions use the naming convention
    test__{pyfile.name}__{function_name}

    :param package_path: Path to the package.

    :param pyfile: Path to the pyfile to write placeholders for.

    :param functions: List of functions to generate
    placehodlers for."""
    package_name = package_path.stem
    tests_dir = package_path / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    pyfile = Path(pyfile)
    test_file = tests_dir / f"test_{pyfile.name}"
    # Makes sure not to overwrite previously written tests
    # or additional imports.
    if test_file.exists():
        content = test_file.read_text() + "\n\n"
    else:
        content = f"import pytest\nfrom {package_name} import {pyfile.stem}\n\n\n"
    for function in functions:
        test_function = f"def test__{pyfile.stem}__{function}"
        if test_function not in content and function != "__init__":
            content += f"{test_function}():\n    ...\n\n\n"
    test_file.write_text(content)
    os.system(f"black {tests_dir}")
    os.system(f"isort {tests_dir}")


def generate_test_files(package_path: Path):
    """Generate test files for all .py files in 'src'
    directory of 'package_path'."""
    pyfiles = [
        file
        for file in (package_path / "src").rglob("*.py")
        if file.name != "__init__.py"
    ]
    for pyfile in pyfiles:
        write_placeholders(package_path, pyfile, get_function_names(pyfile))


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()
    package_path = Path(args.package_name).resolve()
    generate_test_files(package_path)


if __name__ == "__main__":
    main(get_args())
