'''
This bot make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 28/05/2024
Ending //

'''
# Installing the necessary libraries
import os
import sqlite3
import datetime
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file.

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS catalog
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               date VARCHAR(50),
              photo VARCHAR(50),
               description VARCHAR(50),
               price VARCHAR(50))''')
conn.commit()

USER_DATA = {}
questions = [
    "Загрузите фото квартиры:",
    "Введите описание квартиры:",
    "Введите цену:"
]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    USER_DATA.clear()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        keyboard.row("Админ-панель", "Каталог")
        keyboard.row("Наш сайт")
    else:
        keyboard.add("Каталог")
        keyboard.add("Наш сайт")

    me = await bot.get_me()
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!\n"
                         f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
                         parse_mode='html', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Админ-панель")
async def admin_panel_handler(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Добавить данные")
        await message.answer("Добро пожаловать в админ-панель!", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Добавить данные")
async def add_data_handler(message: types.Message):
    await ask_next_question(message)

@dp.message_handler(lambda message: message.text == "Каталог")
async def get_apartment_data_handler(message: types.Message):
    await get_apartment_data(message)

async def ask_next_question(message: types.Message):
    if len(USER_DATA) < len(questions):
        question = questions[len(USER_DATA)]
        if question.startswith("Загрузите фото"):
            await message.answer(question, parse_mode="html")
        else:
            await message.answer(question)
        USER_DATA['current_question'] = question
    else:
        await save_apartment_data(message)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    if 'current_question' in USER_DATA:
        file_id = message.photo[-1].file_id
        USER_DATA[USER_DATA['current_question']] = file_id
        del USER_DATA['current_question']
        await ask_next_question(message)

@dp.message_handler()
async def add_apartment(message: types.Message):
    answer = message.text
    if 'current_question' in USER_DATA:
        USER_DATA[USER_DATA['current_question']] = answer
        del USER_DATA['current_question']
        await ask_next_question(message)

async def save_apartment_data(message: types.Message):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [current_date, USER_DATA.get(questions[0], ""), USER_DATA.get(questions[1], ""), USER_DATA.get(questions[2], "")]
    cursor.execute("INSERT INTO catalog (date, photo, description, price) VALUES (?, ?, ?, ?)", data)
    conn.commit()
    await message.answer("Данные о квартире успешно сохранены!")

async def get_apartment_data(message: types.Message):
    conn = sqlite3.connect('catalog.db')
    cursor.execute("SELECT * FROM catalog")
    data = cursor.fetchall()
    conn.close()

    for record in data:
        photo_id = record[2]
        await bot.send_photo(message.chat.id, photo_id, f"Описание квартиры: {record[3]}\nЦена: {record[4]}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())