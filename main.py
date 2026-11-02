import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command ,StateFilter
from keyboards import *
from states import router as state_router
from service import *
from connection import *
from texts import movie_caption
from callbacks import router as callback_router
from fallback import router as fallback_router
load_dotenv()


token_bot = os.getenv("BOT_TOKEN")



bot = Bot(token=token_bot)


dp = Dispatcher()




@dp.message(F.text == "⭐ Избранное")
@dp.message(Command("favourites"))
async def show_all_movies(message: Message):

    movies = await get_favourite_movies(message.from_user.id)

    if not movies:
        await message.answer("⭐ В избранном пока пусто.\n\nОткройте каталог и сохраните фильмы, которые захотите посмотреть!")
        return

    for movie in movies:
        buttons = await delete_from_fv_button(movie['movie_id'])
        caption =movie_caption(movie)
        await message.answer_photo(photo=movie['poster_file_id'], caption=caption, reply_markup=buttons, parse_mode="HTML")


@dp.message(F.text == "🎲 Случайный фильм")
@dp.message(Command("random"))
async def show_random_movie(message: Message):
    movie = await random_movie()

    if not movie:
        await message.answer("🎬 Каталог пока пуст.\n\nДобавьте первый фильм, чтобы здесь появились рекомендации!")
        return

    caption = movie_caption(movie)
    

    await message.answer_photo(photo=movie['poster_file_id'], caption=caption, parse_mode="HTML", reply_markup= await get_random_btn(movie['id']))






@dp.message(F.text == "🍿 Каталог фильмов")
@dp.message(Command("movies"))
async def show_one_movie(message: Message):

    buttons = await get_movies_all_btn()

    if not buttons.inline_keyboard:
        await message.answer("🎬 В каталоге пока нет фильмов.\n\nНажмите «➕ Добавить фильм», чтобы добавить первый!")
        return

    await message.answer("🍿 Выберите фильм, чтобы открыть его карточку:", reply_markup=buttons)



@dp.message(F.text == "📊 Статистика")
@dp.message(Command("stats"))
async def show_favourites_count(message: Message):

    total = await get_favourites_count(message.from_user.id)
    if total['count'] < 1:
        await message.answer("⭐ У вас пока нет избранных фильмов.\n\nЗагляните в каталог и добавьте туда то, что вам понравилось!")
        return

    await message.answer(f"⭐ В избранном сохранено фильмов: {total['count']}.")




@dp.message(F.text == "🎭 Жанры")
@dp.message(Command("genre"))
async def show_genres(message: Message):

    buttons = await get_genres_btn()

    if not buttons.inline_keyboard:
        await message.answer("🎭 Жанров пока нет.\n\nНажмите «➕ Добавить фильм», чтобы добавить первый!")
        return

    await message.answer("🎭 Выберите жанр:", reply_markup=buttons)




@dp.message(Command("start"))
async def start_bot(message: Message):

    user = message.from_user

    if not await profile(user.id):
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"👋 Добро пожаловать, {message.from_user.full_name}!\n\n🍿 Здесь вы можете просматривать общий каталог, находить случайные фильмы и собирать собственную коллекцию избранного.\n\nВыберите действие в меню:", reply_markup=main_kb)
    else:
        await message.answer(f"👋 С возвращением, {user.full_name}!\n\nПродолжим знакомиться с фильмами? Выберите действие в меню:", reply_markup=main_kb)




async def main():
    print("Бот запущен")
    await create_tables()
    dp.include_router(state_router)
    dp.include_router(callback_router)
    dp.include_router(fallback_router)
    await dp.start_polling(bot)




if __name__ == "__main__":
    asyncio.run(main())
