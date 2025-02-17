import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from googletrans import Translator

TOKEN = "7941812938:AAEYprdhc5FnOLzf4qxbT7r41VvQZcp0N4o"  # token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
translator = Translator()

# keyboard for choosing preferred languagegi
languages = {
    "Английский 🇬🇧": "en",
    "Русский 🇷🇺": "ru",
    "Немецкий 🇩🇪": "de",
    "Французский 🇫🇷": "fr"
}
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for lang in languages.keys():
    keyboard.add(KeyboardButton(lang))

# we store every language used for a translation
user_lang = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_lang[message.from_user.id] = "en"  # english by default
    await message.answer(
        "Привет! Отправь мне текст, и я переведу его. Выбери язык перевода:",
        reply_markup=keyboard
    )

@dp.message_handler(lambda message: message.text in languages.keys())
async def set_language(message: types.Message):
    user_lang[message.from_user.id] = languages[message.text]
    await message.answer(f"Язык перевода изменен на {message.text}!")

@dp.message_handler()
async def translate_text(message: types.Message):
    lang = user_lang.get(message.from_user.id, "en")
    translation = translator.translate(message.text, dest=lang)
    await message.answer(f"Перевод ({lang}): {translation.text}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
