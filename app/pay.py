
# Pay for apartment callback query handler
@dp.callback_query_handler(text="pay")
async def pay_for_apartment(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    title = "Аренда квартиры"
    description = "Аренда квартиры"
    invoice_payload = "month_sub"
    provider_token = os.getenv('PAYMENTS_TOKEN')
    # Querying the price from the database
    cursor.execute("SELECT price FROM catalog WHERE id=?", (USER_DATA['apartment_index']+1,))
    price = cursor.fetchone()

    currency = "RUB"
    new_price = int(price[0]) * max(USER_DATA.get('rent_days', 1), 1)
    prices = [types.LabeledPrice(label='Subscription', amount=new_price*100)]
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