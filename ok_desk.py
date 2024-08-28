import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import json

from config import TOKEN, OK_DESK, api_key_q

# Вставьте сюда ваш токен телеграм-бота и API-ключ для TheCatAPI

bot = Bot(token=TOKEN)
dp = Dispatcher()

def det_quotes():
    url = f"https://favqs.com/api/qotd"
    headers = {f'Authorization: Token token={api_key_q}'}
    response = requests.get(url)
    return response.json()

def get_okdesk_case(case):
    api_key = OK_DESK
    #  адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
    url = f"https://service.adv-t.ru/api/v1/issues/{case}?api_token={api_key}"
    #  для получения результата нам понадобится модуль requests
    response = requests.get(url)
    if response.status_code != 200:
        return None
    # print(f"кейс {case} имеет состояние: {response.json()}")
    #  прописываем формат возврата результата
    return response.json()


@dp.message(Command("start"))
async def start_command(message: Message):
   await message.answer("Привет! Напиши мне номер заявки, и я пришлю тебе её детали.")

@dp.message()
async def send_case_info(message: Message):
    case = int(message.text)
    case_info = get_okdesk_case(case)
    if case_info and not 'errors' in case_info:
        observers = case_info['observers']
        names = [observer['name'] for observer in observers]
        names_str = ', '.join(names)
        info = (
                f"Тема: {case_info['title']}\n"
                f"Создана {case_info['created_at']}\n"
                f"Статус: {case_info['status']['name']}\n"
                f"Приоритет: {case_info['priority']['name']}\n"
                f"Исполнители: {names_str}"
            )
        await message.answer (info)
    else:
        await message.answer("кейс не найден. Попробуйте еще раз.")
    try:
        quote = det_quotes()
        await message.answer(f"Кстати: {quote['quote']['body']} \n Автор {quote['quote']['author']}")
    except:
        await message.answer("Цитаты не будет")





async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())
