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

# logging.basicConfig(level=logging.INFO)
db = DBclass('db.db')
TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Hi man')
    db.create_user(message.from_user.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
