# ApartmentRentals_bot
Данный бот представляет собой Telegram-бота, который помогает пользователям арендовать квартиры. Бот имеет две основные функции: администраторская панель и панель пользователя. <br />
# Администраторская панель:
![Снимок экрана 2024-06-01 225018](https://github.com/fetgrigory/ApartmentRentals_bot/assets/157891679/38f2077b-3a5f-46a0-b4a0-d7913a992337) <br />
![1](https://github.com/fetgrigory/ApartmentRentals_bot/assets/157891679/c17d1bfc-1327-44b0-bb92-13e3adcea8e0) <br />

- При входе в админ-панель администратору отображается возможность добавления данных.
- Администратор может загружать фотографии квартир, вводить описания и цены.
- Данные о квартирах сохраняются в базе данных SQLite.
  # Пользовательская панель:
  ![2](https://github.com/fetgrigory/ApartmentRentals_bot/assets/157891679/9b461917-56c9-43b8-a410-d42227c26504) <br />

- В каталоге квартир вы сможете просматривать доступные квартиры, просматривать фотографии, описание и цены квартир, а также оплачивать аренду фотографий через инлайн-оплату.
- Вы можете использовать кнопки "◀ Пред.", "След. ▶" для просмотра предыдущей и следующей квартиры соответственно, а также "💳Оплатить" для оплаты аренды.
![3](https://github.com/fetgrigory/ApartmentRentals_bot/assets/157891679/bfcdbd7e-381e-46c8-9392-5c9a751b0214)

 # Система оплаты PayMaster:
- В боте реализована интеграция с платежной системой PayMaster для удобной и безопасной оплаты аренды квартиры.
- Пользователи могут нажать на кнопку "💳Оплатить" у выбранной квартиры, чтобы произвести оплату.
- После нажатия на кнопку, пользователь будет перенаправлен на страницу оплаты в системе PayMaster, где можно будет выбрать удобный способ оплаты и завершить транзакцию.

Таким образом, режим обычного пользователя позволяет комфортно и удобно искать и арендовать квартиры, а система оплаты PayMaster обеспечивает безопасные и удобные платежные операции.
