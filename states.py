from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from service import *
from keyboards import *
from datetime import date, datetime
router = Router()




class add_new_movie(StatesGroup):
    get_movie_name = State()
    get_movie_genre = State()
    get_movie_caption = State()
    get_movie_release_year= State()
    get_movie_photo = State()





@router.message(Command("cancel"))
@router.message(F.text == "❌ Отмена")
async def cancel_by_message(message: Message, state: FSMContext):

    if await state.get_state() is None:
        await message.answer("Сейчас нет активного ввода, отменять нечего.")
        return


    await state.clear()
    await message.answer("↩️ Добавление фильма отменено. Вы можете выбрать другое действие в меню.")






@router.message(F.text == "➕ Добавить фильм")
@router.message(Command("add"))
async def add_movie_command(message: Message, state: FSMContext):
    await message.answer("🎬 Добавим новый фильм!\n\nШаг 1 из 5. Введите название фильма:")
    await state.set_state(add_new_movie.get_movie_name)


@router.message(add_new_movie.get_movie_name)
async def add_movie_get_name(message : Message, state: FSMContext):

    name = message.text
    if not name or not name.strip():
        await message.answer("⚠️ Название не может быть пустым. Попробуйте ещё раз:")
        return

    await state.update_data(name = name)

    await message.answer("🎭 Шаг 2 из 5. Укажите жанр фильма:")
    await state.set_state(add_new_movie.get_movie_genre)




@router.message(add_new_movie.get_movie_genre)
async def add_movie_get_genre(message : Message, state: FSMContext):


    genre = message.text
    if not genre or not genre.strip():
        await message.answer("⚠️ Жанр не может быть пустым. Укажите жанр ещё раз:")
        return

    await state.update_data(genre = genre.strip().capitalize())

    await message.answer("📝 Шаг 3 из 5. Напишите краткое описание фильма.\n\nЕсли хотите пропустить этот шаг, отправьте 0:")
    await state.set_state(add_new_movie.get_movie_caption)




@router.message(add_new_movie.get_movie_caption)
async def add_movie_get_caption(message : Message, state: FSMContext):

    if not message.text:
        await message.answer("⚠️ Описание должен быть текстом. Попробуйте ещё раз:")

    caption = "" if message.text == '0' else message.text

    await state.update_data(caption = caption)

    await message.answer("📅 Шаг 4 из 5. Укажите год выхода фильма:")
    await state.set_state(add_new_movie.get_movie_release_year)


@router.message(add_new_movie.get_movie_release_year)
async def add_new_movie_get_year(message: Message, state: FSMContext):

    year = message.text

    if not message.text:
        await message.answer("⚠️ Год должен быть числом. Попробуйте ещё раз:")
    
    if not year.isdigit():
        await message.answer("⚠️ Год должен быть числом. Попробуйте ещё раз:")
        return
    
    if not 1888 <= int(year) <= datetime.now().year:
        await message.answer(f"⚠️ Укажите год от 1888 до {datetime.now().year} включительно:")
        return

    await state.update_data(year = year)

    await message.answer("🖼 Шаг 5 из 5. Отправьте постер фильма одним сообщением:")
    await state.set_state(add_new_movie.get_movie_photo)





@router.message(add_new_movie.get_movie_photo)
async def add_new_movie_get_photo(message: Message, state: FSMContext):

    if not message.photo:
        await message.answer("⚠️ Это не фотография. Пожалуйста, отправьте постер фильма как изображение:")
        return

    photo = message.photo[-1].file_id

    data = await state.get_data()

    if not data['caption'].strip():
        result = await add_new_movie_service(message.from_user.id, data['name'], data['genre'], data['year'], photo)
    else:
        result = await add_new_movie_service(message.from_user.id, data['name'], data['genre'], data['year'], photo, data['caption'])


    if result:
        await message.answer("🎉 Фильм успешно добавлен в общий каталог!")
    else:
        await message.answer("❌ Не удалось добавить фильм. Попробуйте ещё раз позже.")

    await state.clear()
        



