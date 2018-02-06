from os import environ
from os.path import join, dirname
import math
import time
import pickle
from threading import Thread

from dotenv import load_dotenv
import pendulum
import telebot
import schedule

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

bot = telebot.TeleBot(environ.get('TELEGRAM_TOKEN'))


def make_progress_string(percent):
    blocks = 16
    percent = percent * blocks / 100
    return ''.join(["▓" if i < percent else "░" for i in range(blocks)])


def get_year_progress():
    dt = pendulum.now()
    year_days = 366 if dt.is_leap_year() else 365
    passed_days = dt.timetuple().tm_yday
    percent = math.floor((passed_days / year_days) * 100)
    print(percent)
    return percent


def send_message(percent):
    year_progress = make_progress_string(percent)
    text = f'Day: {year_progress} {percent}'
    bot.send_message(chat_id='@year_progress', text=text)


def check():
    with open('progress.pkl', 'rb') as f:
        old_progress = pickle.load(f)
    current_progress = get_year_progress()
    if old_progress != current_progress:
        with open('progress.pkl', 'wb') as f:
            pickle.dump(current_progress, f)
        send_message(current_progress)

schedule.every().day.at("07:00").do(check)


def event_loopy():
    while True:
        schedule.run_pending()
        time.sleep(1)

Thread(target=event_loopy).start()

if __name__ == '__main__':
    bot.polling(none_stop=True)
