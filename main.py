import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import random
from datetime import datetime
import requests
from gtts import gTTS
import os
from googletrans import Translator

  #  @Advt2024r_bot.
bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_weather(city):
    api_key = "fda902a077e24b262b0187ca6bc24204"
   #адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
   #для получения результата нам понадобится модуль requests
    response = requests.get(url)
   #прописываем формат возврата результата
    return response.json()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather [город]")

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектов')
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
    translation = translator.translate(message.text, src='ru', dest='en')
    await message.answer(f"Перевод: {translation}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())