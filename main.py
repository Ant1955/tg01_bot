import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN
import random
from datetime import datetime
import requests

  #  @Advt2024r_bot.
bot = Bot(token=TOKEN)
dp = Dispatcher()

global count
count = 0

def get_weather(city):
    global count
    api_key = "fda902a077e24b262b0187ca6bc24204"
   #адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
   #для получения результата нам понадобится модуль requests
    count += 1
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
    global count
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
        print(f"{city}\n{weather}")
        temp = str(weather['main']['temp']) + '°C'
        deskr = weather['weather'][0]['description']
        print(f" {temp}\n {deskr}")
        await message.answer(f'просто осень скоро в {city} \n '
                         f'сегодня {date} температура {temp} на {stime}\n'
                         f'{deskr}')
    except KeyError as e:
        print(f"Error fetching weather data: {e}")
        print(f"{city}\n{weather}")
        await message.answer("Не удалось получить данные о погоде. Попробуйте еще раз.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"{city} счетчик {count}")
        await message.answer("Произошла ошибка. Попробуйте еще раз.")
#Прописываем хендлер и варианты ответов:

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://vet-centre.by/wp-content/uploads/2016/11/kot-v-luchah-eti-udivitelnye-kotiki.jpg',
            'https://vet-centre.by/wp-content/uploads/2016/11/kot-s-myshyu-eti-udivitelnye-kotiki.jpg',
            'https://n1s2.hsmedia.ru/f0/c9/60/f0c96065f1e50771c40113e2324af266/823x1200_0xac120003_9211641921663938997.jpeg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())