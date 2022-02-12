import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import pytz
from datetime import datetime


API_KEY = '4d373ed1172a59fe8c97395bdb48729e'

bot = Bot('5043014128:AAGZn34I6n1sALs6dxyWC26vIQzeCLRRgYo')
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Привет {message.from_user.first_name}")
    await message.answer("Чтобы узнать погоду введите /find_w")


@dp.message_handler(commands=["find_w"])
async def start_command(message: types.Message):
    await message.answer("Введите название города:")




@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_KEY}&units=metric"
        )
        data = r.json()
        datetime_now = datetime.fromtimestamp(data['dt'])
        country = data['sys']['country']
        city = data["name"]
        temp = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
        
        await message.reply(f"<strong><u>Погода на время:</u></strong>  {datetime_now}\n\n"
              f"<strong><u>Погода в городе:</u></strong>  {city} ({country})\n\n<strong><u>Температура:</u></strong>  {temp} C° <strong>{wd}</strong>\n\n"
              f"<strong><u>Влажность:</u></strong>  {humidity}%\n\n<strong><u>Давление:</u></strong>  {pressure} мм.рт.ст\n\n<strong><u>Скорость ветра:</u></strong>  {wind} м/с\n\n"
              f"<strong><u>Рассвет:</u></strong> {sunrise}\n\n<strong><u>Закат:</u></strong> {sunset}", parse_mode='HTML')
        await message.answer('Хорошего дня!')
    except Exception as ex:
        print(ex) 
        await message.reply("Проверьте название города!!!")


if __name__ == '__main__':
    executor.start_polling(dp)
