"""
Проект разнесен по модулям для разделения целей функций.
Архитектура:
src
├── db_controller.py - модуль связи с базой данных
├── extractors.py - набор основных функций проекта
├── parsed_data.db - файл БД SQLite3
├── parser.py - точка входа
"""

from bs4 import BeautifulSoup as BS
import requests
from extractors import load_data_to_db


def parse() -> None:
    for i in range(1, 14):
        data = requests.get(
            url=f"https://azbykamebeli.ru/catalog/0000057/?page={i}")
        html = BS(data.content, 'lxml')
        load_data_to_db(html)


if __name__ == "__main__":
    parse()
