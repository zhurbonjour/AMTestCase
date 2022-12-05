"""
Данный набор функций позволяет получить информацию с заданной
html-страницы и загрузить её в БД.
"""

from bs4 import BeautifulSoup as BS
import db_controller


def get_items_name(html) -> list:
    """
    Изввлечение имен товаров со страницы каталога
    :return: list: [str, str, ...]
    """
    item_block = html.find_all("div", class_="item__title h4")
    name_list = []
    for item in item_block:
        target = BS(str(item), 'lxml')
        name = target.find("span", itemprop='name')
        if name:
            name_list.append(name.text)
    return name_list


def get_item_id(html) -> list:
    """
    извлечение айди номера
    айди зашит в ссылке на карточку товара, поэтому извлекается из нее
    :return: list: [int, int, ...]
    """
    item_block = html.find_all("div", class_="items-list__item-wrap")
    id_list = []
    for item in item_block:
        target = BS(str(item), 'lxml')
        identifier = str(target.a['href']).split("=")
        if identifier:
            id_list.append(identifier[1])
    return id_list


def get_item_availability(html) -> list:
    """
    извлечение статуса доступности товара
    :return: list [str, str, ...]
    """
    item_block = html.find_all("div", class_="items-list__item-wrap")
    av_list = []
    for item in item_block:
        target = BS(str(item), 'lxml')
        availability = target.find("small", class_="text-muted f-XS"
                                   ).next_sibling.next_sibling
        if availability:
            av_list.append(availability
                           .text
                           .replace("\n", " ")
                           .replace("\t", ""))
    return av_list


def get_item_number(html) -> list:
    """
    Получение списка артикулов
    :return: list: [int, int, ...]
    """
    item_block = html.find_all("div", class_="items-list__item-wrap")
    num_list = []
    for item in item_block:
        target = BS(str(item), 'lxml')
        num = target.find("small", class_="text-muted f-XS").text.split()
        if num:
            num_list.append(num[1])
    return num_list


def get_item_discount_price(html) -> list:
    """
    Получение списка цен для онлайн-заказа
    :return: list: [int, int, ...]
    """
    item_block = html.find_all("div", class_="items-list__item-wrap")
    online_price_list = []
    for item in item_block:
        target = BS(str(item), 'lxml')
        online_price = target.find("div", class_="online-price")
        if online_price:
            online_price_list.append(int(online_price.text.replace(" ", "").replace("₽","")))
    return online_price_list


def get_item_price(html) -> list:
    """
    Получение списка цен
    :return: list: [int, int, ...]
    """
    item_block = html.find_all("div", class_="items-list__item-wrap")
    price_list = []
    for item in item_block:
        target = BS(str(item), 'lxml')
        price = target.find("a", class_="store-price fake-link")
        if price:
            price_list.append(int(price.text.replace(" ", "").replace("₽","")))
        else:
            online_price = target.find("div", class_="online-price")
            price_list.append(int(online_price.text.replace(" ", "").replace("₽","")))
    return price_list


def get_is_discount(html) -> list:
    """
    Расчет информации для поля is_discount.
    В рамках задания поле не применяется, однако,
    оно повышает наглядность данных
    и может быть использовано в дополнительных расчетах
    :return: list [str, str, ...]
    """
    price = get_item_price(html)
    discounted_price = get_item_discount_price(html)
    discount_list = []
    diff = zip(price, discounted_price)
    for i in diff:
        if i[0] - i[1] == 0:
            discount_list.append("No")
        else:
            discount_list.append("Yes")
    return discount_list


def load_data_to_db(html) -> None:
    """
    Извлечение всей информации с переданной страницы.
    В результате работы функция сохраняет данные в бд.
    :param html: html-страница
    """
    name = get_items_name(html)
    article = get_item_number(html)
    identifier = get_item_id(html)
    avaliability = get_item_availability(html)
    is_discouted = get_is_discount(html)
    price = get_item_price(html)
    discounted_price = get_item_discount_price(html)
    group_data = zip(name,
                     article,
                     identifier,
                     avaliability,
                     is_discouted,
                     price,
                     discounted_price)
    db_controller.save_dataframe(group_data)
