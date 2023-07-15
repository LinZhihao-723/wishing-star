import argparse
import asyncio
import discord
import logging
import logging.handlers
import pathlib
import sys
import yaml

from typing import Any, Dict, List, Optional
from wishing_star.WishingStarClient import WishingStar, WishingStarCog

"""
Global logger
"""
logger: logging.Logger


def logger_init(log_file_path_str: Optional[str], log_level: int) -> None:
    """
    Initializes the global logger with the given log level.

    :param log_file_path_str: Path to store the log files. If None is given,
        logs will be written into stdout.
    :param log_level: Target log level.
    """
    global logger
    logger_handler: logging.Handler
    if log_file_path_str is not None:
        log_file_path: pathlib.Path = pathlib.Path(log_file_path_str).resolve()
        if log_file_path.is_dir():
            log_file_path /= "wishing_star.log"
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        logger_handler = logging.handlers.RotatingFileHandler(
            filename=log_file_path, maxBytes=1024 * 1024 * 8, backupCount=7
        )
    else:
        logger_handler = logging.StreamHandler(sys.stdout)

    logger = logging.getLogger("wishing_star")
    logger.setLevel(log_level)
    logging_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    logger_handler.setFormatter(logging_formatter)
    logger_handler.setLevel(log_level)
    logger.addHandler(logger_handler)


def main(argv: List[str]) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Execution Arguments")
    parser.add_argument(
        "--credential",
        required=True,
        help="The path to a yml config file that contains necessary credentials.",
    )
    parser.add_argument(
        "--config",
        required=True,
        help="The path to yml config file that contains customized user settings.",
    )
    parser.parse_args(argv[1:])
    args: argparse.Namespace = parser.parse_args(argv[1:])

    try:
        logger_init("./logs/", logging.INFO)
    except:
        raise

    credential: Dict[str, Any]
    credential_path_str: str = args.credential
    config: Dict[str, Any]
    config_path_str: str = args.config
    try:
        credential_path: pathlib.Path = pathlib.Path(credential_path_str).resolve()
        with open(credential_path, "r") as f:
            credential = yaml.safe_load(f)
        config_path: pathlib.Path = pathlib.Path(config_path_str).resolve()
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except Exception:
        print(f"Failed to load the credential file from '{credential_path}'.")
        raise

    intents: discord.Intents = discord.Intents.default()
    intents.message_content = True
    wishing_star: WishingStar = WishingStar(
        command_prefix="?", logger=logger, credential=credential, config=config, intents=intents
    )

    try:
        asyncio.run(wishing_star.add_cog(WishingStarCog(wishing_star)))
        wishing_star.serve()
        return 0
    except Exception as e:
        logger.error(f"Exiting on error. Error message: {e}")
        return -1
