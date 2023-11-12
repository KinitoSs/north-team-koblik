from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from keyboards.simple_kb import make_row_keyboard
from aiogram.enums import ParseMode
router = Router()
from handlers.dataplot import process_data_and_plot
list_workplace = ['Зона сварки 1', 'Зона сварки 2', 'Зона сварки 3']
list_timeline = ['Сегодня', 'Вчера', 'Неделя', 'Месяц']
class Choosing_stat(StatesGroup):
    choosing_workspace_name = State()
    choosing_datatime_size = State()
@router.message(StateFilter(None), Command("start"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Выберита завод:",
        reply_markup=make_row_keyboard(list_workplace)
    )
    await state.set_state(Choosing_stat.choosing_workspace_name)
@router.message(Choosing_stat.choosing_workspace_name, F.text.in_(list_workplace))
async def time_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите дату:",
        reply_markup=make_row_keyboard(list_timeline)
    )
    await state.set_state(Choosing_stat.choosing_datatime_size)
@router.message(StateFilter("Choosing_stat:choosing_workspace_name"))
async def chosen_incorrectly(message: Message):
    await message.answer(
        text="Такого места нет в базе.\n\n"
             "Пожалуйста, выберите одну из предложенных меток:",
        reply_markup=make_row_keyboard(list_workplace)
    )
@router.message(Choosing_stat.choosing_datatime_size, F.text.in_(list_timeline))
async def time_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали статистику за: {message.text.lower()}. Место: {user_data['chosen_food']}.\n",
        reply_markup=ReplyKeyboardRemove()
    )
    total_time_data = process_data_and_plot("latex.csv")
    photo = FSInputFile("plot.png")
    await message.answer_photo(photo=photo)
    file = FSInputFile("latex.csv", filename="latex.csv")
    await message.answer_document(document=file)
    # statistics_string = total_time_data.to_csv(index=False)
    # await message.answer(text=f"Статистика за выбранный период:\n{statistics_string}")
    await state.clear()
    await message.answer(
        text="Выберита завод:",
        reply_markup=make_row_keyboard(list_workplace)
    )
    await state.set_state(Choosing_stat.choosing_workspace_name)
@router.message(Choosing_stat.choosing_datatime_size)
async def chosen_incorrectly(message: Message):
    await message.answer(
        text="Такой даты нет в базе.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(list_timeline)
    )