import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, ADMIN_IDS
from database import init_db, get_products, buy_product
from keyboards import main_menu, products_list
from states import AdminStates

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в магазин физических номеров!\nВыберите действие:", reply_markup=main_menu())

@dp.message(F.text == "📱 Доступные номера")
async def show_products(message: Message):
    products = get_products()
    if not products:
        await message.answer("❌ Нет доступных товаров. Зайдите позже.")
        return
    text = "📋 *Доступные номера:*\n\n"
    for pid, name, price, desc, stock in products:
        text += f"🔹 *{name}* - {price}₽\n_{desc}_\nВ наличии: {stock}\n\n"
    await message.answer(text, parse_mode="Markdown", reply_markup=products_list(products))

@dp.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    phone = buy_product(user_id, product_id)
    if phone:
        await callback.message.answer(f"✅ Оплата прошла успешно!\nВаш номер: `{phone}`\nКарта будет активирована в течение 24 часов.", parse_mode="Markdown")
    else:
        await callback.message.answer("❌ Ошибка при покупке. Попробуйте позже.")
    await callback.answer()

@dp.message(F.text == "📦 Мои покупки")
async def my_purchases(message: Message):
    await message.answer("Здесь будет список ваших купленных номеров (доделай через БД).")

@dp.message(F.text == "❓ FAQ")
async def faq(message: Message):
    await message.answer("❓ *Частые вопросы*\n1. Как активировать номер? — Вставьте SIM-карту.\n2. Срок годности — 1 год.\n3. Есть ли поддержка? — Напишите в раздел 'Поддержка'.", parse_mode="Markdown")

@dp.message(F.text == "✉️ Поддержка")
async def support(message: Message):
    await message.answer("📩 Напишите ваш вопрос сюда. Мы ответим в течение часа.\n\nИли свяжитесь вручную: @support_username")

# Простой админ-команда для добавления товара
@dp.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Нет доступа.")
        return
    await message.answer("Введите название товара:")
    await state.set_state(AdminStates.waiting_for_product_name)

@dp.message(AdminStates.waiting_for_product_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите цену (только число):")
    await state.set_state(AdminStates.waiting_for_product_price)

@dp.message(AdminStates.waiting_for_product_price)
async def get_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число!")
        return
    await state.update_data(price=int(message.text))
    await message.answer("Введите описание товара:")
    await state.set_state(AdminStates.waiting_for_product_desc)

@dp.message(AdminStates.waiting_for_product_desc)
async def get_desc(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await message.answer("Введите количество в наличии (число):")
    await state.set_state(AdminStates.waiting_for_product_stock)

@dp.message(AdminStates.waiting_for_product_stock)
async def get_stock(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число!")
        return
    data = await state.get_data()
    name = data["name"]
    price = data["price"]
    desc = data["desc"]
    stock = int(message.text)

    # Сохраняем в БД
    conn = sqlite3.connect('shop.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, price, description, stock) VALUES (?, ?, ?, ?)",
                (name, price, desc, stock))
    conn.commit()
    conn.close()
    await message.answer(f"✅ Товар '{name}' добавлен!")
    await state.clear()

async def main():
    init_db()
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
