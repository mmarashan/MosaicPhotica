import telebot
from telebot import apihelper

from auto_post.presenter.presenter_api import Presenter, State
from auto_post.view.view_api import View

apihelper.proxy = {'https': 'socks5://rkn:9ophEgTa@rkn.pizd.ec:443'}

bot: telebot.TeleBot = None


class CustomBot(View):

    def __init__(self, token: str):
        global bot
        bot = telebot.TeleBot("205081013:AAGkmQbVMkCyo2iv9-oF2eaJXTZ4bsOr_aw")
        self.presenter: Presenter = None

        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            bot.reply_to(message, "Howdy, how are you doing?")

        @bot.message_handler(commands=['run'])
        def send_run(message):
            bot.reply_to(message, "Howdy, how are you doing?")
            #chat_id = message.chat.id
            #print("Message: {}. Chat id {}".format(message, 0))

    def __on_new_state_listener(state: State):
        pass

    def inject(self, presenter):
        assert isinstance(presenter, Presenter)
        self.presenter = presenter

    def start(self):
        bot.polling()


bot_1 = CustomBot("")
bot_1.start()
