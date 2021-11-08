from random import randrange
import random
import time
from bot.tidal import Tidal
import undetected_chromedriver.v2 as driver
import os
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import argparse


logging.basicConfig(filename='app.log', level=logging.INFO)

LINKS_PER_ACCOUNT = 10
SONGS_PER_URL = 10
LIKE_SONG_CHANCE = 20
FOLLOW_ARTIST_CHANCE = 20
MINIMUM_SONGS_PER_LINK = 5
MAX_SONGS_PER_LINK = 20
MINIMUM_LINKS_PER_ACCOUNT = 1
MAX_LINKS_PER_ACCOUTN = 20
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


def clear_browser_cache(browser):
    browser.get("chrome://settings/clearBrowserData")
    time.sleep(2)  # this is necessary
    actions = ActionChains(browser)
    actions.send_keys(Keys.TAB * 7 + Keys.ENTER)
    actions.perform()


def decide_like(tidal:Tidal):
    like = random.randint(0,100)
    if like < LIKE_SONG_CHANCE:
        logging.info('Liking the song.')
        tidal.like_song()


def decide_follow(tidal:Tidal):
    follow = random.randint(1,100)
    if follow < FOLLOW_ARTIST_CHANCE:
        logging.info('Folling the Artist.')
        tidal.follow_artist()


def play_songs(username: str, password: str, links: list, browser):
    PROXY_NUMBER = 1
    tidal = Tidal(browser, username, password)
    logging.info(f'No. of links {len(links)}')
    for link in links:
        tidal.url = link
        logging.info(f'Page URL {tidal.url}.')
        try:
            tidal.setup()
            logging.info('Page setup completed.')
            logging.info(f'Songs Per Link = {SONGS_PER_URL}.')
            time.sleep(5)
            tidal.stream_song()
            for i in range(SONGS_PER_URL):
                song_play_time = tidal.get_song_random_point()
                logging.info(f'Play song for {song_play_time} sec.')
                logging.info(f'Current song info: {tidal.get_song_details()}')
                time.sleep(1)
                decide_like(tidal)
                time.sleep(song_play_time)
                logging.info('Playing next song.')
                tidal.play_next_song()
            time.sleep(2)
            decide_follow()
        except Exception as e:
            logging.error(f'Error: {e}')
            if tidal.is_blocked():
                # proxy can be updated here. Close browser and reopen with proxy.
                PROXY_NUMBER += 1
                pass


def play_song_on_each_user(credentials, urls, browser):
    for user in credentials:
        play_songs(user[0], user[1], random.sample(urls, LINKS_PER_ACCOUNT), browser)
        clear_browser_cache(browser)


def install_browsec(browser):
    browser.get("chrome-extension://bhbolmecjmfonpkpebccliojaipnocpc/popup/popup.html")
    browser.execute_script(
        "document.querySelector('page-switch').shadowRoot.querySelector('main-index').shadowRoot.querySelector('c-switch').click()"
    )


def initialize_browser(proxy=None):
    options = driver.ChromeOptions()
    # options.add_argument(f"--proxy-server=%s" % proxy)

    EXTENION_PATH = os.path.abspath("extensions")
    # options.add_argument(f"--load-extension={EXTENION_PATH}")

    browser = driver.Chrome(options=options)
    # install_browsec(browser)
    return browser


def initialize_variables(opt, max_links_len):
    global SONGS_PER_URL, LINKS_PER_ACCOUNT, LIKE_SONG_CHANCE, FOLLOW_ARTIST_CHANCE, MAX_SONGS_PER_LINK, MAX_LINKS_PER_ACCOUTN
    SONGS_PER_URL = opt.songs if opt.songs > 0 else randrange(MINIMUM_SONGS_PER_LINK, MAX_SONGS_PER_LINK, 1)
    LINKS_PER_ACCOUNT = opt.links if opt.links > 0 else randrange(MINIMUM_LINKS_PER_ACCOUNT, MAX_LINKS_PER_ACCOUTN%max_links_len, 1)
    LIKE_SONG_CHANCE = opt.like%100 if opt.like > 0 else randrange(0, opt.like%100, 1)
    FOLLOW_ARTIST_CHANCE = opt.follow%100 if opt.follow > 0 else randrange(0, opt.follow%100, 1)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--songs', nargs='+', type=int, default=0, help='Number of songs per URL.')
        parser.add_argument('--links', type=int, default=0, help='Number of Link per Account.')  # file/folder, 0 for webcam
        parser.add_argument('--like', type=int, default=50, help='Chance of liking a song.')
        parser.add_argument('--follow', nargs='+', default=50, type=int, help='Chance of following a song.')
        opt = parser.parse_args()
        
        credentials = get_credentials("credentials.txt")
        links = get_urls('urls.txt')
        PROXY_LIST = get_porxy('proxy.txt')
        initialize_variables(opt, len(links))
        
        browser = initialize_browser()
        play_song_on_each_user(credentials, links, browser)

    except Exception as e:
        logging.error(e)
