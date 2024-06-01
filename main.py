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
from aiogram.types import ContentType
load_dotenv()  # Load environment variables from a .env file.

# Creating a Telegram bot and dispatcher
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)
# Connecting to the SQLite database and creating a table if it doesn't exist
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
# User data and questions for adding apartment data
USER_DATA = {}
questions = [
    "Загрузите первое фото квартиры:",
    "Загрузите второе фото квартиры:",
    "Загрузите третье фото квартиры:",
    "Введите описание квартиры:",
    "Введите цену:"
]

# Start message handler
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    USER_DATA.clear()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        keyboard.row("Админ-панель", "🛍Каталог")
        keyboard.row("Наш сайт")
    else:
        keyboard.add("🛍Каталог")
        keyboard.add("Наш сайт")
        keyboard.row("☎️Контакты")

    me = await bot.get_me()
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!\n"
                         f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
                         parse_mode='html', reply_markup=keyboard)

# Admin panel message handler


@dp.message_handler(lambda message: message.text == "Админ-панель")
async def admin_panel_handler(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Добавить данные")
        await message.answer("Добро пожаловать в админ-панель!", reply_markup=keyboard)

# Add data message handler
@dp.message_handler(lambda message: message.text == "Добавить данные")
async def add_data_handler(message: types.Message):
    await ask_next_question(message)

# Catalog message handler
@dp.message_handler(lambda message: message.text == "🛍Каталог")
async def get_apartment_data_handler(message: types.Message):
    await get_next_apartment_data(message)

# Website message handler
@dp.message_handler(text='Наш сайт')
async def website(message: types.Message):
    await message.answer('Сожалею, но у нас пока нет сайта')

# Contacts message handler
@dp.message_handler(text='☎️ Контакты')
async def call(message: types.Message):
    await message.answer('Наш телефон: 8-901-133-00-00')

# Asking next question function
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

# Photo message handler
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    if 'current_question' in USER_DATA:
        file_id = message.photo[-1].file_id
        USER_DATA[USER_DATA['current_question']] = file_id
        del USER_DATA['current_question']
        await ask_next_question(message)

# Add apartment message handler


@dp.message_handler()
async def add_apartment(message: types.Message):
    answer = message.text
    if 'current_question' in USER_DATA:
        USER_DATA[USER_DATA['current_question']] = answer
        del USER_DATA['current_question']
        await ask_next_question(message)

# Save apartment data function


async def save_apartment_data(message: types.Message):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [
        current_date,
        USER_DATA.get(questions[0], ""),
        USER_DATA.get(questions[1], ""),
        USER_DATA.get(questions[2], ""),
        USER_DATA.get(questions[3], ""),
        USER_DATA.get(questions[4], "")
    ]
    cursor.execute("INSERT INTO catalog (date, photo1, photo2, photo3, description, price) VALUES (?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    await message.answer("Данные о квартире успешно сохранены!")

# Get next apartment data function

async def get_next_apartment_data(message: types.Message):
    conn = sqlite3.connect('catalog.db')
    cursor.execute("SELECT * FROM catalog")
    data = cursor.fetchall()

    index = USER_DATA.get('apartment_index', 0)
    if index < len(data):
        record = data[index]

        photos_info = []
        for i in range(2, 5):
            photo_id = record[i]
            photos_info.append(types.InputMediaPhoto(media=photo_id, caption=f"Фото квартиры"))

        description = record[5]
        price = record[6]

        message_text = f"Описание квартиры: {description}\nЦена: {price}"

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("◀ Пред.", callback_data="prev"), InlineKeyboardButton("💳Оплатить", callback_data="pay"), InlineKeyboardButton("След. ▶", callback_data="next"))

        await bot.send_media_group(message.chat.id, media=photos_info)
        await message.answer(message_text, reply_markup=keyboard)

        USER_DATA['apartment_index'] = index

# Previous apartment callback query handler

@dp.callback_query_handler(text="prev")
async def prev_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        USER_DATA['apartment_index'] = max(index - 1, 0)
        await get_next_apartment_data(callback_query.message)

# Next apartment callback query handler
@dp.callback_query_handler(text="next")
async def next_apartment(callback_query: types.CallbackQuery):
    if 'apartment_index' in USER_DATA:
        index = USER_DATA['apartment_index']
        conn = sqlite3.connect('catalog.db')
        cursor.execute("SELECT COUNT(*) FROM catalog")
        total_records = cursor.fetchone()[0]
        USER_DATA['apartment_index'] = min(index + 1, total_records - 1)
        await get_next_apartment_data(callback_query.message)

# Pay for apartment callback query handler
@dp.callback_query_handler(text="pay")
async def pay_for_apartment(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    title = "Аренда квартиры"
    description = "Аренда квартиры"
    invoice_payload = "month_sub"
    provider_token = os.getenv('PAYMENTS_TOKEN')
    currency = "RUB"
    prices = [types.LabeledPrice(label='Subscription', amount=3000*100)]

    await bot.send_invoice(chat_id=chat_id,
                           title=title,
                           description=description,
                           payload=invoice_payload,
                           provider_token=provider_token,
                           currency=currency,
                           prices=prices)

# Pre-checkout query handler
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# Successful payment handler
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
# Starting the polling loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())
