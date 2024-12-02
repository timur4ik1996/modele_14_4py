import sqlite3

connection = sqlite3.connect('crud_functions.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')

title = ['Протеин', 'Креатин', 'Гейнер', 'BCAA']
description = (
    [
        'Протеин - это очищенный и концентрированный белок.Такой же, как в обычных продуктах: молоке, яйцах, мясе и тд.Только приведенный в более усвояемый вид.'],
    [
        'Это вещество помогает мышцам получать больше энергии, поэтому оно особенно полезно для спортсменов, которые хотят увеличить силу,выносливость и набрать мышечную массу.'],
    [
        'Гейнер представляет собой порошковую смесь для приготовления коктейля, которую смешивают с водой, соком или молоком или добавляют в пищу.'],
    [
        'Название BCAA — это аббревиатура от английского выражения «Branched-chain amino acids». Оно переводится как «аминокислоты с разветвленными цепочками» и обозначает вещество, являющееся незаменимым материалом для построения новых мышечных структур.']
)
price = [100, 200, 300, 400]

# cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                (f'{title[0]}', f'{description[0]}', f'{price[0]}'))
# cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                (f'{title[1]}', f'{description[1]}', f'{price[1]}'))
# cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                (f'{title[2]}', f'{description[2]}', f'{price[2]}'))
# cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                (f'{title[3]}', f'{description[3]}', f'{price[3]}'))
# connection.commit()
# connection.close()


def get_all_products():
    connection_ = sqlite3.connect('crud_functions.db')
    cursor_ = connection_.cursor()
    cursor_.execute('SELECT title, description, price FROM Products')
    db_ = cursor_.fetchall()
    return list(db_)
