import asyncio
import sqlite3
from random import choices, choice

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload

from keybords.keyboard1 import kb1
from keybords.keyboard3 import kb3
from keybords.keyboard4 import kb4

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
photo TEXT NOT NULL,
caption TEXT NOT NULL
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
        await message.reply(f'Привет, <u>@{message.from_user.username}</u>!', reply_markup=kb1)

        if command:
            args = command.args
            reference = decode_payload(args)
            await message.reply(f'Теперь вы и ваш реферал получат по 1000 many')
            cur.execute('UPDATE Users SET many = many + 1000 WHERE ids = ?', (reference,))
            cur.execute('UPDATE Users SET many = many + 1000 WHERE ids = ?', (message.from_user.id,))
    except:
        await message.reply(f'Привет, <u>@{message.from_user.username}</u>!', reply_markup=kb1)


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


@dp.message(F.text == '🔮 -> Капсула 1')
async def random_1(message: Message):
    await message.reply('''
Тут содержаться 8 карточек!
- Lada  ->  Common  ->  50%
- NISSAN  ->  Common  ->  50%
- Volvo  ->  Common  ->  50%
- Isuzu  -> Rare  ->  30%
- Jeep  ->  Rare  ->  30%
- KIA  ->  Rare  ->  30%
- Toyota  ->  Epic  ->  20%
- Lexus  ->  Epic  ->  20%
Цена - 300
    ''', reply_markup=kb4)


@dp.message(F.text == '✅ -> Открыть')
async def k1def(message: Message):
    cur.execute("SELECT many FROM Users WHERE ids = ?", (message.from_user.id,))
    result = cur.fetchone()
    if 300 <= result[0]:
        con.execute('UPDATE Users SET many = many - 300 WHERE ids = ?', (message.from_user.id,))
        kart1 = choices(items, weights=weights)[0]
        if kart1 == 'common':
            kart = choice(common1)
        elif kart1 == 'rare':
            kart = choice(rare1)
        elif kart1 == 'epic':
            kart = choice(epic1)

        if kart == 'Lada':
            photo = FSInputFile('media/v-rossii-nachalos-testirovanie-avtopilota-dlya-lada-vesta-1.jpg')
            photo1 = 'media/v-rossii-nachalos-testirovanie-avtopilota-dlya-lada-vesta-1.jpg'
            caption = '''
<u>Lada</u>  

Редкость <b>Common</b>      
            '''
            cur.execute('INSERT INTO Carts (id_us1, photo, caption) VALUES (?, ?, ?)',
                        (message.from_user.id, photo1, caption))
            con.commit()
        elif kart == 'NISSAN':
            photo = FSInputFile('media/f33cffb36f991c357a95818e76875254.jpg')
            photo1 = 'media/f33cffb36f991c357a95818e76875254.jpg'
            caption = '''
<u>NISSAN</u>  

Редкость <b>Common</b>      
            '''
            cur.execute('INSERT INTO Carts (id_us1, photo, caption) VALUES (?, ?, ?)',
                        (message.from_user.id, photo1, caption))
            con.commit()
        elif kart == 'Volvo':
            photo = FSInputFile('media/b549ef86bfa3e9568818231465aed573.jpeg')
            photo1 = 'media/b549ef86bfa3e9568818231465aed573.jpeg'
            caption = '''
<u>Volvo</u>  

Редкость <b>Common</b>      
            '''
            cur.execute('INSERT INTO Carts (id_us1, photo, caption) VALUES (?, ?, ?)',
                        (message.from_user.id, photo1, caption))
            con.commit()
        elif kart == 'Isuzu':
            photo = FSInputFile('media/66755.jpg')
            photo1 = 'media/66755.jpg'
            caption = '''
<u>Isuzu</u>  

Редкость <b>Rare</b>      
            '''
            cur.execute('INSERT INTO Carts (id_us1, photo, caption) VALUES (?, ?, ?)',
                        (message.from_user.id, photo1, caption))
            con.commit()
        elif kart == 'Jeep':
            photo = FSInputFile('media/1701755805_sportishka-com-p-krasivie-mashini-vnedorozhniki-pinterest-1.jpg')
            photo1 = 'media/1701755805_sportishka-com-p-krasivie-mashini-vnedorozhniki-pinterest-1.jpg'
            caption = '''
<u>Jeep</u>  

Редкость <b>Rare</b>      
            '''
            cur.execute('INSERT INTO Carts (id_us1, photo, caption) VALUES (?, ?, ?)',
                        (message.from_user.id, photo1, caption))
            con.commit()
        elif kart == 'KIA':
            photo = FSInputFile('media/1693069229_funnyart-club-p-avtomobil-kia-k5-krasivo-2.jpg')
            photo1 = 'media/1693069229_funnyart-club-p-avtomobil-kia-k5-krasivo-2.jpg'
            caption = '''
<u>KIA</u>  

Редкость <b>Rare</b>      
            '''
            cur.execute('INSERT INTO Carts (id_us1, photo, caption) VALUES (?, ?, ?)',
                        (message.from_user.id, photo1, caption))
            con.commit()
        elif kart == 'Toyota':
            photo = FSInputFile('media/2017_toyota_prius_prime_advanced_front_three_quarter_06.jpg')
            photo1 = 'media/2017_toyota_prius_prime_advanced_front_three_quarter_06.jpg'
            caption = '''
<u>Toyota</u>  

Редкость <b>Epic</b>      
            '''
            cur.execute('INSERT INTO Carts (id_us1, photo, caption) VALUES (?, ?, ?)',
                        (message.from_user.id, photo1, caption))
            con.commit()
        elif kart == 'Lexus':
            photo = FSInputFile('media/388736-mashina-leksus-7.jpg')
            photo1 = 'media/388736-mashina-leksus-7.jpg'
            caption = '''
<u>Lexus</u>  

Редкость <b>Epic</b>      
            '''
            cur.execute('INSERT INTO Carts (id_us1, photo, caption) VALUES (?, ?, ?)',
                        (message.from_user.id, photo1, caption))
            con.commit()

        await bot.send_photo(photo=photo, chat_id=message.chat.id, caption=caption)
        con.execute(f'UPDATE Users SET {kart1} = {kart1} + 1 WHERE ids = ?', (message.from_user.id,))
        con.commit()
    else:
        await message.reply('У вас недостаточно сретств', reply_markup=kb1)


@dp.message(F.text == '🔚 -> Вернуться в главное меню')
async def exit_def(message: Message):
    await message.reply(f'Привет, <u>@{message.from_user.username}</u>!', reply_markup=kb1)


@dp.message(F.text == '🔥 -> Промокоды')
async def promo_codes_msg(message: Message):
    await message.reply('Введите, пожалуйста, ваш промокод!')

    @dp.message()
    async def promo_event(message1: Message):
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
        if message1.text in promo_codes and promo_codes2[promo_codes1[message1.text]] < 1:
            cur.execute(f'UPDATE Users SET many = many + {promo_codes[message1.text]} WHERE ids = ?',
                        (message1.from_user.id,))
            cur.execute(
                f'UPDATE Promo SET {promo_codes1[message1.text]} = {promo_codes1[message1.text]} + 1 WHERE id_us = ?',
                (message1.from_user.id,))
            con.commit()
            await message1.reply(
                f'Вам промокод корректен и вы получаете {promo_codes[message1.text]} many.')

        else:
            await message1.reply('Увы...Такого промокода мы еще не придумали...')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

con.commit()
con.close()
