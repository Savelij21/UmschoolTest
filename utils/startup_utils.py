from aiogram import Bot
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_data.config import Config
from db.models import Base, Subject


async def get_session_maker(config: Config) -> async_sessionmaker:
    """
    Функция получения объекта сессии для работы с БД
    """

    db_engine = create_async_engine(
        url=str(config.db.dsn),
        echo=False  # config.db.is_echo
    )
    # -- test db connection
    # async with db_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    # -- init session_maker
    session_maker = async_sessionmaker(
        bind=db_engine,
        expire_on_commit=False
    )

    # -- DEV: create subjects
    # async with session_maker() as session:
    #     session.add_all([
    #         Subject(name='Математика'),
    #         Subject(name='Русский язык'),
    #         Subject(name='Литература'),
    #         Subject(name='Физика'),
    #         Subject(name='Химия'),
    #         Subject(name='Информатика'),
    #     ])
    #     await session.commit()

    return session_maker


async def set_bot_descriptions(bot: Bot, short_description: str, description: str = None) -> None:
    """
    Установка описаний бота
    """
    await bot.set_my_short_description(
        short_description=short_description,
        language_code='ru',
    )
    await bot.set_my_description(
        description=description if description else short_description,
        language_code='ru',
    )
