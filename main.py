from time import sleep
import telebot
import validation
from pytube import YouTube
import os
import string
bot = telebot.TeleBot(
    token='1171061208:AAF1JWRUUloBDpVEwj2-3_3Q_VW_d1x6Dhs', 
    threaded=True,
    num_threads=300)

path_ = '\\YTDownloader\\Video'


@bot.message_handler(commands=['start'])
def start(mes):
    mess = 'Привет, я могу скачивать видео с ютуб. Просто отправь мне ссылку!'
    bot.send_message(mes.chat.id, mess)

@bot.message_handler()
def get_user_text(m):
    url = m.text
    try:
        yt = YouTube(m.text)
        VID_ID = ''
        VID_ID = validation.to_valid(url, VID_ID) #валидация регуляркой из validation.py
        if VID_ID:
            f = bot.send_message(m.chat.id, 'Начинаем загрузку видео...')
            video = yt.streams.get_highest_resolution().download(path_, yt.title.translate(str.maketrans('', '', string.punctuation)) + ".mp4")
            bot.edit_message_text('Видео успешно загрузилось... Отправка...', m.chat.id, f.message_id)
            file_path = f"\\YTDownloader\\Video\\{yt.title.translate(str.maketrans('', '', string.punctuation))}.mp4"
            videos = open(file_path, "rb")
            bot.send_video(m.chat.id, videos)
            bot.edit_message_text('Видео успешно отправлено!', m.chat.id, f.message_id)
            videos.close()
            os.remove(file_path)
    except Exception as e:
        bot.send_message(m.chat.id, f'Что-то пошло не так! Ошибка `{e}`')




bot.polling(none_stop=True)