import calendar
import os
import time
from datetime import datetime
from urllib.parse import urljoin
import requests
from lxml import etree

import settings


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


def download_wallpaper(url):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        wallpaper_filename = os.path.basename(url)
        wallpaper_dir = '.\\wallpapers'
        if not os.path.exists(wallpaper_dir):
            os.mkdir(wallpaper_dir)
        filepath = os.path.join(wallpaper_dir, wallpaper_filename)
        print(f'downloading {url} to {filepath}')
        with open(filepath, 'wb') as f:
            for chunk in response:
                f.write(chunk)
        return filepath


def download_wallpapers(date, resolution):
    url = construct_url(date)
    data = get_data(url)
    parsed_data = parse_web_page(data)
    if parsed_data:
        links_list = parsed_data.get(resolution)
        if links_list:
            for link in links_list:
                download_wallpaper(link)
        else:
            print(f"Wallpapers with resolution {resolution} not found")
    else:
        print('Wallpappers not found')


def get_date_from_string(input_date):
    try:
        wl_date = datetime.strptime(input_date, "%m-%Y")
        return wl_date
    except ValueError:
        print("incorrect month and year parameter")


def validate_resolution(input_resolution):
    try:
        res_x, res_y = map(int, input_resolution.split('x'))
        return input_resolution
    except ValueError:
        print("incorrect resolution parameter")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        input_date = get_date_from_string(sys.argv[1])
        input_resolution = validate_resolution(sys.argv[2])
        if input_date and input_resolution:
            start_time = time.time()
            download_wallpapers(input_date, input_resolution)
            print("time :", time.time() - start_time)
    else:
        print('''
            Wallpapers loader\n
                usage: wl_loader.py <month-year> <resolution>\n
                example: wl_loader.py 12-2020 1920x1080\n
            ''')

