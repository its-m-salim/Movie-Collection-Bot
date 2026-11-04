from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from service import *
from keyboards import *
from datetime import date, datetime
from my_movies import *
router = Router()




class add_new_movie(StatesGroup):
    get_movie_name = State()
    get_movie_genre = State()
    get_movie_caption = State()
    get_movie_release_year= State()
    get_movie_photo = State()


class search_movie(StatesGroup):
    get_query = State()





@router.message(Command("cancel"))
@router.message(F.text == "❌ Отмена")
async def cancel_by_message(message: Message, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Сейчас нет активного ввода, отменять нечего.")
        return


    if current_state in add_new_movie.__all_states__:
        await message.answer("↩️ Добавление фильма отменено. Вы можете выбрать другое действие в меню.")
    elif current_state in search_movie.__all_states__:
        await message.answer("↩️ Поиск фильма отменено. Вы можете выбрать другое действие в меню.")
    elif current_state in edit_my_movie.__all_states__:
        await message.answer("↩️Изменения фильма отменено. Вы можете выбрать другое в меню.")

    await state.clear()




@router.message(F.text == "🔍 Поиск")
async def start_search(message: Message, state: FSMContext):

    await state.set_state(search_movie.get_query)
    await message.answer("🔍 Введите название фильма или его часть.\n\nНапример: интер\n\nОтмена: /cancel")




@router.message(search_movie.get_query)
async def get_search_query(message: Message, state: FSMContext):

    if not message.text or message.text.startswith("/"):
        await message.answer("⚠️ Отправьте название текстом, например: интер\n\nОтмена: /cancel")
        return

    query = message.text.strip()

    buttons = await get_search_btn(query)

    if not buttons.inline_keyboard:
        await message.answer(f"😔 По запросу «{query}» ничего не найдено.\n\nПопробуйте другое слово или отправьте /cancel.")
        return

    await state.clear()
    await message.answer(f"🔍 Найдено по запросу «{query}»: {len(buttons.inline_keyboard)}\n\nВыберите фильм, чтобы открыть карточку:", reply_markup=buttons)





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
        



