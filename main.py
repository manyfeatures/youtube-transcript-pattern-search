# Search of words time steps in video/videos transcripts from the given YouTube channel
from WebDriver import *

def main():
    channel_videos_url = "https://www.youtube.com/c/MadHighlights/videos"
    web_driver_path = "./geckodriver"
    driver = WebDriver(channel_videos_url, web_driver_path)

    driver.open_page()
    driver.scroll_to_end()
    driver.get_all_content()

    driver.exit() # make it context manager?

if __name__ == "__main__":
    main()