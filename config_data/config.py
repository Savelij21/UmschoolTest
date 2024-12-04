from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Callable
import logging
from logging.handlers import RotatingFileHandler
import os
from pydantic import PostgresDsn, BaseModel


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


class DbConfig(BaseModel):
    dsn: PostgresDsn
    is_echo: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    setup_logging: Callable[[str], None]
    env: str


# logging
def setup_logging(logs_dir_path: str = './logs') -> None:
    # Конфиг для логирования
    if not os.path.exists(logs_dir_path):
        os.mkdir(logs_dir_path)

    # Формат логов
    log_format = '[%(asctime)s] [%(levelname)s] - %(name)s - %(message)s (%(filename)s:%(lineno)d)'

    # Хэндлеры для общего лога
    common_file_handler = RotatingFileHandler(
        filename=os.path.join(logs_dir_path, 'bot.log'),
        maxBytes=16 * 1024 * 1024,  # 16 MB
        backupCount=5,
        encoding='utf-8'
    )
    common_file_handler.setLevel(logging.INFO)

    # Хэндлер для вывода логов в консоль
    console_stream_handler = logging.StreamHandler()
    console_stream_handler.setLevel(logging.INFO)

    # Хэндлер для логов ошибок
    error_file_handler = RotatingFileHandler(
        filename=os.path.join(logs_dir_path, 'error.log'),
        maxBytes=16 * 1024 * 1024,  # 16 MB
        backupCount=5,
        encoding='utf-8'
    )
    error_file_handler.setLevel(logging.ERROR)

    # Итоговый конфиг
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            common_file_handler,
            console_stream_handler,
            error_file_handler
        ]
    )

    # Для asyncio логов даем уровень только ERROR, а то спамит предупреждениями
    logging.getLogger('asyncio').setLevel(logging.ERROR)


# config
def load_config(path: str | None = None) -> Config:
    load_dotenv(path)

    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN'),
            admin_ids=[int(id_.strip()) for id_ in os.getenv('ADMIN_IDS').split(',')]
        ),
        db=DbConfig(
            dsn=os.getenv('DATABASE_URL'),
            is_echo=True
        ),
        setup_logging=setup_logging,
        env=os.getenv('ENV')
    )

