'''
This bot make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 28/05/2024
Ending //

'''
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')


class NewOrder(StatesGroup):
    type = State()
    address = State()
    description = State()
    price = State()
    video = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    me = await bot.get_me()
    await message.answer(f"Здравствуйте, {message.from_user.first_name}!\n"
                         f"Меня зовут {me.first_name}. Я помогу вам арендовать квартиру.",
                         parse_mode='html', reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы авторизовались как администратор!', reply_markup=kb.main_admin)


@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')


@dp.message_handler(text='🛍Каталог')
async def catalog(message: types.Message):
    await message.answer('Выберите категорию', reply_markup=kb.catalog_list)


@dp.message_handler(text='☎️Контакты')
async def contacts(message: types.Message):
    await message.answer('Наш телефон: 8-901-133-00-00')


@dp.message_handler(text='🌐Наш сайт')
async def website(message: types.Message):
    await message.answer('Сожалею, но у нас пока нет сайта')


@dp.message_handler(text='🛠️Админ-панель')
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы вошли в админ-панель', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.message_handler(text='Добавить товар')
async def add_apartment(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer('Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я тебя не понимаю.')


@dp.callback_query_handler(state=NewOrder.type)
async def add_apartment_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите адрес квартиры', reply_markup=kb.cancel)
    await NewOrder.next()


@dp.message_handler(state=NewOrder.address)
async def add_apartment_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await message.answer('Введите описание квартиры')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.description)
async def add_apartment_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer('Введите цену(в сутки)')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.price)
async def add_apartment_price(message: types.Message, state: FSMContext):    
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте видео квартиры')
    await NewOrder.next()


@dp.message_handler(lambda message: message.video is None, state=NewOrder.video)
async def add_apartment_video_check(message: types.Message):
    await message.answer('Это не видео!')


@dp.message_handler(content_types=['video'], state=NewOrder.video)
async def add_apartment_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['video'] = message.video.file_id
    await db.add_apartment(state)
    await message.answer('Квартира успешно добавлена!', reply_markup=kb.admin_panel)
    await state.finish()


@dp.callback_query_handler()
async def callback_query_viewing_atelier(callback_query: types.CallbackQuery):
    if callback_query.data == 'atelier':
        apartment = await db.get_apartment_by_type('atelier')
        if apartment:
            apartment = apartment[0]
            video = apartment[4]
            caption = f"Адрес: {apartment[1]}\nОписание: {apartment[2]}\nЦена: {apartment[3]}"
            await bot.send_video(chat_id=callback_query.from_user.id, video=video, caption=caption, reply_markup=kb.product_list)
# Starting the polling loop
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)