import schedule
import time
from telegram import Bot
import config

TOKEN = str(config.TOKEN)
GROUP_ID = str(config.GROUP_ID)

bot = Bot(token=str(TOKEN))

def send_morning_message():
    bot.send_message(GROUP_ID, 'Доброе утро')

def send_night_message():
    bot.send_message(GROUP_ID, 'Доброй ночи')


# schedule.every().day.at("08:00").do(send_morning_message)
# schedule.every().day.at("22:00").do(send_night_message)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

send_morning_message()
time.sleep(10)
send_night_message()
