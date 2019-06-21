#!/usr/bin/env python
# -- coding: utf-8 --

from telethon import TelegramClient, sync
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
import requests
from PIL import ImageDraw, Image, ImageFont
import time

celsius = '°C'
PATH = 'temperature_images'

location = 524901  # moscow
openweather_api_key = 'abcdefghi'

telegram_api_id = 1234567
telegram_api_hash = 'abcdefghi'

FONT_SIZE = 80
TEXT_Y_POSITION = 75

# create all avatars
for temperature in range(-99, 99, 1):
    raw = Image.new('RGBA', (250, 250), "black")
    parsed = ImageDraw.Draw(raw)
    length = len(str(temperature))
    if length == 1:
        x_start = 65
    if length == 2:
        x_start = 40
    if length == 3:
        x_start = 20

    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    parsed.text((x_start, TEXT_Y_POSITION), f'{temperature}{celsius}', align="center", font=font)
    raw.save(f'{PATH}/{temperature}.png', "PNG")


def get_temperature(weather_data):
    return round(weather_data['main']['temp'])


def get_weather(location, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?id={location}&units=metric&appid={api_key}'
    r = requests.get(url)
    return r.json()


client = TelegramClient('1', telegram_api_id, telegram_api_hash)
client.start()

last_temperature = -274

while True:
    weather_data = get_weather(location, openweather_api_key)
    temperature = get_temperature(weather_data)
    print(last_temperature, temperature)
    if temperature == last_temperature:
        time.sleep(15 * 60)
        continue

    client(DeletePhotosRequest(client.get_profile_photos('me')))
    file = client.upload_file(f'{PATH}/{temperature}.png')
    client(UploadProfilePhotoRequest(file))
    last_temperature = temperature
    time.sleep(15 * 60)
