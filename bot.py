import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from datetime import datetime
import logging
import config

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Замените 'YOUR_TOKEN' на ваш токен
API_TOKEN = config.TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ID группы, куда будут отправляться сообщения
GROUP_ID = -1001234567890  # Замените на ваш ID группы

async def send_morning_message():
    """ 
    Функция для отправки сообщения "Доброе утро"
    """
    while True:
        now = datetime.now()
        if now.hour == 8 and now.minute == 0:  # Время отправки "Доброе утро"
            await bot.send_message(GROUP_ID, "Доброе утро!")
            await asyncio.sleep(60)  # Ждем минуту перед следующей проверкой
        await asyncio.sleep(30)  # Проверяем каждые 30 секунд

async def send_night_message():
    """
    Функция для отправки сообщения "Спокойной ночи"
    """
    while True:
        now = datetime.now()
        if now.hour == 22 and now.minute == 0:  # Время отправки "Спокойной ночи"
            await bot.send_message(GROUP_ID, "Спокойной ночи!")
            await asyncio.sleep(60)  # Ждем минуту перед следующей проверкой
        await asyncio.sleep(30)  # Проверяем каждые 30 секунд

@dp.on_startup()
async def on_startup(_):
    asyncio.create_task(send_morning_message())
    asyncio.create_task(send_night_message())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
