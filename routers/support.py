from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from states.support_states import SupportStates
from filters.filters import IsAdmin, IsSupportMessage
from config.settings_admins import admins_config
from config.settings_bot import bot_config


class SupportHandler:
    def __init__(self, bot: Bot, admins: list):
        self.bot = bot
        self.admins = admins
        self.router = Router()
        self._register_handlers()

    def _register_handlers(self):
        self.router.message(F.text == "/support")(self.start_support)
        self.router.message(SupportStates.waiting_for_question)(self.process_question)
        self.router.message(IsAdmin(), IsSupportMessage())(self.admin_reply)
        self.router.callback_query(F.data.startswith("reply_"))(self.process_reply_button)
        self.router.message(SupportStates.waiting_for_response)(self.process_admin_response)

    async def start_support(self, message: types.Message, state: FSMContext):
        await state.set_state(SupportStates.waiting_for_question)
        await message.answer("Пожалуйста, опишите вашу проблему одним сообщением.")

    async def process_question(self, message: types.Message, state: FSMContext):
        await state.update_data(question=message.text, user_id=message.from_user.id)
        
        builder = InlineKeyboardBuilder()
        builder.button(text="Ответить", callback_data=f"reply_{message.from_user.id}")
        
        for admin_id in self.admins:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=f"Support ticket from {message.from_user.full_name} (ID: {message.from_user.id}):\n\n"
                         f"{message.text}",
                    reply_markup=builder.as_markup()
                )
            except Exception as e:
                print(f"Failed to send message to admin {admin_id}: {e}")
        
        await message.answer("Ваш вопрос отправлен в поддержку. Мы скоро ответим вам.")
        await state.clear()

    async def admin_reply(self, message: types.Message):
        original_message = message.reply_to_message.text
        user_id = int(original_message.split("ID: ")[1].split(")")[0])
        
        await self.bot.send_message(
            user_id,
            f"Поддержка:\n\n{message.text}"
        )
        
        await message.answer("Ответ был отправлен пользователю.")

    async def process_reply_button(self, callback: types.CallbackQuery, state: FSMContext):
        user_id = int(callback.data.split("_")[1])
        await state.update_data(target_user_id=user_id)
        await state.set_state(SupportStates.waiting_for_response)
        await callback.message.answer(f"Введите ответ пользователю {user_id}:")
        await callback.answer()

    async def process_admin_response(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        user_id = data['target_user_id']
        
        await self.bot.send_message(
            user_id,
            f"Поддержка:\n\n{message.text}"
        )
        
        await message.answer("Ваш ответ отправлен пользователю.")
        await state.clear()


# Инициализация
ADMINS = admins_config.settings_admins
bot = Bot(token=bot_config.telegram_api_key)
support_handler = SupportHandler(bot, ADMINS)
router = support_handler.router
