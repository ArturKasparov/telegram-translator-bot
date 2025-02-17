import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from googletrans import Translator

TOKEN = "7941812938:AAEYprdhc5FnOLzf4qxbT7r41VvQZcp0N4o"
bot = Bot(token=TOKEN)
dp = Dispatcher()  # В aiogram 3.x Dispatcher создаётся без аргументов
translator = Translator()

# keyboard for choosing preferred languagegi
languages = {
    "Английский 🇬🇧": "en",
    "Русский 🇷🇺": "ru",
    "Немецкий 🇩🇪": "de",
    "Французский 🇫🇷": "fr"
}
keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=lang)] for lang in languages.keys()],
    resize_keyboard=True
)

# we store every language used for a translation
user_lang = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    user_lang[message.from_user.id] = "en"  # english by default
    await message.answer(
        "Привет! Отправь мне текст, и я переведу его. Выбери язык перевода:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text in languages.keys())
async def set_language(message: types.Message):
    user_lang[message.from_user.id] = languages[message.text]
    await message.answer(f"Язык перевода изменен на {message.text}!")

@dp.message()
async def translate_text(message: types.Message):
    lang = user_lang.get(message.from_user.id, "en")
    translation = translator.translate(message.text, dest=lang)
    await message.answer(f"Перевод ({lang}): {translation.text}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
