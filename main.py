import logging
from telegram.ext import CommandHandler, Application, MessageHandler, filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import csv
import requests
from bs4 import BeautifulSoup as b

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def start(update, context):
    reply_keyboard = [['/data', '/zodiac', '/natal'], ['/horoscope', '/compatibility']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user = update.effective_user
    new_user = True

    with open('user_data.csv', encoding="utf8") as csvfile:
        reader = list(csv.DictReader(csvfile, delimiter=';', quotechar='"'))
        for row in reader:
            if row['id'] == str(user.id):
                new_user = False

    if new_user:
        await update.message.reply_text(f'Привет, {user.first_name}! 👋\n'
                                        '\n'
                                        'Для того, чтобы использовать все возможности бота, ответьте на пару вопросов. Для этого вызовите команду /questionary.\n'
                                        'Если возникнут проблемы нажмите /help', reply_markup=markup)

    else:
        await update.message.reply_text(f'Привет, {user.first_name}! 👋\n'
                                        '\n'
                                        'Ранее вы уже использовали этот бот. Чтобы проверить свои данные вызовите команду /data\n'
                                        'Если возникнут проблемы нажмите /help', reply_markup=markup)


async def help_command(update, context):
    await update.message.reply_text('/data - посмотреть данные о себе\n'
                                    '/zodiac - узнать свой знак зодиака\n'
                                    '/horoscope - гороскоп на сегодня\n'
                                    '/natal - посмотреть свою натальную карту\n'
                                    '/compatibility - проверить совместимость с другим человеком')


async def text_handler(update, context):
    await update.message.reply_text("Введите соответствующую команду.")


def main():
    token_tgb = '7193208629:AAE4UJ5w3dlRZGVJvPe5PRNVbWzMjEClIwQ'
    application = Application.builder().token(token_tgb).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    application.run_polling()


if __name__ == '__main__':
    main()
