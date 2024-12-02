from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import crud_functions

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button_3 = KeyboardButton(text='Купить')
kb.add(button)
kb.add(button2)
kb.add(button_3)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.add(button3)
kb2.add(button4)

kb3 = InlineKeyboardMarkup(resize_keyboard=True)
button_1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button_2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button_3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button_4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb3.add(button_1)
kb3.add(button_2)
kb3.add(button_3)
kb3.add(button_4)


@dp.message_handler(text='Рассчитать', state=None)
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию', reply_markup=kb2)


@dp.message_handler(text='Купить', state=None)
async def get_buying_list(message: types.Message):
    products_list = crud_functions.get_all_products()
    for i in range(1, 5):
        await message.answer(f'Название: {products_list[i][0]} | Описание: {products_list[i][1]}| Цена: {products_list[i][2]}')
        with open(f'{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb3)

@dp.callback_query_handler(text="product_buying", state=None)
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text=['formulas'], state=None)
async def get_formulas(call):
    await call.message.answer(f'Для мужчин: 10 х вес(кг) + 6,25 х рост(см) - 5 х возраст(г) + 5''\n'
                              'Для женщин: 10 х вес(кг) + 6,25 х рост(см) - 5 х возраст(г) + 161')
    await call.answer()


@dp.message_handler(commands=['start'], state=None)
async def start(message: types.Message):
    await message.answer('Нажми на одну из кнопок.', reply_markup=kb)


@dp.message_handler(text=['Информация'], state=None)
async def inform(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text=['calories'], state=None)
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = float(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма калорий: {calories} ккал.')
    await state.finish()


@dp.message_handler()
async def hello(message: types.Message):
    await message.answer('Привет! Хочешь узнать свою норму калорий? Тогда нажми на /start!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
