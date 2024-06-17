from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('🛍Каталог').add('☎️Контакты').add('🌐Наш сайт')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('🛍Каталог').add('☎️Контакты').add('🛠️Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар')

catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='1 комнатная квартира', callback_data='1-room apartment'),
                 InlineKeyboardButton(text='2 х комнатная квартира', callback_data='2-room apartment'),
                 InlineKeyboardButton(text='3 х комнатная квартира', callback_data='3-room apartment'),
                 InlineKeyboardButton(text='Студия', callback_data='atelier'),
                 )
cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')

product_list = InlineKeyboardMarkup(row_width=2)
product_list.row(InlineKeyboardButton(text='◀ Пред.', callback_data='previous_apartment'),
                 InlineKeyboardButton(text='Выбрать✅', callback_data='1-room apartment'),
                 InlineKeyboardButton(text='След. ▶', callback_data='next_apartment'),
                 )
pay_list = InlineKeyboardMarkup(row_width=2)
pay_list.row(InlineKeyboardButton(text='+1', callback_data='2-room apartment'),
             InlineKeyboardButton(text='💳Оплатить', callback_data='1-room apartment'),
             InlineKeyboardButton(text='-1', callback_data='3-room apartment'),
             )
