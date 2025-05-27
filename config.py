import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
load_dotenv()

TG_KEY = os.getenv('TG_API')
HOST = os.getenv('ip')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('DATABASE')
API_NN = os.getenv('API_NN')
KEY_NN = os.getenv('KEY_NN')

bot = Bot(token=TG_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
