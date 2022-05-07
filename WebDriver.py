from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import os
from pathlib import Path
import pandas as pd


class WebDriver:
    def __init__(self, channel_videos_url, web_driver_path, options_list=None, timeout=10):
        self.channel_url = Path(channel_videos_url)
        self.init_options(options_list)
        self._service = Service(executable_path=web_driver_path)
        # only Firefox currently implemented
        self.driver = webdriver.Firefox(service=self._service, options=self._options)
        self.content_xpath = '//*[@id="contents"]'
        self.timeout = timeout
        self.videos_xpath = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer'

    def init_options(self, options_list):
        self._options = Options()
        if options_list:
            self._options.add_argument(*options_list)

    def open_page(self):
        self.driver.get(self.channel_url)

    def ensure_content_loaded(self):
        try:
            myElem = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, self.content_xpath)))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time! Increase timeout")

    def scroll_to_end(self):
        """Scroll until the end is reached to get all content on the one page"""
        self.ensure_content_loaded()

        # element = self.driver.find_element_by_xpath(self.content_xpath)  # the element you want to scroll
        prev_page_pos = 0
        while True:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            new_page_pos = str(self.driver.execute_script('return window.pageYOffset;'))
            if prev_page_pos == new_page_pos:
                break
            prev_page_pos = new_page_pos
            time.sleep(1)

    def save_videos_metadata(self, df):
        name = self.channel_url.parent.stem
        if not os.path.exists(name):
            os.mkdir(name)
        if not os.path.exists(name):
            df.to_csv(name+"/videos_metadata.csv", sep=';', index=False)
        else:
            df.to_csv(name+"/videos_metadata.csv", sep=';', index=False, mode='a', header='False')


    def get_all_content(self):
        video_preview = driver.find_elements_by_xpath(self.videos_xpath)
        videos_dict = {'title':[], 'link':[]}
        for item in tqdm(video_preview):
            item = item.find_elements_by_id('video-title')
            assert len(item) == 1, "links number are not equal to 1 for video"
            link = item[0].get_attribute('href')
            title = item.text.split('\n')[1]
            videos_dict['link'].append(link)
            videos_dict['title'].append(title)
        self.save_videos_metadata(pd.DataFrame(videos_dict))

    def exit(self):
        """End session"""
        self.driver.quit()