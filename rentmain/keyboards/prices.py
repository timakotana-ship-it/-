# keyboards/prices.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def rent_price_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="9$/20Min.", callback_data="tariff|9|20")],
        [InlineKeyboardButton(text="7$/15Min.", callback_data="tariff|7|15")],
        [InlineKeyboardButton(text="10$/1Час/До 3 час.", callback_data="tariff|10|60")]
    ])
    return kb
