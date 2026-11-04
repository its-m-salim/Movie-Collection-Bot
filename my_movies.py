from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from html import escape
from datetime import datetime
from service import *
from keyboards import *
from texts import *
router = Router()




class edit_my_movie(StatesGroup):
    get_new_value = State()




async def get_my_movie(movie_id, tg_id):
    movie = await one_movie(movie_id)

    if not movie or movie['owner_id'] != tg_id:
        return None

    return movie




@router.callback_query(F.data.startswith("my_show_"))
async def show_my_movie(callback: CallbackQuery):

    movie_id = callback.data.split("_")[2]

    movie = await get_my_movie(movie_id, callback.from_user.id)

    if not movie:
        await callback.answer("❌ Фильм не найден или он не ваш.", show_alert=True)
        return

    buttons = await my_movie_btn(movie_id)

    await callback.message.answer_photo(photo=movie['poster_file_id'], caption=movie_caption(movie, show_description=True), reply_markup=buttons, parse_mode="HTML")
    await callback.answer()




@router.callback_query(F.data.startswith("my_back_"))
async def back_to_my_movie(callback: CallbackQuery):

    movie_id = callback.data.split("_")[2]

    movie = await get_my_movie(movie_id, callback.from_user.id)

    if not movie:
        await callback.answer("❌ Фильм не найден или он не ваш.", show_alert=True)
        return

    buttons = await my_movie_btn(movie_id)

    await callback.message.edit_caption(caption=movie_caption(movie, show_description=True), reply_markup=buttons, parse_mode="HTML")
    await callback.answer()




@router.callback_query(F.data == "my_list")
async def back_to_my_list(callback: CallbackQuery):

    buttons = await get_my_movies_btn(callback.from_user.id)

    if not buttons.inline_keyboard:
        await callback.message.answer("🎬 Вы пока не добавили ни одного фильма.")
    else:
        await callback.message.answer(f"🎬 Ваши фильмы: {len(buttons.inline_keyboard)}\n\nВыберите фильм, чтобы открыть его и изменить:", reply_markup=buttons)

    await callback.message.delete()
    await callback.answer()




@router.callback_query(F.data.startswith("my_edit_"))
async def start_edit_movie(callback: CallbackQuery, state: FSMContext):

    field = callback.data.split("_")[2]
    movie_id = callback.data.split("_")[3]

    movie = await get_my_movie(movie_id, callback.from_user.id)

    if not movie or field not in EDIT_TEXTS:
        await callback.answer("❌ Фильм не найден или он не ваш.", show_alert=True)
        return

    await state.update_data(movie_id = movie_id, field = field)
    await state.set_state(edit_my_movie.get_new_value)

    await callback.message.answer(f"{EDIT_TEXTS[field]}\n\nОтмена: «❌ Отмена» или /cancel")
    await callback.answer()




@router.message(edit_my_movie.get_new_value)
async def save_new_value(message: Message, state: FSMContext):

    data = await state.get_data()
    field = data['field']
    movie_id = data['movie_id']

    if field == "photo":
        if not message.photo:
            await message.answer("⚠️ Это не фотография. Отправьте постер как изображение, не как файл:")
            return

        value = message.photo[-1].file_id

    else:
        if not message.text or message.text.startswith("/"):
            await message.answer("⚠️ Отправьте новое значение текстом:")
            return

        value = message.text.strip()

        if not value:
            await message.answer("⚠️ Значение не может быть пустым. Попробуйте ещё раз:")
            return

        if field in ("title", "genre") and len(value) > 200:
            await message.answer("⚠️ Слишком длинно, максимум 200 символов. Попробуйте ещё раз:")
            return

        if field == "genre":
            value = value.capitalize()

        if field == "year":
            if not value.isdecimal() or not 1888 <= int(value) <= datetime.now().year:
                await message.answer(f"⚠️ Укажите год числом от 1888 до {datetime.now().year}:")
                return
            value = int(value)

        if field == "caption":
            if len(value) > 1000:
                await message.answer("⚠️ Описание слишком длинное, максимум 1000 символов. Сократите его:")
                return

            if value == "0":
                value = None

    if not await update_my_movie(movie_id, message.from_user.id, field, value):
        await message.answer("❌ Не удалось сохранить изменения. Попробуйте ещё раз позже.")
        return

    await state.clear()

    movie = await get_my_movie(movie_id, message.from_user.id)
    buttons = await my_movie_btn(movie_id)

    await message.answer("✅ Готово! Вот обновлённая карточка:")
    await message.answer_photo(photo=movie['poster_file_id'], caption=movie_caption(movie, show_description=True), reply_markup=buttons, parse_mode="HTML")




@router.callback_query(F.data.startswith("my_ask_delete_"))
async def ask_delete_movie(callback: CallbackQuery):

    movie_id = callback.data.split("_")[3]

    movie = await get_my_movie(movie_id, callback.from_user.id)

    if not movie:
        await callback.answer("❌ Фильм не найден или он не ваш.", show_alert=True)
        return

    title = escape(str(movie['title']))
    buttons = await confirm_delete_btn(movie_id)

    await callback.message.edit_caption(caption=f"⚠️ Удалить фильм <b>{title}</b>?\n\nОн исчезнет из каталога и из избранного других пользователей. Отменить это нельзя.", reply_markup=buttons, parse_mode="HTML")
    await callback.answer()




@router.callback_query(F.data.startswith("my_do_delete_"))
async def delete_movie(callback: CallbackQuery):

    movie_id = callback.data.split("_")[3]

    movie = await get_my_movie(movie_id, callback.from_user.id)

    if not movie:
        await callback.answer("❌ Фильм не найден или он не ваш.", show_alert=True)
        return

    if not await delete_my_movie(movie_id, callback.from_user.id):
        await callback.answer("❌ Не удалось удалить фильм. Попробуйте позже.", show_alert=True)
        return

    await callback.message.answer(f"🗑 Фильм «{movie['title']}» удалён.")
    await callback.message.delete()
    await callback.answer()