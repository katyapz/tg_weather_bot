from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging
from keyboards.buttons import keyboard


router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот погоды\n"
                         "/help для информации о доступных командах",
                         reply_markup=keyboard)

    logging.info(f"User {message.from_user.id} called /start")

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - знакомство с ботом\n"
        "/now_weather - погода\n"
        "/place <place> - выбрать город\n"
        "/favorites - города в избранном\n"
        "/add_fav <place> - добавить город в избранном\n"
        "/remove_fav <place> - удалить город в избранном\n"
        "/help- инфориация о функционале\n"
        "/support- поддержка"
    )
