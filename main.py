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

from keybords.keyboard1 import kb1, kb3, kb4, kb5, kb8, kb9, kb_ex

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
id_us10 INTEGER PRIMARY KEY,
id_us11 INTEGER NOT NULL,
name_us1 TEXT NOT NULL,
name_us2 TEXT NOT NULL, 
capt1 TEXT NOT NULL,
photo1 TEXT NOT NULL,
capt2 TEXT NOT NULL,
photo2 TEXT NOT NULL,
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
        cur.execute(
            'INSERT INTO Tr_sessions (id_us10, id_us11, name_us1, name_us2, capt1, photo1, capt2, photo2, status1, '
            'status2) VALUES (?, ?,'
            '?, ?, ?, ?, ?, ?, ?, ?)',
            (message.from_user.id, 0, message.from_user.username, 'None', 'None', 'None', 'None', 'None', 'None',
             'None'))
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


@dp.message(F.text == '🤝 -> Обмен')
async def trade_1(message: Message):
    try:
        cur.execute('SELECT * FROM Carts WHERE id_us1 = ? AND i = 1', (message.from_user.id,))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts
        photo1 = FSInputFile(photo)

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ?', (message.from_user.id,))
        total_users = cur.fetchone()[0]

        if total_users == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/1",
                        callback_data="counter"
                    )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

        else:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

        msg = await message.bot.send_photo(chat_id=message.chat.id,
                                           caption=name,
                                           photo=photo1,
                                           reply_markup=kb7)
        con.execute(
            F'UPDATE Sessions SET session = 1, message_id = {msg.message_id} WHERE id_us2 = ?',
            (message.from_user.id,))
        con.commit()
    except Exception as e:
        await message.reply(text='У вас еще нет карточек, но вы можете их купить!')
        print(e)


@dp.callback_query(F.data == ">>4")
async def strela_DD4(callback_query: CallbackQuery):
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
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<4"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<4"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )
            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<4"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<4"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == ">>>4")
async def strela_DDD4(callback_query: CallbackQuery):
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
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<4"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<4"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )]
                    ,
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<4"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<4"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<4")
async def strela_qq4(callback_query: CallbackQuery):
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
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<4"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<4"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<4"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<4"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<<4")
async def strela_qqq4(callback_query: CallbackQuery):
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
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<4"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<4"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>4"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>4"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<4"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<4"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )
    except:
        pass


class TradeState(StatesGroup):
    waiting_for_tr = State()


@dp.callback_query(F.data == 'vibrat')
async def traide_1(callback_query: CallbackQuery, state: FSMContext):
    cur.execute('SELECT iteration FROM Carts WHERE id_us1 = ? AND name = ?',
                (callback_query.from_user.id, callback_query.message.caption))
    iteration1 = cur.fetchone()[0]
    if iteration1 > 1:
        photo_object = str(callback_query.message.photo[0].file_id)

        cur.execute('UPDATE Tr_sessions SET capt1 = ?, photo1 = ? WHERE id_us10 = ?',
                    (callback_query.message.caption, photo_object,
                     callback_query.from_user.id))
        con.commit()

        await callback_query.message.reply('Введите имя пользователя, с которым вы хотите совершить сделку! Если бот не'
                                           'находит пользователя, то пуcть пользователь введет команду /start',
                                           reply_markup=kb_ex)
        await state.set_state(TradeState.waiting_for_tr)
    else:
        await callback_query.message.reply('Нет, у вас должно быть хотябы больше 1 карточки такого вида!')


@dp.message(TradeState.waiting_for_tr)
async def traide_2(message: Message, state: FSMContext):
    if message.text[0] == '@':
        name = message.text[1:]
    else:
        name = message.text
    cur.execute('SELECT name_us1 FROM Tr_sessions')
    names = cur.fetchall()
    if (name,) in names:
        cur.execute(f'SELECT id_us10 FROM Tr_sessions WHERE name_us1 = ?', (name,))
        id = cur.fetchall()[0][0]
        cur.execute(f'SELECT photo1 FROM Tr_sessions WHERE id_us10 = ?', (message.from_user.id,))
        photo = cur.fetchone()[0]

        cur.execute('UPDATE Tr_sessions SET name_us2 = ? WHERE id_us10 = ?',
                    (name, message.from_user.id))
        con.commit()

        await message.reply('Заявка на обмен была отправлена! Ожидайте!')

        await bot.send_photo(chat_id=int(id),
                             caption=f'Пользователь @{message.from_user.username} хочет совершить с тобой сделку!',
                             photo=photo,
                             reply_markup=kb8)
        await state.clear()

    else:
        await message.reply('Увы, такого пользователя нет!')


@dp.callback_query(F.data == 'no1')
async def traide3(callback_query: CallbackQuery):
    await callback_query.message.reply('Вы успешно отменили сделку!', reply_markup=kb_ex)

    cur.execute(f'SELECT id_us10 FROM Tr_sessions WHERE name_us2 = ?', (callback_query.from_user.username,))
    id = cur.fetchall()[0][0]

    await bot.send_message(chat_id=int(id), text='Пользователь не согласен на сделку!')


@dp.callback_query(F.data == 'yes1')
async def traide3(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT capt1 FROM Tr_sessions WHERE name_us2 = ?', (callback_query.from_user.username,))
        name777 = cur.fetchone()[0]

        cur.execute('SELECT status FROM Carts WHERE name = ?', (name777,))
        status777 = cur.fetchone()[0]

        cur.execute('UPDATE Tr_sessions SET status2 = ?, id_us11 = ? WHERE name_us2 = ?',
                    (status777, callback_query.from_user.id, callback_query.from_user.username))
        con.commit()

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = ?', (callback_query.from_user.id, status777))
        a = cur.fetchone()[0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = ? AND i = {a}',
                    (callback_query.from_user.id, status777))
        carts = cur.fetchone()
        id_us1, name, status, photo, caption, iteration, i = carts
        photo1 = FSInputFile(photo)

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = ?',
                    (callback_query.from_user.id, status777))
        total_users = cur.fetchone()[0]

        if total_users == 1:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/1",
                        callback_data="counter"
                    )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

        else:
            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"1/{total_users}",
                        callback_data="counter"
                    ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

        msg = await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id,
                                                  caption=name,
                                                  photo=photo1,
                                                  reply_markup=kb7)
        con.execute(
            F'UPDATE Sessions SET session = 1, message_id = {msg.message_id} WHERE id_us2 = ?',
            (callback_query.from_user.id,))
        con.commit()
    except Exception as e:
        await callback_query.message.reply(text='У вас еще нет карточек, но вы можете их купить!')
        print(e)


@dp.callback_query(F.data == ">>5")
async def strela_DD5(callback_query: CallbackQuery):
    try:

        cur.execute('SELECT capt1 FROM Tr_sessions WHERE name_us2 = ?', (callback_query.from_user.username,))
        name777 = cur.fetchone()[0]

        cur.execute('SELECT status FROM Carts WHERE name = ?', (name777,))
        status777 = cur.fetchone()[0]

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = ?',
                    (callback_query.from_user.id, status777))
        total_users = cur.fetchone()[0]

        con.execute('UPDATE Sessions SET session = session + 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = ?', (callback_query.from_user.id, status777))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = ? AND i = {a}',
                    (callback_query.from_user.id, status777))
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
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<5"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<5"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )
            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<5"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<5"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == ">>>5")
async def strela_DDD5(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT capt1 FROM Tr_sessions WHERE name_us2 = ?', (callback_query.from_user.username,))
        name777 = cur.fetchone()[0]

        cur.execute('SELECT status FROM Carts WHERE name = ?', (name777,))
        status777 = cur.fetchone()[0]

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = ?',
                    (callback_query.from_user.id, status777))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = {total_users} WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = ?', (callback_query.from_user.id, status777))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = ? AND i = {a}',
                    (callback_query.from_user.id, status777))
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
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<5"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<5"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )]
                    ,
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<5"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<5"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )
    except Exception as e:
        print(e)


@dp.callback_query(F.data == "<<5")
async def strela_qq5(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT capt1 FROM Tr_sessions WHERE name_us2 = ?', (callback_query.from_user.username,))
        name777 = cur.fetchone()[0]

        cur.execute('SELECT status FROM Carts WHERE name = ?', (name777,))
        status777 = cur.fetchone()[0]

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = ?',
                    (callback_query.from_user.id, status777))
        total_users = cur.fetchone()[0]

        con.execute('UPDATE Sessions SET session = session - 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = ?', (callback_query.from_user.id, status777))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = ? AND i = {a}',
                    (callback_query.from_user.id, status777))
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
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<5"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<5"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<<",
                        callback_data="<<<5"
                    ),
                        InlineKeyboardButton(
                            text="<<",
                            callback_data="<<5"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == "<<<5")
async def strela_qqq4(callback_query: CallbackQuery):
    try:
        cur.execute('SELECT capt1 FROM Tr_sessions WHERE name_us2 = ?', (callback_query.from_user.username,))
        name777 = cur.fetchone()[0]

        cur.execute('SELECT status FROM Carts WHERE name = ?', (name777,))
        status777 = cur.fetchone()[0]

        cur.execute('SELECT COUNT(*) FROM Carts WHERE id_us1 = ? AND status = ?',
                    (callback_query.from_user.id, status777))
        total_users = cur.fetchone()[0]
        con.execute(f'UPDATE Sessions SET session = 1 WHERE id_us2 = ?', (callback_query.from_user.id,))
        con.commit()
        cur.execute(f'SELECT * FROM Sessions WHERE id_us2 = ?', (callback_query.from_user.id,))
        sessin = cur.fetchone()
        id_us2, session, message_id = sessin

        cur.execute('SELECT i FROM Carts WHERE id_us1 = ? AND status = ?', (callback_query.from_user.id, status777))
        a = cur.fetchall()[session - 1][0]

        cur.execute(f'SELECT * FROM Carts WHERE id_us1 = ? AND status = ? AND i = {a}',
                    (callback_query.from_user.id, status777))
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
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif 1 < session < total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<5"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<5"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        ),
                        InlineKeyboardButton(
                            text=">>",
                            callback_data=">>5"
                        ),
                        InlineKeyboardButton(
                            text=">>>",
                            callback_data=">>>5"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )

        elif session == total_users:

            kb7 = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="<<",
                        callback_data="<<5"
                    ),
                        InlineKeyboardButton(
                            text="<<<",
                            callback_data="<<<5"
                        ),
                        InlineKeyboardButton(
                            text=f"{session}/{total_users}",
                            callback_data="counter"
                        )],
                    [InlineKeyboardButton(
                        text='✅ -> Выбрать',
                        callback_data='vibrat5'
                    )]
                ]
            )

            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo1,
                    caption=name,
                ),
                reply_markup=kb7
            )
    except:
        pass


@dp.callback_query(F.data == 'vibrat5')
async def traide124(callback_query: CallbackQuery):
    cur.execute('SELECT iteration FROM Carts WHERE id_us1 = ? AND name = ?',
                (callback_query.from_user.id, callback_query.message.caption))
    iteration1 = cur.fetchone()[0]
    if iteration1 > 1:
        photo_object = str(callback_query.message.photo[0].file_id)

        cur.execute('UPDATE Tr_sessions SET capt2 = ?, photo2 = ? WHERE name_us2 = ?',
                    (callback_query.message.caption, photo_object,
                     callback_query.from_user.username))
        con.commit()

        cur.execute(f'SELECT id_us10 FROM Tr_sessions WHERE name_us2 = ?', (callback_query.from_user.username,))
        id = cur.fetchall()[0][0]

        await bot.send_photo(chat_id=int(id),
                             caption=f'Пользователь @{callback_query.from_user.username} хочет совершить с тобой сделку!',
                             photo=photo_object,
                             reply_markup=kb9)
    else:
        await callback_query.message.reply('Нет, у вас должно быть хотябы больше 1 карточки такого вида!')


@dp.callback_query(F.data == 'no2')
async def traide3(callback_query: CallbackQuery):
    await callback_query.message.reply('Вы успешно отменили сделку!', reply_markup=kb_ex)

    cur.execute(f'SELECT id_us11 FROM Tr_sessions WHERE name_us1 = ?', (callback_query.from_user.username,))
    id = cur.fetchall()[0][0]

    await bot.send_message(chat_id=int(id), text='Пользователь не согласен на сделку!')


@dp.callback_query(F.data == 'yes2')
async def traide5(callback_query: CallbackQuery):
    await callback_query.message.reply('Сделка прошла успешно!', reply_markup=kb_ex)

    cur.execute(f'SELECT id_us11 FROM Tr_sessions WHERE name_us1 = ?', (callback_query.from_user.username,))
    id = cur.fetchall()[0][0]

    await bot.send_message(chat_id=int(id), text='Сделка прошла успешно!')

    cur.execute('SELECT capt1 FROM Tr_sessions WHERE name_us1 = ?', (callback_query.from_user.username,))
    name777 = cur.fetchone()[0]

    cur.execute('SELECT status FROM Carts WHERE name = ?', (name777,))
    status777 = cur.fetchone()[0]

    cur.execute('UPDATE Tr_sessions SET status1 = ? WHERE name_us1 = ?', (status777, callback_query.from_user.username))
    con.commit()

    cur.execute('SELECT * FROM Tr_sessions WHERE id_us10 = ?', (callback_query.from_user.id,))
    carts1 = cur.fetchone()

    id_us10, id_us11, name_us1, name_us2, capt1, photo1, capt2, photo2, status1, status2 = carts1

    cur.execute('SELECT name FROM Carts WHERE id_us1 = ?', (id_us10,))
    result1 = cur.fetchall()

    cur.execute('SELECT name FROM Carts WHERE id_us1 = ?', (id_us11,))
    result2 = cur.fetchall()

    if capt2 == 'Lada':
        photo7771 = 'media/v-rossii-nachalos-testirovanie-avtopilota-dlya-lada-vesta-1.jpg'
    elif capt2 == 'NISSAN':
        photo7771 = 'media/f33cffb36f991c357a95818e76875254.jpg'
    elif capt2 == 'Volvo':
        photo7771 = 'media/b549ef86bfa3e9568818231465aed573.jpeg'
    elif capt2 == 'Isuzu':
        photo7771 = 'media/66755.jpg'
    elif capt2 == 'Jeep':
        photo7771 = 'media/1701755805_sportishka-com-p-krasivie-mashini-vnedorozhniki-pinterest-1.jpg'
    elif capt2 == 'KIA':
        photo7771 = 'media/1693069229_funnyart-club-p-avtomobil-kia-k5-krasivo-2.jpg'
    elif capt2 == 'Toyota':
        photo7771 = 'media/2017_toyota_prius_prime_advanced_front_three_quarter_06.jpg'
    elif capt2 == 'Lexus':
        photo7771 = 'media/388736-mashina-leksus-7.jpg'

    if (capt2,) in result1:
        cur.execute('UPDATE Carts SET iteration = iteration + 1 WHERE id_us1 = ? AND name = ?',
                    (id_us10, capt2))
        con.commit()

        cur.execute('SELECT iteration FROM Carts WHERE id_us1 = ? AND name = ?',
                    (id_us10, capt2))
        iteration2 = cur.fetchone()[0]

        caption1 = f'''
<u>{capt2}</u>  

Редкость <b>{status2}</b>      
Карт всего <b>{iteration2}</b>
                            '''
        cur.execute('UPDATE Carts SET caption = ? WHERE id_us1 = ? AND name = ?',
                    (caption1, id_us10, capt2))
        con.commit()
    else:
        iteration1 = 1
        photo771 = photo7771
        caption1 = f'''
<u>{capt2}</u>  

Редкость <b>{status2}</b>      
Карт всего <b>{iteration1}</b>
                '''
        cur.execute('INSERT INTO Carts (id_us1, name, status, photo, caption) VALUES (?, ?, ?, ?, ?)',
                    (id_us10, capt2, status2, photo771, caption1))
        con.commit()
        cur.execute('UPDATE Carts SET i = i + 1 WHERE id_us1 = ?', (id_us10,))
        con.commit()

    con.execute(f'UPDATE Users SET {status2} = {status2} + 1 WHERE ids = ?', (id_us10,))
    con.commit()

    if capt1 == 'Lada':
        photo7772 = 'media/v-rossii-nachalos-testirovanie-avtopilota-dlya-lada-vesta-1.jpg'
    elif capt1 == 'NISSAN':
        photo7772 = 'media/f33cffb36f991c357a95818e76875254.jpg'
    elif capt1 == 'Volvo':
        photo7772 = 'media/b549ef86bfa3e9568818231465aed573.jpeg'
    elif capt1 == 'Isuzu':
        photo7772 = 'media/66755.jpg'
    elif capt1 == 'Jeep':
        photo7772 = 'media/1701755805_sportishka-com-p-krasivie-mashini-vnedorozhniki-pinterest-1.jpg'
    elif capt1 == 'KIA':
        photo7772 = 'media/1693069229_funnyart-club-p-avtomobil-kia-k5-krasivo-2.jpg'
    elif capt1 == 'Toyota':
        photo7772 = 'media/2017_toyota_prius_prime_advanced_front_three_quarter_06.jpg'
    elif capt1 == 'Lexus':
        photo7772 = 'media/388736-mashina-leksus-7.jpg'

    if (capt1,) in result2:
        cur.execute('UPDATE Carts SET iteration = iteration + 1 WHERE id_us1 = ? AND name = ?',
                    (id_us11, capt1))
        con.commit()

        cur.execute('SELECT iteration FROM Carts WHERE id_us1 = ? AND name = ?',
                    (id_us11, capt1))
        iteration2 = cur.fetchone()[0]

        caption2 = f'''
<u>{capt1}</u>  

Редкость <b>{status1}</b>      
Карт всего <b>{iteration2}</b>
                            '''
        cur.execute('UPDATE Carts SET caption = ? WHERE id_us1 = ? AND name = ?',
                    (caption2, id_us11, capt1))
        con.commit()

    else:
        iteration2 = 1
        photo772 = photo7772
        caption2 = f'''
<u>{capt1}</u>  

Редкость <b>{status1}</b>      
Карт всего <b>{iteration2}</b>
                    '''
        cur.execute('INSERT INTO Carts (id_us1, name, status, photo, caption) VALUES (?, ?, ?, ?, ?)',
                    (id_us11, capt1, status1, photo772, caption2))
        con.commit()
        cur.execute('UPDATE Carts SET i = i + 1 WHERE id_us1 = ?', (id_us11,))
        con.commit()

    con.execute(f'UPDATE Users SET {status1} = {status1} + 1 WHERE ids = ?', (id_us11,))
    con.commit()

    cur.execute('UPDATE Carts SET iteration = iteration - 1 WHERE id_us1 = ? AND name = ?',
                (id_us11, capt2))
    con.commit()

    cur.execute('SELECT iteration FROM Carts WHERE id_us1 = ? AND name = ?',
                (id_us11, capt2))
    iteration3 = cur.fetchone()[0]

    caption3 = f'''
<u>{capt2}</u>  

Редкость <b>{status1}</b>      
Карт всего <b>{iteration3}</b>
                                '''
    cur.execute('UPDATE Carts SET caption = ? WHERE id_us1 = ? AND name = ?',
                (caption3, id_us11, capt2))
    con.commit()

    cur.execute('UPDATE Carts SET iteration = iteration - 1 WHERE id_us1 = ? AND name = ?',
                (id_us10, capt1))
    con.commit()

    cur.execute('SELECT iteration FROM Carts WHERE id_us1 = ? AND name = ?',
                (id_us10, capt1))
    iteration4 = cur.fetchone()[0]

    caption4 = f'''
<u>{capt1}</u>  

Редкость <b>{status2}</b>      
Карт всего <b>{iteration4}</b>
                                '''
    cur.execute('UPDATE Carts SET caption = ? WHERE id_us1 = ? AND name = ?',
                (caption4, id_us10, capt1))
    con.commit()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

con.commit()
con.close()
cur.close()
