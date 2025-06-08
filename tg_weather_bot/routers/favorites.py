from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
from services.favorites_storage import FavoritesStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.location_storage import PlaceStorage


router = Router()

# инициализируем хранилище (файл рядом с bot.py: storage/favorites.json)
storage = FavoritesStorage("storage/favorites.json")
place_storage = PlaceStorage("storage/place.json")

# ---- Добавить в избранное ----
# Использование: /add_fav <place>
@router.message(Command("add_fav"))
async def cmd_add_favorit(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Вы забыли написать место.\nВоспользуйтесь командой /add_fav <place>")

    place = parts[1].strip()
    # опционально можно проверить существование через mal_client.anime_exists
    await storage.add(message.from_user.id, place)
    await message.reply(f"{place} добавлен в избранное.")

# ---- Список избранного ----
@router.message(Command("favorites"))
async def cmd_list_favorites(message: Message):
    favs = await storage.list(message.from_user.id)
    if not favs:
        return await message.reply("Пока нет избранного 🙁")
    text = "Ваше избранное:\n" + "\n".join(f"- {a}" for a in favs)
    # кнопки для выбора каждого:
    kb = InlineKeyboardBuilder()
    for fav in favs:
        kb.button(text=f"{fav}", callback_data=f"choose_place_{fav}")
    kb.adjust(1)
    await message.reply(text, reply_markup=kb.as_markup())

# Выбрать по кнопке
@router.callback_query(lambda c: c.data.startswith("choose_place_"))
async def cmd_choose_place(query: CallbackQuery):
    place = query.data.split("_", 2)[2]
    await place_storage.choice(query.from_user.id, place)
    await query.answer(f"{place} выбран.", show_alert=False)

# ---- Удалить из избранного командой ----
@router.message(Command("remove_fav"))
async def cmd_remove_favorit(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Вы забыли написать место.\nВоспользуйтесь командой /remove_fav <place>")
    place = parts[1].strip()
    await storage.remove(message.from_user.id, place)
    await message.reply(f"❌ {place} удален из избранного.")



