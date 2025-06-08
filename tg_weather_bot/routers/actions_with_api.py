from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from config.settings_api_key_weather import api_key_weather
from services.weather_client import ApiInteractionClient
from services.location_storage import PlaceStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

router = Router()


mal_client = ApiInteractionClient(api_key_weather.api_key_weather)
place_storage = PlaceStorage("storage/place.json")


# Использование: /place <place>
@router.message(Command("place"))
async def cmd_place(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Вы забыли написать место: /place <place>")

    place = parts[1].strip()
    await place_storage.choice(message.from_user.id, place)
    await message.reply(f"{place} выбран.")


# Использование: /now_wheather
@router.message(Command("now_weather"))
async def cmd_now_weather(message: Message):
    place = await place_storage.get_place(message.from_user.id)
    if place == "":
        return await message.reply("Место не выбрано.\nВоспользуйтесь командой /place <place>")
    response = await mal_client.get_weather(place)
    if response['cod'] == 200:
        return await message.reply(f"В {response['name']} {int(round((response['main']['temp'] -273), 0))} °С\n"
                                   f"Скорость ветра {int(round(response['wind']['speed'], 0))} м/с\n"
                                   f"Минмальная температура {int(round(response['main']['temp_min'], 0))}\n"
                                   f"Максимальная температура {int(round(response['main']['temp_max'], 0))}\n")
    else:
        return await message.reply(f"Ошибка:(\n\n Код {response['cod']}\nСообщение API {response['message']}")
    
    
        
    
    
