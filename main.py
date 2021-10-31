from random import randrange
from bot.tidal import Tidal
import undetected_chromedriver.v2 as driver


def get_credentials(filename: str):
    with open(filename, 'r') as file:
        credentials_string = file.readlines()
        credentials = [tuple(c.strip().split(':')) for c in credentials_string]
    return credentials or []

try:
    options = driver.ChromeOptions()
    PROXY = '23.107.176.19:32180'
    # options.add_argument("--proxy-server=%s" % PROXY)
    browser = driver.Chrome(options=options)
    credentials = get_credentials('credentials.txt')

    links = [
        'https://listen.tidal.com/artist/10003047',
        'https://listen.tidal.com/album/186907408',
        'https://listen.tidal.com/playlist/fdf9201c-5e21-462f-a50f-33e31566ee74',
    ]

    tidal = Tidal(browser, links[0], credentials[0][0], credentials[0][1],)
    tidal.setup()
    tidal.stream_song()

    
except Exception as e:
    print(e)
finally:
    browser.close()
