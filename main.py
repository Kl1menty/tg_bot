import logging
from telegram.ext import CommandHandler, Application, MessageHandler, filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import csv
import requests
from bs4 import BeautifulSoup as b

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def date_to_zodiac(date):
    day, month, year = map(int, date.split('.'))

    if (month == 1 and day >= 21) or (month == 2 and day <= 20):
        return "Водолей"

    elif (month == 2 and day >= 21) or (month == 3 and day <= 20):
        return "Рыбы"

    elif (month == 3 and day >= 21) or (month == 4 and day <= 20):
        return "Овен"

    elif (month == 4 and day >= 21) or (month == 5 and day <= 20):
        return "Телец"

    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "Близнецы"

    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "Рак"

    elif (month == 7 and day >= 23) or (month == 8 and day <= 23):
        return "Лев"

    elif (month == 8 and day >= 24) or (month == 9 and day <= 23):
        return "Дева"

    elif (month == 9 and day >= 24) or (month == 10 and day <= 23):
        return "Весы"

    elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
        return "Скорпион"

    elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
        return "Стрелец"

    elif (month == 12 and day >= 22) or (month == 1 and day <= 20):
        return "Козерог"


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


async def questionary(update, context):
    await update.message.reply_text("Опрос начался, для досрочного завершения вызовите /stop")
    await update.message.reply_text("Какой у вас пол?(м/ж)")
    return 1


gender = ''


async def first_response(update, context):
    global gender
    mes = update.message.text.lower()

    if mes in ['м', 'ж']:
        gender = mes
        await update.message.reply_text("Введите свою дату рождения\n"
                                        "Пример: 23.04.2024")
        return 2

    else:
        await update.message.reply_text("Внимательно посмотрите пример и попробуйте еще раз")
        return 1


async def second_response(update, context):
    user = update.effective_user
    mes = update.message.text

    try:
        day, month, year = [int(i) for i in mes.split('.')]

        if day in range(1, 32) and month in range(1, 13) and year in range(1900, 2025):
            with open('user_data.csv', 'r', encoding="utf8") as csvfile:
                reader = list(csv.DictReader(csvfile, delimiter=';', quotechar='"'))

            if str(user.id) in [i['id'] for i in reader]:
                for i in range(len(reader)):
                    if reader[i]['id'] == str(user.id):
                        reader[i] = {
                            'id': user.id,
                            'user_name': user.username,
                            'gender': gender,
                            'date': mes,
                            'zodiac': date_to_zodiac(mes)
                        }
                with open('user_data.csv', 'w', newline='', encoding="utf8") as csvfile:
                    writer = csv.DictWriter(csvfile,
                                            fieldnames=list(reader[0].keys()),
                                            delimiter=';',
                                            quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
                    for row in reader:
                        writer.writerow(row)
            else:
                with open('user_data.csv', 'a', newline='', encoding="utf8") as csvfile:
                    writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([user.id, user.username, gender, mes, date_to_zodiac(mes)])

            await update.message.reply_text("Спасибо! Для продолжения введите соответствующую команду.")
            return ConversationHandler.END

        else:
            await update.message.reply_text("Укажите существующую дату")
            return 2

    except:
        await update.message.reply_text("Внимательно посмотрите пример и попробуйте еще раз")
        return 2


async def stop(update, context):
    await update.message.reply_text("Опрос окончен")
    return ConversationHandler.END


async def show_data(update, context):
    user = update.effective_user

    with open('user_data.csv', 'r', encoding="utf8") as csvfile:
        reader = list(csv.DictReader(csvfile, delimiter=';', quotechar='"'))

    try:
        for person in reader:
            if person['id'] == str(user.id):
                user_data = person

        if user_data["gender"] == 'м':
            gen = 'мужской'

        elif user_data["gender"] == 'ж':
            gen = 'женский'

        await update.message.reply_text(f'Ваш пол: {gen}\n'
                                        f'Ваша дата рождения: {user_data["date"]}\n'
                                        '\n'
                                        'Если хотите изменить данные вызовете /questionary')

    except:
        await update.message.reply_text('Вы еще не заполняли данные о себе\n'
                                        'Для этого вызовите /questionary')


async def check_zodiac(update, context):
    user = update.effective_user

    with open('user_data.csv', 'r', encoding="utf8") as csvfile:
        reader = list(csv.DictReader(csvfile, delimiter=';', quotechar='"'))

    try:
        for person in reader:
            if person['id'] == str(user.id):
                user_data = person
        await update.message.reply_text(f'Ваш знак зодиака: {user_data["zodiac"]}')

    except:
        await update.message.reply_text('Вы еще не заполняли данные о себе\n'
                                        'Для этого вызовите /questionary')


def main():
    token_tgb = '7193208629:AAE4UJ5w3dlRZGVJvPe5PRNVbWzMjEClIwQ'
    application = Application.builder().token(token_tgb).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('questionary', questionary)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("data", show_data))
    application.add_handler(CommandHandler("zodiac", check_zodiac))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    application.run_polling()


if __name__ == '__main__':
    main()
