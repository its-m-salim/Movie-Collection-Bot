from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from service import *





main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍽 Каталог"), KeyboardButton(text="избранные")],
        [KeyboardButton(text="cлучайный фильм"), KeyboardButton(text="Добавить фильм")],
        [KeyboardButton(text="stats"), KeyboardButton(text="Помощь")]
        
    ],
    resize_keyboard=True,
)





async def get_movies_all_btn():
    data = await all_movies()
    keyboards = []

    for movies in data:
        keyboards.append([InlineKeyboardButton(text=f"{movies['title']}", callback_data=f"movie_show_{movies['id']}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keyboard




async def get_info_about_movie(movie_id):

    keyboards = [
        [InlineKeyboardButton(text="Подробнее", callback_data=f"movie_about_{movie_id}"), InlineKeyboardButton(text="в избранном", callback_data=f"movie_favourite_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard




async def get_back_button(movie_id):
    keyboards = [
        [InlineKeyboardButton(text="back", callback_data=f"movie_back_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard




async def delete_from_fv_button(movie_id):
    keyboards = [
        [InlineKeyboardButton(text="удалить из избранного", callback_data=f"movie_delete_{movie_id}"), InlineKeyboardButton(text="Подробнее", callback_data=f"fv_movie_about_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard




async def get_fv_back_button(movie_id):
    keyboards = [
        [InlineKeyboardButton(text="back", callback_data=f"fv_movie_back_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard



async def get_random_back_button(movie_id):
    keyboards = [
        [InlineKeyboardButton(text="back", callback_data=f"random_movie_back_{movie_id}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard






async def get_random_btn(movie_id):

    keyboards = [
        [InlineKeyboardButton(text="Подробнее", callback_data=f"random_movie_about_{movie_id}"), InlineKeyboardButton(text="в избранном", callback_data=f"movie_favourite_{movie_id}")],
        [InlineKeyboardButton(text="Скрыт", callback_data="hide")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboards)

    return keyboard