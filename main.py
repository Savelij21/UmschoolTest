import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import Config, load_config
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from middlewares.middlewares import InnerLogHandlerMiddleware, PrepareUpdateMiddleware
from utils.admin_utils import send_msg_to_admins_by_api
from utils.startup_utils import get_session_maker, set_bot_descriptions


logger = logging.getLogger(__name__)


async def main() -> None:

    # 1. Конфиг бота
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
    # -- DB session maker
    session_maker = await get_session_maker(config)
    # -- dp
    dp = Dispatcher(
        storage=MemoryStorage(),
        session_maker=session_maker
    )
    # -- Настраиваем главное меню бота
    await set_main_menu(bot)
    # -- Полное, краткое описания бота
    await set_bot_descriptions(bot, 'UmschoolTest бот для хранения твоих результатов ЕГЭ!')

    # 2. Middlewares
    # -- prepare update for inner log
    dp.update.outer_middleware(PrepareUpdateMiddleware())
    # -- log all new updates (total 22 types)
    dp.update.middleware(InnerLogHandlerMiddleware())

    # 3. Routers
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # 4. Start
    # -- clear old updates
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        # START POLLING
        await dp.start_polling(bot)

    except Exception as ex:
        send_msg_to_admins_by_api(
            config_tg_bot=config.tg_bot,
            text=f'Admin 👨🏻‍💼:\n\n⭕️ <b>Ошибка запуска бота</b>:\n\n{str(ex)}'
        )
        logger.error(f'[Bot Starting Error] - {ex}', exc_info=True)
        raise

    finally:
        await bot.session.close()


if __name__ == "__main__":

    config: Config = load_config()
    stop_text = '✅ Плановое отключение бота'
    try:
        # DEV: для асинхронной работы psycopg на Windows
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # добавление main в цикл событий
        asyncio.run(main())

    except Exception as ex:
        stop_text = f'<b>Ошибка</b>:\n\n{str(ex)}'
        logger.error(f'[Bot Fatal Error] - {ex}', exc_info=True)

    finally:
        send_msg_to_admins_by_api(
            config_tg_bot=config.tg_bot,
            text=f'Admin 👨🏻‍💼:\n\n⛔️ Бот <b>UmschoolTest</b> остановлен! ⛔️\n\n{stop_text}'
        )
        logger.warning(f'!!! Bot stopped !!!')

