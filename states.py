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



@router.message(F.text == "Добавить книгу")
@router.message(Command("add"))
async def add_movie_command(message: Message, state: FSMContext):
    await message.answer("enter name of movie")
    await state.set_state(add_new_movie.get_movie_name)


@router.message(add_new_movie.get_movie_name)
async def add_movie_get_name(message : Message, state: FSMContext):

    name = message.text
    if not name or not name.strip():
        await message.answer("Name can not be empty! try again")
        return

    await state.update_data(name = name)

    await message.answer("Enter a genre of movie")
    await state.set_state(add_new_movie.get_movie_genre)




@router.message(add_new_movie.get_movie_genre)
async def add_movie_get_genre(message : Message, state: FSMContext):

    genre = message.text
    if not genre or not genre.strip():
        await message.answer("Genre can not be empty! try again")
        return

    await state.update_data(genre = genre)

    await message.answer("Enter a caption of movie (or 0 to skip)")
    await state.set_state(add_new_movie.get_movie_caption)




@router.message(add_new_movie.get_movie_caption)
async def add_movie_get_caption(message : Message, state: FSMContext):

    caption = "" if message.text == '0' else message.text

    await state.update_data(caption = caption)

    await message.answer("Enter a release_year of movie")
    await state.set_state(add_new_movie.get_movie_release_year)


@router.message(add_new_movie.get_movie_release_year)
async def add_new_movie_get_year(message: Message, state: FSMContext):

    year = message.text

    if not year.isdigit():
        await message.answer("Please enter a number")
        return
    if not 1888 <= int(year) <= datetime.now().year:
        await message.answer("Year is invalid , try again")
        return

    await state.update_data(year = year)

    await message.answer("send poster of movie")
    await state.set_state(add_new_movie.get_movie_photo)





@router.message(add_new_movie.get_movie_photo)
async def add_new_movie_get_photo(message: Message, state: FSMContext):

    if not message.photo:
        await message.answer("send me a photo!")
        return

    photo = message.photo[-1].file_id

    data = await state.get_data()

    if not data['caption'].strip():
        result = await add_new_movie_service(message.from_user.id, data['name'], data['genre'], data['year'], photo)
    else:
        result = await add_new_movie_service(message.from_user.id, data['name'], data['genre'], data['year'], photo, data['caption'])


    if result:
        await message.answer("your movie added")
    else:
        await message.answer("something went wrong")

    await state.clear()
        



