import asyncio
import sqlite3
from random import choices, choice

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload

from keybords.keyboard1 import kb1, kb3, kb4, kb5, kb8, kb9, kb_tr, kb_ex

bot = Bot(token='7343617128:AAHyW2P6KApMkQlBGf2vIGlNPl7CrYYmcwA', default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

con = sqlite3.connect('tg.db')
cur = con.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS Users (
ids INTEGER PRIMARY KEY,
many INTEGER NOT NULL,
common INTEGER NOT NULL,
rare INTEGER NOT NULL, 
epic INTEGER NOT NULL
)''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Promo (
id_us INTEGER PRIMARY KEY,
promo1 INTEGER NOT NULL,
promo2 INTEGER NOT NULL, 
promo3 INTEGER NOT NULL
)''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Carts (
id_us1 INTEGER NOT NULL,
name TEXT NOT NULL,
status TEXT NOT NULL,
photo TEXT NOT NULL,
caption TEXT NOT NULL, 
iteration INTEGER NOT NULL DEFAULT 1,
i INTEGER NOT NULL DEFAULT 0
)
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Sessions (
id_us2 INTEGER PRIMARY KEY,
session INTEGER NOT NULL,
message_id INTEGER NOT_NULL
)
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Ref_count (
id_us3 INTEGER PRIMARY KEY,
counter INTEGER NOT NULL
)
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS Tr_sessions (
id_us4 INTEGER PRIMARY KEY,
id_us5 INTEGER NOT NULL, 
cart1 TEXT NOT NULL,
cart2 TEXT NOT NULL,
status1 TEXT NOT NULL,
status2 TEXT NOT NULL
)
''')
con.commit()

common1 = ['Lada', 'NISSAN', 'Volvo']
rare1 = ['Isuzu', 'Jeep', 'KIA']
epic1 = ['Toyota', 'Lexus']

items = ['common', 'rare', 'epic']
weights = [50, 30, 20]


@dp.message(Command('start'))
async def start_command(message: Message, command: Command = None):
    try:
        cur.execute('INSERT INTO Users (ids, many, common, rare, epic) VALUES (?, ?, ?, ?, ?)',
                    (message.from_user.id, 0, 0, 0, 0))
        con.commit()
        cur.execute('INSERT INTO Promo (id_us, promo1, promo2, promo3) VALUES (?, ?, ?, ?)',
                    (message.from_user.id, 0, 0, 0))
        con.commit()
        cur.execute('INSERT INTO Sessions (id_us2, session, message_id) VALUES (?, ?, ?)',
                    (message.from_user.id, 0, 0))
        con.commit()
        cur.execute('INSERT INTO Ref_count (id_us3, counter) VALUES (?, 0)', (message.from_user.id,))
        con.commit()
        cur.execute('INSERT INTO Tr_sessions (id_us4, id_us5, cart1, cart2, status1, status2) VALUES (?, ?, ?, ?, ?, ?)',
                    (message.from_user.id, 0, 'None', 'None', 'None', 'None'))
        con.commit()
        await message.reply(f'Привет, <u>@{message.from_user.username}</u>!', reply_markup=kb1)

        if command.args:
            args = command.args
            reference = decode_payload(args)

            await message.reply(f'Теперь вы и ваш реферал получат по 1000 many')
            cur.execute('UPDATE Users SET many = many + 1000 WHERE ids = ?', (reference,))
            con.commit()
            cur.execute('UPDATE Users SET many = many + 1000 WHERE ids = ?', (message.from_user.id,))
            con.commit()
            cur.execute('UPDATE Ref_count SET counter = counter + 1 WHERE id_us3 = ?', (reference,))
    except:
        await message.reply(f'Привет, <u>@{message.from_user.username}</u>!', reply_markup=kb1)


@dp.message(F.text == '📈 -> Статистика')
async def status_msg_msg(message: Message):
    try:
        cur.execute('SELECT * FROM Users WHERE ids = ?', (message.from_user.id,))
        user = cur.fetchone()
        cur.execute('SELECT * FROM Promo WHERE id_us = ?', (message.from_user.id,))
        promo_c = cur.fetchone()
        cur.execute('SELECT * FROM Ref_count WHERE id_us3 = ?', (message.from_user.id,))
        ref = cur.fetchone()
        if user and promo_c:
            ids, many, common, rare, epic = user
            id_us, promo1, promo2, promo3 = promo_c
            id_us3, counter = ref
            await message.reply(f'''
<b>🔐 Выши данные 🔐</b>
Id - <em>{ids}</em>
<b>💸Ваши платежные средства💸</b>
Many - <em>{many}</em>
<b>💎Капсулы💎</b>
Common - <em>{common}</em>
Rare - <em>{rare}</em>
Epic - <em>{epic}</em>
<b>🔖Промокоды🔖</b>
Использовано промокодов - <em>{promo1 + promo2 + promo3}</em>
<b>🤝Реферальная система🤝</b>
Всего приглашено пользователей - {counter}
        ''')
        else:
            await message.reply('Вы НЕ были зарегистрированы')
    except:
        pass


@dp.message(F.text == '🔖 -> Задания')
async def mession_msg(message: Message):
    pass


@dp.message(F.text == '🎫 -> Ваша реферальная ссылка')
async def mession_msg_1(message: Message):
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    await message.reply(f'Вот ваша реферальная ссылка -> {link}', reply_markup=kb1)


@dp.message(F.text == '💎 -> Капсулы')
async def random_msg(message: Message):
    await message.reply('''
Чтобы купить капсулу вам нужно 300 <b>many</b>!
При открытии капсул вам будут выпадать <b>карточки</b>!
Карточки деляться на три типа по редкости выпадения:
Common - 50%
Rare - 30%
Epic - 20%
''', reply_markup=kb3)


@dp.message(F.text == '❤️ -> Мои карточки')
async def random_1(message: Message):
    await message.answer("Какие карты хотите посмотреть?", reply_markup=kb5)


@dp.callback_query(F.data == 'epic_cart')
async def epic_rare(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        a = cur.fetchone()[0]
        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "epic" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts
        photo1 = FSInputFile(photo)

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]

        if total_users == 1:
            kb6 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/1",
                        callback_data="counter"
                    )]
                ]
            )

        else:
            kb6 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>3"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )

        msg = await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, caption=caption, photo=photo1,
                                                  reply_markup=kb6)
        con.execute(
            F'UPDATE Sessions SET session = 1, message_id = {msg.message_id} WHERE id_us2 = ?',
            (callback_query.from_user.id,))
        con.commit()
    except:
        await callback_query.bot.send_message('У вас еще нет карточек, но вы можете их купить!')


@dp.callback_query(F.data == ">>3")
async def strela_DD3(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]

        con.execute('UPDATE Sessions SET session = session + 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "epic" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>3"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<3"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<3"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>3"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )
            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<3"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<3"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == ">>>3")
async def strela_DDD3(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = {total_users} WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "epic" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>3"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<3"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<3"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>3"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<3"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<3"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<3")
async def strela_qq2(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = session - 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "epic" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data='>>3'
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<3"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<3"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>3"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<3"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<3"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<<3")
async def strela_qq2(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "epic"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "epic" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>3"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<3"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<3"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>3"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>3"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<3"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<3"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == 'rare_cart')
async def common_rare(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        a = cur.fetchone()[0]
        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "rare" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts
        photo1 = FSInputFile(photo)

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]

        if total_users == 1:
            kb6 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/1",
                        callback_data="counter"
                    )]
                ]
            )

        else:
            kb6 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>2"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )

        msg = await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, caption=caption, photo=photo1,
                                                  reply_markup=kb6)
        con.execute(
            F'UPDATE Sessions SET session = 1, message_id = {msg.message_id} WHERE id_us2 = ?',
            (callback_query.from_user.id,))
        con.commit()
    except:
        await callback_query.bot.send_message('У вас еще нет карточек, но вы можете их купить!')


@dp.callback_query(F.data == ">>2")
async def strela_DD2(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]

        con.execute('UPDATE Sessions SET session = session + 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "rare" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>2"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<2"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<2"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>2"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )
            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<2"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<2"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == ">>>2")
async def strela_DDD2(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = {total_users} WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "rare" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>2"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<2"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<2"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>2"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<2"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<2"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<2")
async def strela_qq2(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = session - 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "rare" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data='>>2'
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<2"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<2"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>2"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<2"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<2"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<<2")
async def strela_qq2(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "rare"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "rare" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>2"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<2"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<2"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>2"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>2"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<2"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<2"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == 'common_cart')
async def common_cart(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        a = cur.fetchone()[0]
        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "common" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts
        photo1 = FSInputFile(photo)

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]

        if total_users == 1:
            kb6 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/1",
                        callback_data="counter"
                    )]
                ]
            )

        else:
            kb6 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )
        msg = await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, caption=caption, photo=photo1,
                                                  reply_markup=kb6)
        con.execute(
            F'UPDATE Sessions SET session = 1, message_id = {msg.message_id} WHERE id_us2 = ?',
            (callback_query.from_user.id,))
        con.commit()
    except:
        await callback_query.bot.send_message('У вас еще нет карточек, но вы можете их купить!')


@dp.callback_query(F.data == ">>1")
async def strela_DD1(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]

        con.execute('UPDATE Sessions SET session = session + 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "common" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<1"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<1"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )
            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<1"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<1"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == ">>>1")
async def strela_DDD1(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = {total_users} WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "common" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<1"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<1"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<1"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<1"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<1")
async def strela_qq1(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = session - 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "common" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<1"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<1"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<1"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<1"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<<1")
async def strela_qqq1(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = "common"', (callback_query.from_user.id,))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = "common" AND i = {a}',
                    (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<1"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<1"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>1"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>1"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<1"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<1"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "all_cart")
async def all_cart(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT * FROM Carts WHERE id_us1 = ? AND i = 1', (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts
        photo1 = FSInputFile(photo)

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ?', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]

        if total_users == 1:
            kb6 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/1",
                        callback_data="counter"
                    )]
                ]
            )

        else:
            kb6 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )

        msg = await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, caption=caption, photo=photo1,
                                                  reply_markup=kb6)
        con.execute(
            F'UPDATE Sessions SET session = 1, message_id = {msg.message_id} WHERE id_us2 = ?',
            (callback_query.from_user.id,))
        con.commit()
    except:
        await callback_query.message.reply(text='У вас еще нет карточек, но вы можете их купить!')


@dp.callback_query(F.data == ">>")
async def strela_DD(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ?', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]

        con.execute('UPDATE Sessions SET session = session + 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND i = {session}', (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )
            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == ">>>")
async def strela_DDD(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ?', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = {total_users} WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND i = {session}', (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<")
async def strela_qq(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ?', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = session - 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND i = {session}', (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<<")
async def strela_qqq(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ?', (callback_query.from_user.id,))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND i = {session}', (callback_query.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts

        photo1 = FSInputFile(photo)

        if session == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"{session}/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=caption,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.message(F.text == '🔮 -> Капсула 1')
async def random_1(message: Message):
    await message.reply('''
Тут содержаться 8 карточек!
<u>Lada</u>  ->  Common  ->  50%
<u>NISSAN</u>  ->  Common  ->  50%
<u>Volvo</u>  ->  Common  ->  50%
<u>Isuzu</u>  -> Rare  ->  30%
<u>Jeep</u>  ->  Rare  ->  30%
<u>KIA</u>  ->  Rare  ->  30%
<u>Toyota</u>  ->  Epic  ->  20%
<u>Lexus</u>  ->  Epic  ->  20%
Цена - 300
    ''', reply_markup=kb4)


@dp.message(F.text == '✅ -> Открыть')
async def k1def(message: Message):
    cur.execute('SELECT name FROM Carts WHERE id_us1 = ?', (message.from_user.id,))
    result1 = cur.fetchall()
    cur.execute("SELECT many FROM Users WHERE ids = ?", (message.from_user.id,))
    result = cur.fetchone()
    if 300 <= result[0]:
        con.execute('UPDATE Users SET many = many - 300 WHERE ids = ?', (message.from_user.id,))
        con.commit()
        kart1 = choices(items, weights=weights)[0]
        if kart1 == 'common':
            kart = choice(common1)
        elif kart1 == 'rare':
            kart = choice(rare1)
        elif kart1 == 'epic':
            kart = choice(epic1)

        # common1 = ['Lada', 'NISSAN', 'Volvo']
        # rare1 = ['Isuzu', 'Jeep', 'KIA']
        # epic1 = ['Toyota', 'Lexus']

        if kart == 'Lada':
            photo777 = 'media/v-rossii-nachalos-testirovanie-avtopilota-dlya-lada-vesta-1.jpg'
        elif kart == 'NISSAN':
            photo777 = 'media/f33cffb36f991c357a95818e76875254.jpg'
        elif kart == 'Volvo':
            photo777 = 'media/b549ef86bfa3e9568818231465aed573.jpeg'
        elif kart == 'Isuzu':
            photo777 = 'media/66755.jpg'
        elif kart == 'Jeep':
            photo777 = 'media/1701755805_sportishka-com-p-krasivie-mashini-vnedorozhniki-pinterest-1.jpg'
        elif kart == 'KIA':
            photo777 = 'media/1693069229_funnyart-club-p-avtomobil-kia-k5-krasivo-2.jpg'
        elif kart == 'Toyota':
            photo777 = 'media/2017_toyota_prius_prime_advanced_front_three_quarter_06.jpg'
        elif kart == 'Lexus':
            photo777 = 'media/388736-mashina-leksus-7.jpg'

        if (kart,) in result1:

            cur.execute('UPDATE Carts SET iteration = iteration + 1 WHERE id_us1 = ? AND name = ?',
                        (message.from_user.id, kart))
            con.commit()
            cur.execute('SELECT iteration FROM Carts WHERE id_us1 = ? AND name = ?', (message.from_user.id, kart))
            result2 = cur.fetchall()
            photo1 = FSInputFile(photo777)
            caption = f'''
<u>{kart}</u>  

Редкость <b>{kart1}</b>      
Карт всего <b>{result2[0][0]}</b>
                        '''
            cur.execute('UPDATE Carts SET caption = ? WHERE id_us1 = ? AND name = ?',
                        (caption, message.from_user.id, kart))
            con.commit()
        else:
            iteration = 1
            photo1 = FSInputFile(photo777)
            photo2 = photo777
            caption = f'''
<u>{kart}</u>  

Редкость <b>{kart1}</b>      
Карт всего <b>{iteration}</b>
            '''
            cur.execute('INSERT INTO Carts (id_us1, name, status, photo, caption) VALUES (?, ?, ?, ?, ?)',
                        (message.from_user.id, kart, kart1, photo2, caption))
            con.commit()
            cur.execute('UPDATE Carts SET i = i + 1 WHERE id_us1 = ?', (message.from_user.id,))
            con.commit()

        await bot.send_photo(photo=photo1, chat_id=message.chat.id, caption=caption)
        con.execute(f'UPDATE Users SET {kart1} = {kart1} + 1 WHERE ids = ?', (message.from_user.id,))
        con.commit()
    else:
        await message.reply('У вас недостаточно сретств', reply_markup=kb1)


@dp.message(F.text == '🔚 -> Вернуться в главное меню')
async def exit_def(message: Message):
    await message.reply(f'Привет, <u>@{message.from_user.username}</u>!', reply_markup=kb1)


class PromoCodeState(StatesGroup):
    waiting_for_promo_code = State()


@dp.message(F.text == '🔥 -> Промокоды')
async def promo_codes_msg(message: Message, state: FSMContext):
    await message.reply('Введите, пожалуйста, ваш промокод!', reply_markup=kb_ex)
    await state.set_state(PromoCodeState.waiting_for_promo_code)


@dp.message(StateFilter(PromoCodeState.waiting_for_promo_code))
async def promo_event(message1: Message, state: FSMContext):
    cur.execute('SELECT * FROM Promo WHERE id_us = ?', (message1.from_user.id,))
    promo_c = cur.fetchone()
    id_us, promo1, promo2, promo3 = promo_c
    promo_codes = {
        'xdcBboUiKKZY24UoCBgZqelRkJ95S1s': '100',
        'jOEfIVj0haEXMVHxfCGcc8N9JloZ8D7': '1000',
        'tpb6uuLU3yJ33uqL2UdQjbvYJbYQcLh': '10000'
    }

    promo_codes1 = {
        'xdcBboUiKKZY24UoCBgZqelRkJ95S1s': 'promo1',
        'jOEfIVj0haEXMVHxfCGcc8N9JloZ8D7': 'promo2',
        'tpb6uuLU3yJ33uqL2UdQjbvYJbYQcLh': 'promo3'
    }

    promo_codes2 = {
        'promo1': promo1,
        'promo2': promo2,
        'promo3': promo3
    }
    if message1.text in promo_codes and promo_codes2[promo_codes1[message1.text]] < 1:
        cur.execute(f'UPDATE Users SET many = many + {promo_codes[message1.text]} WHERE ids = ?',
                    (message1.from_user.id,))
        cur.execute(
            f'UPDATE Promo SET {promo_codes1[message1.text]} = {promo_codes1[message1.text]} + 1 WHERE id_us = ?',
            (message1.from_user.id,))
        con.commit()
        await message1.reply(
            f'Вам промокод корректен и вы получаете {promo_codes[message1.text]} many.', reply_markup=kb1)
        await state.clear()
    else:
        await message1.reply('Увы...Такого промокода мы еще не придумали...', reply_markup=kb1)
        await state.clear()


class TradeState(StatesGroup):
    waiting_for_tr = State()


@dp.message(F.text == '🤝 -> Обмен')
async def traide_1(message: Message, state: FSMContext):
    await message.reply('Введите id пользователя, с которым вы хотите совершить сделку!', reply_markup=kb_ex)
    await state.set_state(TradeState.waiting_for_tr)


@dp.message(TradeState.waiting_for_tr)
async def traide_2(message: Message, state: FSMContext):
    id = message.text
    cur.execute('SELECT ids FROM Users')
    ids1 = cur.fetchall()
    if (int(id),) in ids1:
        cur.execute(
            'UPDATE Tr_sessions SET id_us5 = ? WHERE id_us4 = ?',
            (message.from_user.id, id))
        con.commit()
        await bot.send_message(chat_id=int(id),
                               text=f'Привет, пользователь {message.from_user.username} хочет совершить с тобой '
                                    f'сделку! Хочешь сделку?',
                               reply_markup=kb8)
        await state.clear()

    else:
        await message.reply('Увы, такого пользователя нет!')


class TradeState1(StatesGroup):
    waiting_for_tr1 = State()
    waiting_for_tr2 = State()


@dp.callback_query(F.data == 'yes')
async def traide_yes(callback_query: CallbackQuery, state: FSMContext):
    cur.execute('SELECT id_us4 FROM Tr_sessions WHERE id_us5 = ?', (callback_query.from_user.id,))
    id_us4 = cur.fetchall()[0][0]
    await callback_query.bot.send_message(chat_id=id_us4,
                                          text=f'Пользователь {callback_query.from_user.username} согласен на '
                                               f'сделаку! Выбери какую карточку ты хочешь поменять, написав название!')
    await state.set_state(TradeState1.waiting_for_tr1)


@dp.message(StateFilter(TradeState1.waiting_for_tr1))
async def traide_yes1(message: Message, state: FSMContext):
    try:
        name_c = message.text
        cur.execute('SELECT * FROM Carts WHERE id_us1 = ? AND name = ?', (message.from_user.id, name_c))
        cart = cur.fetchone()
    except:
        await message.reply('Увы, такой карточки у вас нет! Попробуйте еще раз!')
    else:
        id_us1, name, status, photo, caption, iteration, i = cart
        cur.execute('UPDATE Tr_sessions SET cart1 = ?, status1 = ? WHERE id_us4 = ?',
                    (name, status, message.from_user.id))
        con.commit()

        cur.execute('SELECT id_us5 FROM Tr_sessions WHERE id_us4 = ?', (message.from_user.id,))
        id_us5 = cur.fetchone()[0]
        await message.bot.send_message(chat_id=id_us5,
                                       text=f'Пользователь {message.from_user.username} выбрал карточку {name_c}, '
                                            f'теперь твоя очередь. Введи название своей карточки', reply_markup=kb9)
        await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

con.commit()
con.close()
cur.close()
