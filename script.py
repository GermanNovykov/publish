from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, MediaGroupFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils import executor
from aiogram.utils.markdown import hide_link
from aiogram.utils.deep_linking import decode_payload
from aiogram_media_group import media_group_handler
from typing import List
from sqlight import DBclass

db = DBclass('db.db')
TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    db.create_user(message.from_user.id, message.from_user.first_name)
    await message.answer('Hi man')

@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        if db.get_user(message.from_user.id)[4] == 1:
            await message.answer('I am admin')
        else:
            await message.answer('I am not an admin')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
