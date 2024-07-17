from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

buttons1 = [
    [KeyboardButton(text='📈 -> Статистика')],
    [KeyboardButton(text='❤️ -> Мои карточки')],
    [KeyboardButton(text='💎 -> Капсулы')],
    [KeyboardButton(text='🤝 -> Обмен')],
    [KeyboardButton(text='🔖 -> Задания')],
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
    [KeyboardButton(text='🔮 -> Капсула 1')]
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

kb8 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="✅",
            callback_data="yes1"
        )],
        [InlineKeyboardButton(
            text="❌",
            callback_data="no1"
        )]
    ]
)

kb9 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="✅",
            callback_data="yes2"
        )],
        [InlineKeyboardButton(
            text="❌",
            callback_data="no2"
        )]
    ]
)

buttons_tr = [
    [KeyboardButton(text='✅ -> Да')],
    [KeyboardButton(text='❌ -> Нет')]
]

kb_tr = ReplyKeyboardMarkup(
    keyboard=buttons_tr,
    resize_keyboard=True
)

buttons_ex = [
    [KeyboardButton(text='🔚 -> Вернуться в главное меню')]
]
kb_ex = ReplyKeyboardMarkup(
    keyboard=buttons_ex,
    resize_keyboard=True
)