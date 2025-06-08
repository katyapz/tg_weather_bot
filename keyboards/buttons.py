from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_list = [
        [KeyboardButton(text="/now_weather")],
        [KeyboardButton(text="/favorites")],
    ]

keyboard = ReplyKeyboardMarkup(keyboard=kb_list,
                               resize_keyboard=True,
                               one_time_keyboard=False)
        
    

