import argparse
from typing import List


def main(argv: List[str]) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Execution Arguments")
    parser.add_argument("--key", required=True, help="Credential keyfor the bot to log in")
    parser.parse_args(argv[1:])

    return 0
