'''
This bot make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 28/05/2024
Ending //

'''
# Installing the necessary libraries
import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
import datetime
import math
load_dotenv()  # Load environment variables from a .env file.


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

conn = sqlite3.connect('catalog.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS catalog
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               date VARCHAR(50),
               photo1 VARCHAR(50),
               photo2 VARCHAR(50),
               photo3 VARCHAR(50),
               description VARCHAR(50),
               price VARCHAR(50))''')
conn.commit()

USER_DATA = {}
questions = [
    "Загрузите первое фото квартиры:",
    "Загрузите второе фото квартиры:",
    "Загрузите третье фото квартиры:",
    "Введите описание квартиры:",
    "Введите цену:"
]

PAGE_SIZE = 1  # Количество записей на странице
CURRENT_PAGE = 0

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    USER_DATA.clear()
    await message.answer("Привет! Я помогу вам арендовать квартиру. Используйте /catalog для просмотра каталога.")

@dp.message_handler(commands=['catalog'])
async def show_catalog(message: types.Message):
    global CURRENT_PAGE
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM catalog LIMIT ? OFFSET ?", (PAGE_SIZE, CURRENT_PAGE * PAGE_SIZE))
    data = cursor.fetchall()

    if data:
        for record in data:
            photos_info = []
            for i in range(2, 5):
                photo_id = record[i]
                photos_info.append(types.InputMediaPhoto(media=photo_id, caption="Фото квартиры"))

            description = record[5]
            price = record[6]

            message_text = f"Описание квартиры: {description}\nЦена: {price}"

            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Предыдущая", callback_data="prev"), InlineKeyboardButton("Следующая", callback_data="next"))

            await bot.send_media_group(message.chat.id, media=photos_info)
            await message.answer(message_text, reply_markup=keyboard)

    else:
        await message.answer("В каталоге больше нет записей.")

@dp.callback_query_handler(text="prev")
async def prev_page(callback_query: types.CallbackQuery):
    global CURRENT_PAGE
    if CURRENT_PAGE > 0:
        CURRENT_PAGE -= 1
    await show_catalog(callback_query.message)

@dp.callback_query_handler(text="next")
async def next_page(callback_query: types.CallbackQuery):
    global CURRENT_PAGE
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM catalog")
    total_records = cursor.fetchone()[0]
    total_pages = (total_records + PAGE_SIZE - 1) // PAGE_SIZE

    if CURRENT_PAGE < total_pages - 1:
        CURRENT_PAGE += 1

    await show_catalog(callback_query.message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())