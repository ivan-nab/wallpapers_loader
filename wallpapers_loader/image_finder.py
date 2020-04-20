import calendar
from urllib.parse import urljoin
import requests
from lxml import etree

from wallpapers_loader import settings


def parse_web_page(page_body):
    tree = etree.HTML(str(page_body))
    result = tree.xpath(settings.XPATH_REF)
    links_dict = {}
    for r in result:
        links_dict.setdefault(r.text, []).append(r.attrib['href'])
    return links_dict


def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content


def construct_url(date):
    month = date.month
    year = date.year

    month_str = str(month).zfill(2)

    if month == 12:
        collection_month = 1
        collection_year = year + 1
    else:
        collection_month = month + 1
        collection_year = year
    collection_month_name = calendar.month_name[collection_month].lower()
    walpapers_page_url = f"{year}/{month_str}/desktop-wallpaper-calendars-{collection_month_name}-{collection_year}/"
    return urljoin(settings.WALLPAPERS_URL, walpapers_page_url)