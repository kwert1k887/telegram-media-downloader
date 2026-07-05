"""Telegram Media Downloader — скачивание медиафайлов из Telegram-каналов."""

import asyncio
import os
import sys

from loguru import logger
from telegram_channel_duplicator.duplicator_download import Duplicator


async def main():
    logger.remove()
    logger.add(
        sys.stderr,
        format="<cyan>{time}</cyan> | <lvl>{level}</lvl> - <lvl>{message}</lvl>",
        colorize=True,
        level="DEBUG",
    )
    logger.add(
        os.path.join("logs", "debug.log"),
        format="{time} {level} {message}",
        level="DEBUG",
        rotation="3mb",
        compression="zip",
    )

    logger.info("Telegram Media Downloader запущен")

    duplicator = Duplicator()
    await duplicator.start()


if __name__ == "__main__":
    asyncio.run(main())
