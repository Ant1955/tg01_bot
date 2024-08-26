import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY
import random
from datetime import datetime
import requests
from gtts import gTTS
import os
from googletrans import Translator
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging

  #  @Advt2024r_bot.
bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect('bot.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    chat_id INTEGER)''')

conn.commit()
conn.close()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
	CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	age INTEGER NOT NULL,
	grade TEXT NOT NULL)
	''')
    conn.commit()
    conn.close()

init_db()

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком ты классе (на каком курсе)?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state:FSMContext):
    await state.update_data(grade=message.text)

    user_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO users (name, age, grade) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()
    await state.clear()


@dp.message(Command('dblist'))
async def dblist(message: Message):
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('SELECT name, age, grade FROM users')
    students = cur.fetchall()
    conn.close()
    if students:
        students_list = "\n".join([f"Name: {name}, Age: {age}, Grade: {grade}" for name, age, grade in students])
    else:
        students_list = "No students found."
    await message.answer(f"Список учеников (студентов)\n {students_list}")


def get_weather(city):
    api_key = WEATHER_API_KEY
   #адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
   #для получения результата нам понадобится модуль requests
    response = requests.get(url)
   #прописываем формат возврата результата
    return response.json()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather [город]")

@dp.message(Command('weather'))
async def weather_get(message: Message):
    sentence = message.text.lower()
    words = sentence.split()
    if len(words) >= 2:
        city = words[1]
    else:
        city = "moscow"
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    stime = now.strftime("%H:%M")
    try:
        weather = get_weather(city)
        temp = str(weather['main']['temp']) + '°C'
        deskr = weather['weather'][0]['description']
        await message.answer(f'просто осень скоро в {city} \n '
                         f'сегодня {date} температура {temp} на {stime}\n'
                         f'{deskr}')
    except KeyError as e:
        await message.answer("Не удалось получить данные о погоде. Попробуйте еще раз.")
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте еще раз.")
#Прописываем хендлер и варианты ответов:

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://vet-centre.by/wp-content/uploads/2016/11/kot-v-luchah-eti-udivitelnye-kotiki.jpg',
            'https://vet-centre.by/wp-content/uploads/2016/11/kot-s-myshyu-eti-udivitelnye-kotiki.jpg',
            'https://n1s2.hsmedia.ru/f0/c9/60/f0c96065f1e50771c40113e2324af266/823x1200_0xac120003_9211641921663938997.jpeg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")
   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   audio = FSInputFile('training.ogg')
   await bot.send_audio(message.chat.id, audio)
   os.remove("training.ogg")

@dp.message()
async def start(message: Message):
    translator = Translator()
    try:
        # Перевод текста
        translation = translator.translate(message.text, src='ru', dest='en')
        await message.answer(f"Перевод: {translation.text}")
    except Exception as e:
        print(f"ошибка {e}")
        await message.answer("Произошла ошибка при переводе.")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())