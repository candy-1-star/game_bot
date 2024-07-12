from aiogram import Router
from aiogram.types import Message

from main import db1, db2

rt = Router()


@rt.message()
async def promo_codes_msg(message: Message):
    db2.cur1.execute('SELECT * FROM Promo')
    promo_c = db2.cur1.fetchone()
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
        db1.cur.execute(f'UPDATE Users SET many = many + {promo_codes[message.text]} WHERE ids = ?',
                        (message.from_user.id,))
        db2.cur1.execute(
            f'UPDATE Promo SET {promo_codes1[message.text]} = {promo_codes1[message.text]} + 1 WHERE id_us = ?',
            (message.from_user.id,))
        db1.con.commit()
        db2.con1.commit()
        await message.reply(
            f'Вам промокод корректен и вы получаете {promo_codes[message.text]} many.')

    else:
        await message.reply('Увы...Такого промокода мы еще не придумали...')


db1.con.close()
db2.con1.close()
