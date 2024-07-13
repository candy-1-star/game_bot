from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

buttons = [
    [KeyboardButton(text='📈 -> Cтатистика')],
    [KeyboardButton(text='🔖 -> Задания')],
    [KeyboardButton(text='💎 -> Капсулы')],
    [KeyboardButton(text='🎫 -> Ваша реферальная ссылка')],
    [KeyboardButton(text='🔥 -> Промокоды')]
]
kb1 = ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder='📌 -> Введите промокод'
)