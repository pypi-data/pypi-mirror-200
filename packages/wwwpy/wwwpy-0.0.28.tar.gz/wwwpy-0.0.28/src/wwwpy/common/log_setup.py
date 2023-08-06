from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def getLoggerFor(file):
    return logging.getLogger(os.path.basename(file))


logger = getLoggerFor(__file__)


@dataclass(frozen=True)
class LogConfig:
    when: str = 'midnight'
    interval: int = 1
    backup_count: int = 90
    format: str = "%(asctime)s [%(threadName)-12.12s] %(levelname)-5.5s %(name)s - %(message)s"


default = LogConfig()


def setup_logging(log_folder: str | Path, config: LogConfig = default):
    log_folder = Path(log_folder)
    log_folder.mkdir(exist_ok=True, parents=True)
    logging.basicConfig(
        level=logging.INFO,
        format=config.format,
        handlers=[TimedRotatingFileHandler(
            log_folder / "app-log",
            when=config.when,
            interval=config.interval,
            backupCount=config.backup_count),
            logging.StreamHandler()
        ]
    )
    logger.info(f'Starting logging in folder {log_folder}')
    logger.info(f'Working directory: {os.getcwd()}')
