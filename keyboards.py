from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = [
        [KeyboardButton(text="📱 Доступные номера")],
        [KeyboardButton(text="🛒 Купить"), KeyboardButton(text="📦 Мои покупки")],
        [KeyboardButton(text="❓ FAQ"), KeyboardButton(text="✉️ Поддержка")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def products_list(products):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for pid, name, price, _, _ in products:
        kb.inline_keyboard.append([InlineKeyboardButton(text=f"{name} - {price}₽", callback_data=f"buy_{pid}")])
    kb.inline_keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")])
    return kb
