import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from database.db import Database, Database1
from handlers import promo

bot = Bot(token='7343617128:AAHyW2P6KApMkQlBGf2vIGlNPl7CrYYmcwA', default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

db1 = Database()
db1.creating_table()

db2 = Database1()
db2.creating_table1()


@dp.message(Command('start'))
async def start_command(message: Message):
    db1.cur.execute('INSERT INTO Users (ids, many, common, rare, epic) VALUES (?, ?, ?, ?, ?)',
                    (message.from_user.id, 0, 0, 0, 0))
    db1.con.commit()
    db2.cur1.execute('INSERT INTO Promo (id_us, promo1, promo2, promo3) VALUES (?, ?, ?, ?)',
                     (message.from_user.id, 0, 0, 0))
    db2.con1.commit()
    buttons = [
        [KeyboardButton(text='📈 -> Cтатистика')],
        [KeyboardButton(text='🔖 -> Задания')],
        [KeyboardButton(text='💎 -> Капсулы')]
    ]
    kb = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='📌 -> Введите промокод'
    )
    await message.reply(f'Привет, <u>@{message.from_user.username}</u>!', reply_markup=kb)


@dp.message(F.text == '📈 -> Cтатистика')
async def status_msg(message: Message):
    db1.cur.execute('SELECT * FROM Users WHERE ids = ?', (message.from_user.id,))
    user = db1.cur.fetchone()
    db2.cur1.execute('SELECT * FROM Promo WHERE id_us = ?', (message.from_user.id,))
    promo_c = db2.cur1.fetchone()
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
    await message.reply('Ладно...')


async def main():
    dp.include_router(promo.rt)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

db1.con.commit()
db1.con.close()
db2.con1.commit()
db2.con1.close()
