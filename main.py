import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery


from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.callback_query(F.data == 'showmore')
async def news(callback: CallbackQuery):
   await callback.message.edit_text('Два варианта', reply_markup=await kb.test_keyboard())


@dp.message(Command("dynamic"))
async def dynamic(message: Message):
    await message.answer('Динамик', reply_markup=kb.inline_keyboard_more)


@dp.message(Command("links"))
async def links(message: Message):
    await message.answer('Вот эти', reply_markup=kb.inline_keyboard_links)


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
    await message.answer(f'да-да',reply_markup=kb.startkb)
 #  await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_links)

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())
