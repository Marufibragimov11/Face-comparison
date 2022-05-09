import os
import logging
import sqlite3
from glob import glob

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
# Local files ---------------------------------------

# from db_save_pic import insertBLOB
from face_comparison import face_recog, lst
from update_coin import databased

BOT_TOKEN = "5115520546:AAE5mzr02iLXZl2rTP9YxMyL7uUVUxFX7K4"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Buttons ------------------------------------------

PHOTO, APPLICATION, RETURN = range(3)

button_text_1, button_text_2, button_text_3 = ("Rasm Yuborish", "Yengil shikoyat", "O'gir shikoyat")

reply_keyboard = [[button_text_1]]
forward_keyboard = [[button_text_2], [button_text_3]]

# -----------------------------------------------------

# Update DataBase

try:
    con = sqlite3.connect('Second.db')
    cur = con.cursor()
    # print("Connected to SQLite")
    cur.execute("""SELECT students_2.id, students_2.first_name, students_2.directory, wallets.amount 
                   FROM students_2 LEFT JOIN wallets ON students_2.id = wallets.wallet_id""")
    rows = cur.fetchall()
    # print(rows[0][3])
    con.commit()
    cur.close()

except sqlite3.Error as error:
    # print("Failed to insert blob data into sqlite table", error)
    print(error)
finally:
    if con:
        con.close()
        # print("the sqlite connection is closed")


# ------------------------------------------------------


def start(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user

    update.message.reply_html(
        "Assalomu Aleykum <b>{}!</b>\n "
        "\n<b>Qoida buzgan o'quvchining rasmini yuboring</b>\n"
        "\n<b>Undan AstroCoin ayrib tashlimiz </b>".
            format(user.first_name),
        # reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True),
    )
    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(f'db_images\{user.first_name}.jpg')
    logger.info("Photo of %s: %s", user.first_name, f'db_images\{user.first_name}.jpg')
    update.message.reply_text(
        'O\'quvchining ma\'lumotlari qidirilmoqda. Iltimos kutib turing...',
    )
    # insertBLOB(user.first_name, f'db_images\{user.first_name}.jpg', user.id)
    face_recog()
    print(lst[0][0])
    # print(type(lst))
    update.message.reply_text(
        "🎓Student ma'lumotlari topildi.👇\n"
        f"   👨‍🎓Ismi: {lst[0][1]} \n"
        f"   👨‍🎓Familiyasi: {lst[0][2]} \n"
        f"   👨‍💻Yo'nalishi: {lst[0][3]} \n",
        # f"AstroCoin: {rows[0][4]}",
        # f"ID: {lst[0][0]}",
        reply_markup=ReplyKeyboardMarkup(forward_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    f_n = glob('db_images/*')
    os.remove(f_n[0])
    # lst.clear()
    return APPLICATION


def application(update: Update, context: CallbackContext):
    # chat_id = update.message.chat_id
    # message_id = update.message.message_id
    text = update.message.text
    user = update.message.from_user
    print(text)

    # Bot ga ma'lumotlarni yuborish uchun.

    if text != "Yengil shikoyat" and text != "O'gir shikoyat":
        txt = f"Mentor: {user.first_name} {user.last_name}  \n" \
              f"👨‍🎓Student: {lst[0][1]} {lst[0][2]} \n" \
              f"👨‍💻Yo'nalishi: {lst[0][3]} \n" \
              f"📝Shikoyat: {text}"
        update.message.bot.send_message("@asssalon", txt)
        lst.clear()
        start(update, context)
    elif text == "Yengil shikoyat":
        update.message.reply_text(
            text="Shikoyat yozing. Men uni Astrum CEO ga yuboraman"
        )
        for i in range(len(rows)):
            if rows[i][0] == lst[0][0]:
                summ = int(rows[0][3])
                summ -= 100
                databased(summ, lst[0][0])
    elif text == "O'gir shikoyat":
        update.message.reply_text(
            text="Shikoyat yozing. Men uni Astrum CEO ga yuboraman"
        )
        for i in range(len(rows)):
            if rows[0][0] == lst[0][0]:
                summ = int(rows[0][3])
                summ -= 500
                databased(summ, lst[0][0])
    # update.message.bot.forward_message("@asssalon", chat_id, message_id)


def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, photo)],
            APPLICATION: [
                MessageHandler(Filters.photo, photo),
                MessageHandler(Filters.update, application)
            ]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
