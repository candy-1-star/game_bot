from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buttons = [
    [KeyboardButton(text='🎫 -> Ваша реферальная ссылка')]
]

kb2 = ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder='📌 -> Введите промокод'
)