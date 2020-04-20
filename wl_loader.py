import time
from datetime import datetime
from wallpapers_loader import settings
from wallpapers_loader.async_loader import download_files
from wallpapers_loader.image_finder import construct_url, get_data, parse_web_page


def download_wallpapers(date, resolution):
    url = construct_url(date)
    data = get_data(url)
    parsed_data = parse_web_page(data)
    if parsed_data:
        urls = parsed_data.get(resolution)
        if urls:
            print("Downloading wallpapers")
            download_files(urls, settings.WALLPAPERS_DIR)
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

       