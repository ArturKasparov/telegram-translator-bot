from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, Message, KeyboardButton
from aiogram.filters import Command

# Используем асинхронный переводчик
from aiogoogletrans import Translator

router = Router()
translator = Translator()

user_lang = {}

languages = {
    "Английский 🇬🇧": "en",
    "Русский 🇷🇺": "ru",
    "Немецкий 🇩🇪": "de",
    "Французский 🇫🇷": "fr",
    "Українська 🇺🇦": "uk"
}

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=lang)] for lang in languages.keys()],
    resize_keyboard=True
)

@router.message(Command("start"))
async def start(message: Message):
    user_lang[message.from_user.id] = "en"
    await message.answer(
        "Привет! Отправь мне текст, и я переведу его. Выбери язык перевода:",
        reply_markup=keyboard
    )

@router.message(lambda message: message.text in languages.keys())
async def set_language(message: Message):
    user_lang[message.from_user.id] = languages[message.text]
    await message.answer(f"Язык перевода изменен на {message.text}!")

@router.message()
async def translate_text(message: Message):
    lang = user_lang.get(message.from_user.id, "en")

    # Теперь используем `await`, потому что `translate` асинхронный
    translation = await translator.translate(message.text, dest=lang)

    await message.answer(f"Перевод ({lang}): {translation.text}")
