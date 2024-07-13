from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buttons = [
    [KeyboardButton(text='🔮 -> Капсула 1')],
    [KeyboardButton(text='🔮 -> Капсула 2')],
    [KeyboardButton(text='🔮 -> Капсула 3')]
]
kb3 = ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder='📌 -> Введите промокод'
)