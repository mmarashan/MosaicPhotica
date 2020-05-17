import telebot
from telebot import apihelper

apihelper.proxy = {'https': 'socks5://rkn:9ophEgTa@rkn.pizd.ec:443'}
bot = telebot.TeleBot("205081013:AAGkmQbVMkCyo2iv9-oF2eaJXTZ4bsOr_aw")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello Ivan")


bot.polling()
