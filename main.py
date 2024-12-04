import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

from lexicon.lexicon import LEXICON
from config_data.config import Config, load_config
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from middlewares.middlewares import InnerLogHandlerMiddleware, PrepareUpdateMiddleware
from utils.admin_utils import send_msg_to_admins_by_api, send_bot_started_msg_to_admins
from db.tables import metadata


logger = logging.getLogger(__name__)


async def main() -> None:

    # Конфиг бота
    config: Config = load_config()

    # -- logging
    config.setup_logging('./logs')
    logger.info('Starting bot')

    # -- bot
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    # DB
    db_engine = create_async_engine(
        url=str(config.db.dsn),
        echo=config.db.is_echo
    )
    # -- test connection
    async with db_engine.begin() as conn:
        await conn.execute(text('SELECT 1'))

    async with db_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    # -

    # -- dp
    dp = Dispatcher(
        storage=MemoryStorage(),
        db_engine=db_engine
    )


    # Настраиваем главное меню бота
    await set_main_menu(bot)
    # await bot.delete_my_commands()

    # Полное, краткое описания бота
    await bot.set_my_description(
        description=LEXICON['description_text'],
        language_code='ru',
    )

    await bot.set_my_short_description(
        short_description=LEXICON['short_description'],
        language_code='ru',
    )

    # Middlewares
    # -- prepare update for inner log
    dp.update.outer_middleware(PrepareUpdateMiddleware())
    # -- log all new updates (total 22 types)
    update_types = [
        dp.message,
        dp.edited_message,
        dp.channel_post,
        dp.edited_channel_post,
        dp.inline_query,
        dp.chosen_inline_result,
        dp.callback_query,
        dp.shipping_query,
        dp.pre_checkout_query,
        dp.poll,
        dp.poll_answer,
        dp.my_chat_member,
        dp.chat_member,
        dp.chat_join_request,
        dp.message_reaction,
        dp.message_reaction_count,
        dp.chat_boost,
        dp.removed_chat_boost,
        # dp.deleted_business_messages,
        # dp.business_connection,
        # dp.edited_business_message,
        # dp.business_message,
    ]
    for update_type in update_types:
        update_type.middleware(InnerLogHandlerMiddleware())

    # Routers
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Start
    # -- clear old updates
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        # start
        await dp.start_polling(bot)
    except Exception as ex:
        send_msg_to_admins_by_api(
            bot_token=config.tg_bot.token,
            admins_ids=config.tg_bot.admin_ids,
            text=f'Admin 👨🏻‍💼:\n\n'
                 f'⭕️ <b>Ошибка запуска бота</b>:\n\n{str(ex)}'
        )
        logger.error(f'[Bot Starting Error] - {ex}', exc_info=True)
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":

    config: Config = load_config()
    stop_text = '✅ Плановое отключение бота'
    try:
        # для асинхронной работы psycopg на Windows
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # добавление main в цикл событий
        asyncio.run(main())
    except Exception as ex:
        stop_text = f'<b>Ошибка</b>:\n\n{str(ex)}'
        logger.error(f'[Bot Fatal Error] - {ex}', exc_info=True)
    finally:
        send_msg_to_admins_by_api(
            bot_token=config.tg_bot.token,
            admins_ids=config.tg_bot.admin_ids,
            text=f'Admin 👨🏻‍💼:\n\n'
                 f'⛔️ Бот <b>UmschoolTest</b> остановлен! ⛔️\n\n'
                 f'{stop_text}'
        )
        logger.warning(f'!!! Bot stopped !!!')

