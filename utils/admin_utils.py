from typing import List
import requests
from aiogram import Bot
from config_data.config import TgBot


def send_msg_to_admins_by_api(config_tg_bot: TgBot, text: str = '') -> None:
    """
    Отправка сообщения всем админам бота через API телеграмма, если бот в aiogram упал
    """
    for admin_id in config_tg_bot.admin_ids:
        requests.post(
            url=f'https://api.telegram.org/bot{config_tg_bot.token}/sendMessage',
            data={
                'chat_id': admin_id,
                'text': text,
                'parse_mode': 'HTML'
            }
        )


async def send_bot_started_msg_to_admins(bot: Bot, admins_ids: List[int]) -> None:
    """
    Отправка сообщения всем админам бота через aiogram, что бот запущен
    """
    bot_info = await bot.get_me()
    for admin_id in admins_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=f'Admin 👨🏻‍💼:\n\n'
                 f'🚀 Бот <b>{bot_info.first_name}</b> успешно запущен! 🚀'
        )


