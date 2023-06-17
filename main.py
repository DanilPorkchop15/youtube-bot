from pytube import YouTube
import os
import telebot

bot = telebot.TeleBot(***) # your telegram bot API


def download_mp3(x):
    yt = YouTube(x)
    audio = yt.streams.filter(only_audio=True).first()
    audio_file = audio.download()
    os.rename(audio_file, 'audio.mp3')


def download_mp4(x):
    yt = YouTube(x)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video_file = video.download()
    os.rename(video_file, 'video.mp4')


@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, 'Отправь ссылку на видео с ютуба')


@bot.message_handler(commands=["help"])
def help_command(m):
    bot.send_message(m.chat.id,
                     '1. Попробуй заново отправить ссылку.\n\n2. Попробуй выбрать расширение (используй команды /mp3 или /mp4 (альт - /MP3 или /MP4)), если ссылка уже отправлена.\n\n3. Сообщение с командой /help появляется после любого твоего сообщения, не соответствующего функционалу бота')


@bot.message_handler(commands=["mp3", "MP3"])
def mp3(m):
    audio_path = os.path.abspath('audio.mp3')
    with open(audio_path, 'rb') as f:
        bot.send_audio(m.from_user.id, f)


@bot.message_handler(commands=["mp4", "MP4"])
def mp4(m):
    video_path = os.path.abspath('video.mp4')
    with open(video_path, 'rb') as f:
        bot.send_video(m.chat.id, f)


@bot.message_handler(content_types=['text'], )
def msg(m):
    yt_link = m.text[8:]
    if ('youtube.com' in m.text) or ('youtu.be' in m.text):
        bot.send_message(m.chat.id, 'Немного подожди... идет скачивание данных')
        download_mp3(yt_link)
        download_mp4(yt_link)
        bot.send_message(m.chat.id, 'Выбери формат скачивания (/mp3 или /mp4) и отправь сообщение с ним')
    else:
        bot.send_message(m.chat.id, 'Что-то пошло не так?\n/help <= нажмите')


bot.polling(non_stop=True)
