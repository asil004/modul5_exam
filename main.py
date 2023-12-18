import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

from db import Session, User, Message_

load_dotenv('.env')

TOKEN = os.getenv('TOKEN')
router = Router()


# start comandani ishga tushursa
@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    session = Session()
    user_list = session.query(User).filter(User.user_telegram_id == str(message.from_user.id)).first()
    if not user_list:
        user_telegram_id = message.from_user.id
        username = message.from_user.username
        created = message.date

        user = User(user_telegram_id=user_telegram_id, username=username, created=created)
        session = Session()
        session.add(user)
        session.commit()
        await message.reply("Sizning ma'lumotlaringiz bazaga saqlandi!")
    else:
        await message.answer('Siz malumotlar bazasida borsiz!')


# user haqida infolar chiqadi
@router.message(Command('info'))
async def user_list(message: types.Message):
    session = Session()
    user_list = session.query(User).filter(User.user_telegram_id == str(message.from_user.id)).first()
    if user_list:
        res = f"Username: @{user_list.username}\nId: {user_list.user_telegram_id}\nDate: {user_list.created}\n"
    else:
        res = "Bunday foydalanuvchi topilmadi"
    await message.answer(res)


@router.message()
async def chat_message(message: types.Message):
    # gruppaga aynan message yozilsa shuni saqlaydi boshqa narsalarni saqlamaydi
    if str(message.content_type) == 'ContentType.TEXT':
        text = message.text
        created = message.date
        mes = Message_(user_id=message.from_user.id, text=text, created=created)
        session = Session()
        session.add(mes)
        session.commit()
        await message.reply(f"Siz yozgan xabar bazaga saqlandi!")


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
