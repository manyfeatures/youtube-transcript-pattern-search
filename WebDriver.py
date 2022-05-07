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
import re
import numpy as np


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
        self.foldername = self.channel_url.parent.stem

    def init_options(self, options_list):
        self._options = Options()
        if options_list:
            self._options.add_argument(*options_list)

    def open_page(self):
        self.driver.get(self.channel_url.as_posix())

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

        print('Scrolling...')
        # element = self.driver.find_element_by_xpath(self.content_xpath)  # the element you want to scroll
        prev_page_pos = 0
        while True:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.END)
            new_page_pos = str(self.driver.execute_script('return window.pageYOffset;'))
            if prev_page_pos == new_page_pos:
                break
            prev_page_pos = new_page_pos
            time.sleep(1)

            # DEBUG
            break

    def save_videos_metadata(self, df):
        if not os.path.exists(self.foldername):
            os.mkdir(self.foldername)
        if not os.path.exists(foldername):
            df.to_csv(self.foldername+"/videos_metadata.csv", sep=';', index=False)
        else:
            df.to_csv(self.foldername+"/videos_metadata.csv", sep=';', index=False, mode='a', header='False')


    def get_all_content(self):
        video_preview = self.driver.find_elements_by_xpath(self.videos_xpath)
        videos_dict = {'title':[], 'link':[], 'file':[]}
        regex = re.compile(r"([\d\:]*)?(\n)?(.*)(\n).*(\n).*$") # extact title
        for i, item in tqdm(enumerate(video_preview)):
            link = item.find_elements_by_id('video-title')
            assert len(link) == 1, "links number are not equal to 1 for video"
            link = link[0].get_attribute('href')
            title = regex.search(item.text).group(3) # or just use all item with views and time
            videos_dict['link'].append(link)
            videos_dict['title'].append(title)
            videos_dict['file'].append('file'+str(i)+'.txt')
        self.save_videos_metadata(pd.DataFrame(videos_dict))

    # TODO: split the function to pieces
    def download_transcript(self, url, filename, title):
        self.driver.get(url)
        _1st_button_css = "ytd-menu-renderer.ytd-video-primary-info-renderer > yt-icon-button:nth-child(3) > button:nth-child(1)"
        button = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, _1st_button_css)))
        button.click() #  elipsis (...) button
        _2nd_button_css = "ytd-menu-service-item-renderer.style-scope:nth-child(2) > tp-yt-paper-item:nth-child(1) > yt-formatted-string:nth-child(2)"
        button = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, _2nd_button_css)))
        button.click() #  `show transcript` buttion

        # get transcript panel
        css_selector = "html body ytd-app div#content.style-scope.ytd-app ytd-page-manager#page-manager.style-scope.ytd-app ytd-watch-flexy.style-scope.ytd-page-manager.hide-skeleton div#columns.style-scope.ytd-watch-flexy div#secondary.style-scope.ytd-watch-flexy div#secondary-inner.style-scope.ytd-watch-flexy div#panels.style-scope.ytd-watch-flexy ytd-engagement-panel-section-list-renderer.style-scope.ytd-watch-flexy"
        transcript = self.driver.find_element_by_css_selector(css_selector)

        sentnence_xpath = "//div[contains(@class, 'segment style-scope ytd-transcript-segment-renderer')]"
        sentences = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, sentnence_xpath)))

        #all_text = []
        with open(self.foldername+f"/{filename}", 'a+') as f:
            print(f'go throuh transcript of video: {title}')
            for sent in tqdm(sentences):
                #all_text.append(x.text.replace('\n','#'))
                f.write(sent.text.replace('\n','#'))
                f.write('\n')

    def save_videos_transcripts(self):
        df = pd.read_csv(self.foldername+"/videos_metadata.csv", sep=';')
        for i, row in df.iterrows():
           self.download_transcript(row.link, row.file, row.title)
           break

    def exit(self):
        """End session"""
        self.driver.quit()