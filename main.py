import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import *
from states import router as state_router
from service import *
from connection import *
from callbacks import router as callback_router

load_dotenv()


token_bot = os.getenv("BOT_TOKEN")



bot = Bot(token=token_bot)


dp = Dispatcher()





@dp.message(F.text == "🍽 Каталог")
@dp.message(Command("movies"))
async def show_all_movies(message: Message):

    movies = await all_movies()

    if not movies:
        await message.answer("not movies yet")
        return

    await message.answer(f"your movies: {len(movies)}")


@dp.message(F.text == "найти книгу")
@dp.message(Command("movie"))
async def show_one_movie(message: Message):

    buttons = await get_movies_all_btn()

    if not buttons.inline_keyboard:
        await message.answer("movies catalog is empty, try to add with add button")
        return

    await message.answer("select a movie to see about", reply_markup=buttons)






@dp.message(Command("start"))
async def start_bot(message: Message):

    user = message.from_user

    if not await profile(user.id):
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"hello {message.from_user.full_name}", reply_markup=main_kb)
    else:
        await message.answer(f"Welcome back, {user.full_name}", reply_markup=main_kb)




async def main():
    print("Бот запущен")
    await create_tables()
    dp.include_router(state_router)
    dp.include_router(callback_router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())


