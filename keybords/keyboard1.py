from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

buttons1 = [
    [KeyboardButton(text='📈 -> Статистика')],
    [KeyboardButton(text='❤️ -> Мои карточки')],
    [KeyboardButton(text='🔖 -> Задания')],
    [KeyboardButton(text='💎 -> Капсулы')],
    [KeyboardButton(text='🎫 -> Ваша реферальная ссылка')],
    [KeyboardButton(text='🔥 -> Промокоды')]
]
kb1 = ReplyKeyboardMarkup(
    keyboard=buttons1,
    resize_keyboard=True
)

buttons2 = [
    [KeyboardButton(text='🎫 -> Ваша реферальная ссылка')]
]

kb2 = ReplyKeyboardMarkup(
    keyboard=buttons2,
    resize_keyboard=True
)

buttons3 = [
    [KeyboardButton(text='🔮 -> Капсула 1')],
    [KeyboardButton(text='🔮 -> Капсула 2')],
    [KeyboardButton(text='🔮 -> Капсула 3')]
]
kb3 = ReplyKeyboardMarkup(
    keyboard=buttons3,
    resize_keyboard=True,
)

buttons4 = [
    [KeyboardButton(text='✅ -> Открыть')],
    [KeyboardButton(text='🔚 -> Вернуться в главное меню')]
]
kb4 = ReplyKeyboardMarkup(
    keyboard=buttons4,
    resize_keyboard=True
)

kb5 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Все карточки",
            callback_data="all_cart"
        )],
        [InlineKeyboardButton(
            text="Common карточки",
            callback_data="common_cart"
        )],
        [InlineKeyboardButton(
            text="Rare карточки",
            callback_data="rare_cart"
        )],
        [InlineKeyboardButton(
            text="Epic карточки",
            callback_data="epic_cart"
        )]
    ]
)

buttons_ex = [
    [KeyboardButton(text='🔚 -> Вернуться в главное меню')]
]
kb_ex = ReplyKeyboardMarkup(
    keyboard=buttons_ex,
    resize_keyboard=True
)

# [InlineKeyboardButton(
#     text="<<",
#     callback_data="<<"
# )],
# [InlineKeyboardButton(
#     text="<<<",
#     callback_data="<<<"
# )],