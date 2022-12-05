"""
1
select price, count(price) as amount
from shop_data
where avaliability = 'доступно'
GROUP by price
order by price ASC

select price, count(price) as amount
from shop_data
where avaliability = 'под заказ'
GROUP by price
order by price ASC


2
SELECT avg(price) as avg_price, article
FROM shop_data
GROUP by article
ORDER by avg_price DESC
LIMIT 10


3
SELECT DISTINCT identifier, count(*) as amount
FROM shop_data
WHERE (avaliability = 'доступно' or avaliability = 'под заказ')
GROUP by avaliability
"""

import sqlite3


connect_db = sqlite3.connect('parsed_data.db')

cur = connect_db.cursor()


def create_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS shop_data(
        name TEXT,
        article INT,
        identifier INT PRIMARY KEY,
        avaliability TEXT,
        is_discouted TEXT,
        price INT,
        discounted_price INT);""")
    connect_db.commit()


def save_dataframe(frame):
    cur.executemany("INSERT INTO shop_data VALUES(?, ?, ?, ?, ?, ?, ?);", frame)
    connect_db.commit()


create_db()