from random import randrange
import time
from bot.tidal import Tidal
import undetected_chromedriver.v2 as driver
import os
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)


def get_credentials(filename: str):
    with open(filename, "r") as file:
        credentials_string = file.readlines()
        credentials = [tuple(c.strip().split(":")) for c in credentials_string]
    return credentials or []


def play_songs(username: str, password: str, links: list, browser):
    tidal = Tidal(browser, username, password)
    for link in links:
        tidal.url = link
        logging.info(f'Page URL {tidal.url}.')
        try:
            tidal.setup()
            logging.info('Setup the page.')
            time.sleep(10)
            tidal.stream_song()
            number_of_songs_to_play = randrange(2, 10, 1)
            for i in range(number_of_songs_to_play-1):
                song_play_time = tidal.get_song_random_point()
                logging.info(f'Play song for {15} sec.')
                logging.info(f'Current song info: {tidal.get_song_details()}')
                time.sleep(30)
                tidal.play_next_song()
                logging.info('Playing next song.')
        except Exception as e:
            logging.error(f'Error: {e}')
            print(e)


if __name__ == '__main__':
    try:
        options = driver.ChromeOptions()
        PROXY = "23.107.176.19:32180"
        # options.add_argument("--proxy-server=%s" % PROXY)
        EXTENION_PATH = os.path.abspath("extensions")
        exe_path = os.path.abspath(os.path.join("drivers", "chromedriver.exe"))


        EXTENION_PATH = os.path.abspath("extensions")
        options.add_argument(f"--load-extension={EXTENION_PATH}")


        browser = driver.Chrome(options=options)

        browser.get("chrome-extension://bhbolmecjmfonpkpebccliojaipnocpc/popup/popup.html")
        browser.execute_script(
            "document.querySelector('page-switch').shadowRoot.querySelector('main-index').shadowRoot.querySelector('c-switch').click()"
        )


        credentials = get_credentials("credentials.txt")
        links = [
            "https://listen.tidal.com/artist/10003047",
            "https://listen.tidal.com/album/186907408",
            "https://listen.tidal.com/playlist/fdf9201c-5e21-462f-a50f-33e31566ee74",
        ]

        play_songs(credentials[0][0], credentials[0][1], links, browser)

    except Exception as e:
        print(e)
    finally:
        browser.close()
