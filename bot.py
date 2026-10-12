import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from google import genai

# Считываем токены из окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Здарова! Я твой ИИ-бот, запущенный в облаке 24/7. Спроси меня о чем угодно!")

@dp.message(F.text)
async def chat_with_ai(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Ой, что-то пошло не так при обращении к ИИ.")

async def main():
    print("ИИ-бот запущен в облаке...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
