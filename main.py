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





@dp.message(F.text == "избранные")
@dp.message(Command("favourites"))
async def show_all_movies(message: Message):

    movies = await get_favourite_movies(message.from_user.id)

    if not movies:
        await message.answer("Раздел избранных пока пусто ")
        return

    for movie in movies:
        buttons = await delete_from_fv_button(movie['movie_id'])
        caption = f"""
<b>{movie['title']}</b>

year: {movie['release_year']}

genre: {movie['genre']}
        """
        await message.answer_photo(photo=movie['poster_file_id'], caption=caption, reply_markup=buttons, parse_mode="HTML")


@dp.message(F.text == "cлучайный фильм")
@dp.message(Command("random"))
async def show_random_movie(message: Message):
    movie = await random_movie()

    if not movie:
        await message.answer("Каталог пока пуст!")
        return

    caption = f"""
🎬 <b>{movie['title']}</b>
📅 Год: {movie['release_year']}
🎭 Жанр: {movie['genre']}
"""
    

    await message.answer_photo(photo=movie['poster_file_id'], caption=caption, parse_mode="HTML", reply_markup= await get_random_btn(movie['id']))






@dp.message(F.text == "🍽 Каталог")
@dp.message(Command("movies"))
async def show_one_movie(message: Message):

    buttons = await get_movies_all_btn()

    if not buttons.inline_keyboard:
        await message.answer("movies catalog is empty, try to add with add button")
        return

    await message.answer("select a movie to see about", reply_markup=buttons)



@dp.message(F.text == "stats")
@dp.message(Command("stats"))
async def show_favourites_count(message: Message):

    total = await get_favourites_count(message.from_user.id)
    if total['count'] < 1:
        await message.answer("Похоже у вас нет избранных фильмов , исследуйте фильмы в общем каталоге")
        return

    await message.answer(f"У вас всего {total['count']} фильмов в избранном")







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


