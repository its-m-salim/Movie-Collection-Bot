from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from service import *
from keyboards import *
from texts import movie_caption
router = Router()




@router.callback_query(F.data.startswith("movie_show_"))
async def show_about_movie(callback: CallbackQuery):

    movie_id = callback.data.split("_")[2]

    movie = await one_movie(movie_id)
   
    if not movie:
        await callback.message.answer("❌ Не удалось открыть карточку фильма. Попробуйте ещё раз.")
        await callback.answer()
        return
    
    caption = movie_caption(movie)
 
    buttons = await get_info_about_movie(int(movie_id))

    await callback.message.answer_photo(photo=movie['poster_file_id'], caption=caption, reply_markup=buttons, parse_mode="HTML")
    await callback.answer()




@router.callback_query(F.data.startswith("movie_favourite_"))
async def add_movie_to_favourites(callback: CallbackQuery):

    movie_id = callback.data.split("_")[2]

    if await check_favourites(movie_id, callback.from_user.id):
        await callback.answer("⭐ Этот фильм уже есть в вашем избранном.")
        await callback.answer()
        return 

    if await to_favourites(movie_id, callback.from_user.id):
        await callback.answer("⭐ Фильм добавлен в избранное!")
    else:
        await callback.answer("❌ Не удалось добавить фильм. Попробуйте позже.")
    await callback.answer()






@router.callback_query(F.data.startswith("fv_movie_about_"))
async def show_fv_movie_description(callback: CallbackQuery):
    
    movie_id = callback.data.split("_")[3]
    
    movie = await one_movie(movie_id)

    if not movie:
        await callback.answer("🎬 Фильм не найден. Возможно, он был удалён.", show_alert=True)
        return

    caption = movie_caption(movie, show_description=True)

    buttons = await get_fv_back_button(movie_id)

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=buttons,
        parse_mode="HTML"
    )

    await callback.answer()



@router.callback_query(F.data.startswith("movie_about_"))
async def show_movie_description(callback: CallbackQuery):
    
    movie_id = callback.data.split("_")[2]
    
    movie = await one_movie(movie_id)

    if not movie:
        await callback.answer("🎬 Фильм не найден. Возможно, он был удалён.", show_alert=True)
        return

    caption = movie_caption(movie, show_description=True)

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
   
    movie = await one_movie(movie_id)

    if not movie:
        await callback.answer("🎬 Фильм не найден. Возможно, он был удалён.", show_alert=True)
        return

    caption = movie_caption(movie)

 
    buttons = await get_info_about_movie(int(movie_id))

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=buttons,
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data.startswith("movie_delete_"))
async def back_to_movie(callback: CallbackQuery):
    
    movie_id = callback.data.split("_")[2]


    if not await check_favourites(movie_id, callback.from_user.id):
        await callback.message.answer("Этот фильм уже удалён из избранного.")
        await callback.answer()
        return

    if await delete_from_favourites(movie_id, callback.from_user.id):
        await callback.message.delete()
        await callback.answer("🗑 Фильм удалён из вашего избранного.")
    else:
        await callback.answer("❌ Не удалось удалить фильм из избранного. Попробуйте ещё раз.")


    if not await get_favourite_movies(callback.from_user.id):
        await callback.message.answer("⭐ Ваш список избранного пуст. Самое время найти новый фильм в каталоге!")

    await callback.answer()



@router.callback_query(F.data == "hide")
async def hide_ms(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

    


@router.callback_query(F.data.startswith("fv_movie_back_"))
async def back_to_fv_movie(callback: CallbackQuery):
    
    movie_id = callback.data.split("_")[3]
   
    movie = await one_movie(movie_id)

    if not movie:
        await callback.answer("🎬 Фильм не найден. Возможно, он был удалён.", show_alert=True)
        return

    caption = movie_caption(movie)
 
    buttons = await delete_from_fv_button(int(movie_id))

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=buttons,
        parse_mode="HTML"
    )

    await callback.answer()







@router.callback_query(F.data.startswith("random_movie_about_"))
async def show_movie_description(callback: CallbackQuery):
    
    movie_id = callback.data.split("_")[3]
    
    movie = await one_movie(movie_id)

    if not movie:
        await callback.answer("🎬 Фильм не найден. Возможно, он был удалён.", show_alert=True)
        return

    caption = movie_caption(movie, show_description=True)

    buttons = await get_random_back_button(movie_id)

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=buttons,
        parse_mode="HTML"
    )

    await callback.answer()




@router.callback_query(F.data.startswith("random_movie_back_"))
async def back_to_movie(callback: CallbackQuery):
    
    movie_id = callback.data.split("_")[3]
   
    movie = await one_movie(movie_id)

    if not movie:
        await callback.answer("🎬 Фильм не найден. Возможно, он был удалён.", show_alert=True)
        return

    caption = movie_caption(movie)

 
    buttons = await get_random_btn(int(movie_id))

    await callback.message.edit_caption(
        caption=caption,
        reply_markup=buttons,
        parse_mode="HTML"
    )

    await callback.answer()




@router.callback_query(F.data.startswith("genre_show_"))
async def show_movies_by_genre(callback: CallbackQuery):

    genre = callback.data.split("_", 2)[2]

    buttons = await get_movies_by_genre_btn(genre)

    if len(buttons.inline_keyboard) < 2:
        await callback.answer("🎬 В этом жанре пока нет фильмов.", show_alert=True)
        return

    await callback.message.edit_text(f"🎭 Жанр: {genre}\n\nВыберите фильм, чтобы открыть карточку:", reply_markup=buttons)
    await callback.answer()




@router.callback_query(F.data == "genre_back")
async def back_to_genres(callback: CallbackQuery):

    buttons = await get_genres_btn()

    await callback.message.edit_text("🎭 Выберите жанр:", reply_markup=buttons)
    await callback.answer()



@router.callback_query(F.data == "random")
async def more_random(callback: CallbackQuery):
    movie = await random_movie()
    
    if not movie:
        await callback.message.answer("🎬 Каталог пока пуст.\n\nДобавьте первый фильм, чтобы здесь появились рекомендации!")
        await callback.answer()
        return

    caption = movie_caption(movie)
    
    await callback.answer()
    await callback.message.answer_photo(photo=movie['poster_file_id'], caption=caption, parse_mode="HTML", reply_markup= await get_random_btn(movie['id']))