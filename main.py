import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
import random

from gtts import gTTS
import os

from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
   await callback.answer("Новости подгружаются", show_alert=True)
   await callback.message.edit_text('Вот свежие новости!', reply_markup=await kb.test_keyboard())

@dp.callback_query(F.data == 'links')
async def links(callback: CallbackQuery):
    await callback.message.answer( 'Вот эти',reply_markup=await kb.inline_keyboard_links())

@dp.message(F.text == "Тестовая кнопка 1")
async def test_button(message: Message):
   await message.answer('Обработка нажатия на reply кнопку')
@dp.message(F.text == "Привет")
async def hello(message: Message):
   await message.answer(f'Приветики, {message.from_user.first_name}')

@dp.message(F.text == "Пока")
async def bye(message: Message):
   await message.answer(f'До свидания, {message.from_user.first_name}')

@dp.message(Command('help'))
async def help(message: Message):
   await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /minitraining')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'да',reply_markup=kb.startkb)
 #  await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())
