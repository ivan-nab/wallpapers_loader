from datetime import datetime
from wallpapers_loader.image_finder import construct_url, parse_web_page


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
        with open("./tests/test_data/test_html.html") as f:
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
        parsed_data = parse_web_page(None)
        assert parsed_data == {}
