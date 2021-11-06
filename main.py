from random import randrange
import time
from bot.tidal import Tidal
import undetected_chromedriver.v2 as driver
import os
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

logging.basicConfig(filename='app.log', level=logging.INFO)

SONGS_PER_URL = 10
browser = None
PROXY_LIST = []

def read_file_lines(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    return lines


def get_porxy(filename):
    return read_file_lines(filename)


def get_credentials(filename: str):
    credentials_string = read_file_lines(filename)
    credentials = [tuple(c.strip().split(":")) for c in credentials_string]
    return credentials or []


def get_urls(filename:str):
    return read_file_lines(filename)


def clear_browser_cache():
    browser.get("chrome://settings/clearBrowserData")
    time.sleep(2)  # this is necessary
    actions = ActionChains(browser)
    actions.send_keys(Keys.TAB * 7 + Keys.ENTER)
    actions.perform()


def play_songs(username: str, password: str, links: list, browser):
    PROXY_NUMBER = 1
    tidal = Tidal(browser, username, password)
    for link in links:
        tidal.url = link
        logging.info(f'Page URL {tidal.url}.')
        try:
            tidal.setup()
            logging.info('Page setup completed.')
            time.sleep(10)
            tidal.stream_song()
            for i in range(SONGS_PER_URL):
                song_play_time = tidal.get_song_random_point()
                logging.info(f'Play song for {song_play_time} sec.')
                logging.info(f'Current song info: {tidal.get_song_details()}')
                time.sleep(song_play_time)
                logging.info('Playing next song.')
                tidal.play_next_song()
        except Exception as e:
            logging.error(f'Error: {e}')
            if tidal.is_blocked():
                pass
                # proxy can be updated here. Close browser and reopen with proxy.
                PROXY_NUMBER += 1


def play_song_on_each_user(credentials, urls, browser):
    for user in credentials:
        play_songs(user[0], user[1], links, browser)
        clear_browser_cache()


def install_browsec(browser):
    browser.get("chrome-extension://bhbolmecjmfonpkpebccliojaipnocpc/popup/popup.html")
    browser.execute_script(
        "document.querySelector('page-switch').shadowRoot.querySelector('main-index').shadowRoot.querySelector('c-switch').click()"
    )


def initialize_browser(proxy=None):
    options = driver.ChromeOptions()
    # options.add_argument(f"--proxy-server=%s" % proxy)

    EXTENION_PATH = os.path.abspath("extensions")
    options.add_argument(f"--load-extension={EXTENION_PATH}")

    browser = driver.Chrome(options=options)
    install_browsec(browser)
    return browser


if __name__ == '__main__':
    try:
        credentials = get_credentials("credentials.txt")
        links = get_urls('urls.txt')
        PROXY_LIST = get_porxy('proxy.txt')
        
        browser = initialize_browser()
        play_song_on_each_user(credentials, links, browser)

    except Exception as e:
        logging.error(e)

    finally:
        browser.close()
