from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class WebDriver:
    def __init__(self, channel_videos_url, web_driver_path, options=[]):
        self.channel_url = channel_videos_url
        self._options = init_options(options)
        self._service = Service(executable_path=web_driver_path)

    def init_options(self, options_list):
        self.options = Options()
        self.options.add_argument(*options_list)