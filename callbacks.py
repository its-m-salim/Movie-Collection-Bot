from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from service import *
from keyboards import *
router = Router()




@router.callback_query(F.data.startswith("movie_show_"))
async def show_about_movie(callback: CallbackQuery):

    movie_id = callback.data.split("_")[2]

    movie = await one_movie(movie_id)
  
    if not movie:
        await callback.message.answer("Something went wrong about showing info about movie")
        print(callback.data)
        return



    caption = f"""
<b>{movie['title']}</b>
year: {movie['release_year']}
genre: {movie['genre']}
"""

 
    buttons = await get_info_about_movie(int(movie_id))

    await callback.message.answer_photo(photo=movie['poster_file_id'], caption=caption, reply_markup=buttons, parse_mode="HTML")
    await callback.answer()




@router.callback_query(F.data.startswith("movie_favourite_"))
async def add_movie_to_favourites(callback: CallbackQuery):

    movie_id = callback.data.split("_")[2]

    if await check_favourites(movie_id, callback.from_user.id):
        await callback.message.answer("this movie is already in your favourites")
        await callback.answer()
        return 

    if await to_favourites(movie_id, callback.from_user.id):
        await callback.message.answer("movie successfuly added to favourites")
    else:
        await callback.message.answer("something went wrong while adding to favourites")






@router.callback_query(F.data.startswith("movie_about_"))
async def show_movie_description(callback: CallbackQuery):
    
    movie_id = callback.data.split("_")[2]
    print(callback.data)
    print(movie_id)
    movie = await one_movie(movie_id)

    if not movie:
        await callback.answer("Фильм не найден", show_alert=True)
        return

    caption = f"""
<b>{movie['title']}</b>
Год: {movie['release_year']}
Жанр: {movie['genre']}

📝 Описание:
{movie['caption']}
"""

    buttons = await get_back_button(movie_id)

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=buttons,
        parse_mode="HTML"
    )

    await callback.answer()




@router.callback_query(F.data.startswith("movie_back_"))
async def back_to_movie(callback: CallbackQuery):
    
    movie_id = callback.data.split("_")[2]
    print(callback.data)
    print(movie_id)
    movie = await one_movie(movie_id)

    if not movie:
        await callback.answer("Фильм не найден", show_alert=True)
        return

    caption = f"""
<b>{movie['title']}</b>
year: {movie['release_year']}
genre: {movie['genre']}
"""

 
    buttons = await get_info_about_movie(int(movie_id))

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=buttons,
        parse_mode="HTML"
    )

    await callback.answer()