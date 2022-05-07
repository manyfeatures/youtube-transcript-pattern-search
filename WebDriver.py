from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class WebDriver:
    def __init__(self, channel_videos_url, web_driver_path, options_list=None):
        self.channel_url = channel_videos_url
        self._options = self.init_options(options_list)
        self._service = Service(executable_path=web_driver_path)
        # only Firefox currently implemented
        self.driver = webdriver.Firefox(service=self._service, options=self.options)
        self.content_xpath = '//*[@id="contents"]'
        self.timeout = 10

    def init_options(self, options_list):
        self.options = Options()
        if options_list:
            self.options.add_argument(*options_list)

    def open_page(self):
        self.driver.get(self.channel_url)

    def ensure_content_loaded(self):
        try:
            myElem = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, self.content_xpath)))
            print()
        except TimeoutException:
            print
            "Loading took too much time!"


    def scroll_to_end(self):
        """Scroll until the end is reached to get all content"""
        self.ensure_content_loaded()

        element = self.driver.find_element_by_xpath(self.content_xpath)  # the element you want to scroll to
        prev_page_pos = 0
        while True:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            new_page_pos = str(self.driver.execute_script('return window.pageYOffset;'))
            if prev_page_pos == new_page_pos:
                break
            prev_page_pos = new_page_pos
            time.sleep(1)
