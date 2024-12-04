from typing import List
import requests
from aiogram import Bot


def send_msg_to_admins_by_api(bot_token: str, admins_ids: List[int], text: str = '') -> None:
    for admin_id in admins_ids:
        requests.post(
            url=f'https://api.telegram.org/bot{bot_token}/sendMessage',
            data={
                'chat_id': admin_id,
                'text': text,
                'parse_mode': 'HTML'
            }
        )


async def send_bot_started_msg_to_admins(bot: Bot, admins_ids: List[int]) -> None:
    bot_info = await bot.get_me()
    for admin_id in admins_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=f'Admin 👨🏻‍💼:\n\n'
                 f'🚀 Бот <b>{bot_info.first_name}</b> успешно запущен! 🚀'
        )


