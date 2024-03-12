from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, MediaGroupFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ContentType, CallbackQuery
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
    await message.answer('Здравствуйте, этот бот подписывает вас на салон епта')

@dp.message_handler(content_types=ContentType.ANY)
async def handle_message(message: types.Message):
    try:
        if db.get_user(message.from_user.id)[4] == 1:
            # create a post and post to subscribers
            all_subs = db.get_all_subscribers()
            postid = db.write_post(message.message_id, message.text)
            for sub in all_subs:
                messagetosave = await message.send_copy(chat_id=sub[1])
                db.link_post_to_message(messagetosave.message_id, postid)

            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("Удалить", callback_data=f'deltepost{postid}')
            markup.add(item1)
            await message.answer('Пост успешно рассылан епта')
        else:
            await message.answer('I am not an admin')


    except Exception as e:
        print(e)
@dp.callback_query_handler(str.startswith('deletepost'))
async def delete_post(call: CallbackQuery):
    await call.message.edit_text("Удалено")

    for post in db.get_all_posts_by_postid(int(call.text[10:])):
        await bot.delete_message(post[1])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
