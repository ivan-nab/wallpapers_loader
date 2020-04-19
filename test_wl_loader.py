import os
from wl_loader import construct_url, parse_web_page, download_wallpaper
from datetime import datetime
from unittest import mock


class TestConstructUrl:
    def setup(self):
        self.expected_url = 'https://www.smashingmagazine.com/2019/11/desktop-wallpaper-calendars-december-2019/'
        self.expected_url_last_month = 'https://www.smashingmagazine.com/2019/12/desktop-wallpaper-calendars-january-2020/'

    def test_construct_url(self):
        date = datetime.strptime("11-2019", "%m-%Y")
        url = construct_url(date)
        assert url == self.expected_url
    
    def test_construct_url_last_month(self):
        date = datetime.strptime('12-2019', "%m-%Y")
        url = construct_url(date)
        assert url == self.expected_url_last_month

class TestParseWebPage:
    def setup(self):
        with open ("test_html.html") as f:
            self.page_body = f.read()
        self.expected_images_count = 21
        self.expected_image_url = 'http://files.smashingmagazine.com/wallpapers/jan-17/reindeer/nocal/jan-17-reindeer-nocal-640x480.png'
    
    def test_parse_web_page_with_data(self):
        parsed_data = parse_web_page(self.page_body)
        assert len(parsed_data['640x480']) == self.expected_images_count
        assert self.expected_image_url in parsed_data['640x480']
    
    def test_parse_web_page_without_data(self):
        parsed_data = parse_web_page('<html></html>')
        assert parsed_data == {}
        

class TestDownloadWallpaper:
    def setup(self):
        self.wallpaper_file = ".\\test_data\\feb-14-principles-of-good-design--dieter-rams-nocal-1920x1080.png"
        self.expected_size = os.stat(self.wallpaper_file).st_size

    @mock.patch('wl_loader.requests.get')
    def test_download_wallpaper(self, mock_requests_get):
        wallpaper_fd = open(self.wallpaper_file, "rb")
        mock_requests_get.return_value = wallpaper_fd
        mock_requests_get.return_value.status_code = 200
        filename = download_wallpaper("http://localhost/feb-14-principles-of-good-design--dieter-rams-nocal-1920x1080.png")
        assert os.path.exists(filename)
        assert os.stat(filename).st_size == self.expected_size
        os.remove(filename)
        wallpaper_fd.close()

    @mock.patch('wl_loader.requests.get')
    def test_download_wallpaper_incorrect_url(self, mock_requests_get):
        mock_requests_get.return_value = mock.Mock()
        mock_requests_get.return_value.status_code = 404
        filename = download_wallpaper("http://wrongurl/picture.jpg")
        assert filename == None


