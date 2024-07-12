import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload

from keybords.keyboard1 import kb1
from keybords.keyboard2 import kb2

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
con.commit()


@dp.message(Command('start'))
async def start_command(message: Message, command: Command = None):
    cur.execute('INSERT INTO Users (ids, many, common, rare, epic) VALUES (?, ?, ?, ?, ?)',
                    (message.from_user.id, 0, 0, 0, 0))
    con.commit()
    cur.execute('INSERT INTO Promo (id_us, promo1, promo2, promo3) VALUES (?, ?, ?, ?)',
                    (message.from_user.id, 0, 0, 0))
    con.commit()
    await message.reply(f'Привет, <u>@{message.from_user.username}</u>!', reply_markup=kb1)

    if command:
        args = command.args
        reference = decode_payload(args)
        await message.reply(f'Теперь вы и ваш реферал получат по 1000 many')
        cur.execute('UPDATE Users SET many = many + 1000 WHERE ids = ?', (reference, ))
        cur.execute('UPDATE Users SET many = many + 1000 WHERE ids = ?', (message.from_user.id,))


@dp.message(F.text == '📈 -> Cтатистика')
async def status_msg(message: Message):
    cur.execute('SELECT * FROM Users WHERE ids = ?', (message.from_user.id,))
    user = cur.fetchone()
    cur.execute('SELECT * FROM Promo WHERE id_us = ?', (message.from_user.id,))
    promo_c = cur.fetchone()
    if user and promo_c:
        ids, many, common, rare, epic = user
        id_us, promo1, promo2, promo3 = promo_c
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
        ''')
    else:
        await message.reply('Вы НЕ были зарегистрированы')


@dp.message(F.text == '🔖 -> Задания')
async def mession_msg(message: Message):
    await message.reply(f'''
<u>@{message.from_user.username}</u>, ты должен навербовать как можно больше людей, чтобы стать богаче!
За каждого нового приглашенного пользователя ты получишь <em>1000 many</em>
''', reply_markup=kb2)


@dp.message(F.text == '🎫 -> Ваша реферальная ссылка')
async def mession_msg_1(message: Message):
    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    await message.reply(f'Вот ваша реферальная ссылка -> {link}', reply_markup=kb1)


@dp.message()
async def promo_codes_msg(message: Message):
    cur.execute('SELECT * FROM Promo')
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
    if message.text in promo_codes and promo_codes2[promo_codes1[message.text]] < 1:
        cur.execute(f'UPDATE Users SET many = many + {promo_codes[message.text]} WHERE ids = ?',
                    (message.from_user.id,))
        cur.execute(
            f'UPDATE Promo SET {promo_codes1[message.text]} = {promo_codes1[message.text]} + 1 WHERE id_us = ?',
            (message.from_user.id,))
        con.commit()
        await message.reply(
            f'Вам промокод корректен и вы получаете {promo_codes[message.text]} many.')

    else:
        await message.reply('Увы...Такого промокода мы еще не придумали...')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

con.commit()
con.close()
