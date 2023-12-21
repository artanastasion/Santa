import logging
import bot_token
from aiogram import Bot, Dispatcher, types, executor

import sqlite_db
import dialog

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token.BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    await sqlite_db.db_connect()
    print('connection successful')


@dp.message_handler(commands=["participate"])
async def cmd_start_group(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        await sqlite_db.add_user(tg_id_user=message.from_user.id, username=message.from_user.username,
                                 room=message.chat.id)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.chat.type == "private":
        await bot.send_message(message.from_user.id, text=dialog.start_private)
    if message.chat.type in ["group", "supergroup"]:
        await bot.send_message(message.chat.id, text=dialog.start_group)


@dp.message_handler(commands=["play"])
async def play_start(message: types.Message):
    if message.from_user.id == 644724972 and message.chat.type == "group":
        count = await sqlite_db.count_part(message.chat.id)
        await sqlite_db.start_play(count, message.chat.id)
        await message.reply(
            "А вы нарядили уже ёлку?🎄 Кстати у нее песня классная есть: УЮТНОЕЕЕЕ КАФЭЭЭЭЭЭЭЭ😹)))))) Я жду, что вы напишете мне в лс: @ChillSanta_bot🥰")
    else:
        await message.reply("охохо, я вижу тут одного гангстера🙈, игра сейчас не может начаться")


@dp.message_handler(commands=["get_recipient"])
async def get_recipient(message: types.Message):
    if message.chat.type == "private":
        recipient = await sqlite_db.check_username_recipient(message.from_user.id)
        if not recipient:
            await bot.send_message(message.from_user.id, text="Ты еще не участвуешь в игре, тебе следует прислать /participate в чате со своими друзьями")
        else:
            str_recipient = ', '.join(list(map(lambda x: f'@{x}', recipient)))
            text = dialog.get_recipient_text + str_recipient + "\nКогда ты будешь готов поднять настроение своему другу, пиши мне /sent"
            await bot.send_message(message.from_user.id, text=text)


@dp.message_handler(commands=["sent"])
async def sent(message: types.Message):
    if message.chat.type == "private":
        recipient_id = await sqlite_db.check_tg_id_recipient(message.from_user.id)
        recipient = await sqlite_db.check_username_recipient(message.from_user.id)
        str_recipient = ', '.join(list(map(lambda x: f'@{x}', recipient)))
        text = dialog.sent_text_to + "\n" + str_recipient + f" теперь {'знают' if len(recipient) > 1 else 'знает'}, что тайный Санта в ближайшем будущем отдаст подарок!"

        await bot.send_message(message.from_user.id, text=text)

        for i in range(len(recipient)):
            await bot.send_message(recipient_id[i], text=dialog.sent_text_from)


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await bot.send_message(message.chat.id, text=dialog.help_text)


@dp.message_handler(commands=["received"])
async def received(message: types.Message):
    await bot.send_message(message.from_user.id, text=dialog.received_from)
    recipient_id = await sqlite_db.check_tg_id_recipient(message.from_user.id)
    for i in range(len(recipient_id)):
        await bot.send_message(recipient_id[i], text=dialog.received_to)
        await sqlite_db.delete(recipient_id[i])


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
