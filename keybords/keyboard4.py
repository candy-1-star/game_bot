from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buttons = [
    [KeyboardButton(text='✅ -> Открыть')],
    [KeyboardButton(text='🔚 -> Вернуться в главное меню')]
]
kb4 = ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True
)