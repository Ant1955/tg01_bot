from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Тестовая кнопка 1")],
   [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
], resize_keyboard=True)

inline_keyboard_links = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Ноыости", callback_data='news')],
   [InlineKeyboardButton(text="Музыка", callback_data='music')],
   [InlineKeyboardButton(text="Видео", callback_data='video')]
])

startkb = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Привет")],
   [KeyboardButton(text="Пока")]
], resize_keyboard=True)

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   for key in test:
       keyboard.add(InlineKeyboardButton(text=key, url='https://www.youtube.com/watch?v=HfaIcB4Ogxk'))
   return keyboard.adjust(2).as_markup()
