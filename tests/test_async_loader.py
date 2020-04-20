import asyncio
import os
import shutil
import tempfile
from asynctest import CoroutineMock, patch
from datetime import datetime
from unittest import mock

from wallpapers_loader.async_loader import download_file_async, download_files
from wl_loader import download_wallpapers


class TestDownloadWallpaper:
    def setup(self):
        self.wallpaper_file = "./tests/test_data/feb-14-principles-of-good-design--dieter-rams-nocal-1920x1080.png"
        self.expected_size = os.stat(self.wallpaper_file).st_size
        self.expected_parsed_data = {
            '640x480': [
                'http://example.com/1.jpg', 'http://example.com/2.jpg',
                'http://example.com/3.jpg'
            ]
        }
        self.dst_dir = tempfile.mkdtemp()

    @patch('aiohttp.ClientSession.get')
    def test_download_file(self, mock_get):
        f = open(self.wallpaper_file, "rb")
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.read = CoroutineMock(
            side_effect=f.read)
        loop = asyncio.get_event_loop()
        future = download_file_async(
            "http://localhost/feb-14-principles-of-good-design--dieter-rams-nocal-1920x1080.png",
            self.dst_dir)
        filename = loop.run_until_complete(future)
        assert os.path.exists(filename)
        assert filename is not None
        assert os.stat(filename).st_size == self.expected_size
        os.remove(filename)
        f.close()

    @patch('aiohttp.ClientSession.get')
    def test_download_file_incorrect_url(self, mock_get):
        mock_get.return_value.__aenter__.return_value.status = 404
        loop = asyncio.get_event_loop()
        future = download_file_async("http://wrongurl/picture.jpg",
                                     self.dst_dir)
        filename = loop.run_until_complete(future)
        assert filename is None

    @patch('wallpapers_loader.async_loader.download_file_async')
    @mock.patch('os.mkdir')
    def test_download_multiple_files(self, mock_mkdir,
                                      mock_download_files_async):
        urls = self.expected_parsed_data['640x480']
        download_files(urls, self.dst_dir)
        assert mock_download_files_async.call_count == 3

    @mock.patch('wl_loader.download_files')
    @mock.patch('wl_loader.parse_web_page')
    @mock.patch('wl_loader.get_data')
    def test_download_wallpapers(self, mock_get_data, mock_parse_web_page,
                                 mock_download_files):
        mock_get_data.return_value = ''
        mock_parse_web_page.return_value = self.expected_parsed_data
        input_date = datetime.strptime('12-2020', '%m-%Y')
        input_resolution = "640x480"
        download_wallpapers(input_date, input_resolution)
        assert mock_get_data.call_count == 1
        assert mock_download_files.call_count == 1

    @mock.patch('wl_loader.download_files')
    @mock.patch('wl_loader.parse_web_page')
    @mock.patch('wl_loader.get_data')
    def test_download_wallpapers_incorrect_params(self, mock_get_data,
                                                  mock_parse_web_page,
                                                  mock_download_file):
        mock_get_data.return_value = ''
        mock_parse_web_page.return_value = self.expected_parsed_data
        input_date = datetime.strptime('12-2020', '%m-%Y')
        input_resolution = "1920x1080"
        download_wallpapers(input_date, input_resolution)
        assert mock_download_file.call_count == 0

    def teardown(self):
        shutil.rmtree(self.dst_dir)
