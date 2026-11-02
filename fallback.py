from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router()


@router.message(StateFilter(None))
async def unknown_message(message: Message):
    await message.answer("🤔 Не понял вас. Выберите действие в меню или отправьте /help.")