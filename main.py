import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = "8688724544:AAFut5vPRGFp1LxzrR-Wqe9gecbKixVTpCc"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())