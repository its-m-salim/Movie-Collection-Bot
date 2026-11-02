from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from service import *



main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍿 Каталог фильмов"), KeyboardButton(text="⭐ Избранное")],
        [KeyboardButton(text="🎭 Жанры"), KeyboardButton(text="🎲 Случайный фильм")],
        [KeyboardButton(text="➕ Добавить фильм"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True,
)




async def get_movies_all_btn():
    data = await all_movies()
    keyboards = []

    for movies in data:
        keyboards.append([InlineKeyboardButton(text=f"{movies['title']}({movies['release_year']})", callback_data=f"movie_show_{movies['id']}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard




async def get_info_about_movie(movie_id):

    keyboards = [
        [InlineKeyboardButton(text="📖 Подробнее", callback_data=f"movie_about_{movie_id}"), InlineKeyboardButton(text="⭐ В избранное", callback_data=f"movie_favourite_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard




async def get_back_button(movie_id):
    keyboards = [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"movie_back_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard




async def delete_from_fv_button(movie_id):
    keyboards = [
        [InlineKeyboardButton(text="🗑 Удалить из избранного", callback_data=f"movie_delete_{movie_id}"), InlineKeyboardButton(text="📖 Подробнее", callback_data=f"fv_movie_about_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard




async def get_fv_back_button(movie_id):
    keyboards = [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"fv_movie_back_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard



async def get_random_back_button(movie_id):
    keyboards = [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"random_movie_back_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard






async def get_random_btn(movie_id):

    keyboards = [
        [InlineKeyboardButton(text="📖 Подробнее", callback_data=f"random_movie_about_{movie_id}"), InlineKeyboardButton(text="⭐ В избранное", callback_data=f"movie_favourite_{movie_id}")],
        [InlineKeyboardButton(text="✖️ Закрыть карточку", callback_data="hide")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard



async def get_genres_btn():
    data = await get_all_genres() 
    keyboards = []
    row = []

    for genres in data:
        callback_data = f"genre_show_{genres['genre']}"

        

        row.append(InlineKeyboardButton(text=f"{genres['genre']} ({genres['count']})", callback_data=callback_data))

        if len(row) == 2:
            keyboards.append(row)
            row = []

    if row:
        keyboards.append(row)

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard




async def get_movies_by_genre_btn(genre):
    data = await get_movies_by_genre(genre) 
    keyboards = []

    for movies in data:
        keyboards.append([InlineKeyboardButton(text=f"{movies['title']} ({movies['release_year']})", callback_data=f"movie_show_{movies['id']}")])

    keyboards.append([InlineKeyboardButton(text="⬅️ Все жанры", callback_data="genre_back")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard