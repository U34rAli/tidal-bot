
import os
from selenium.webdriver.chrome import options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


from bot.driver import get_driver
from bot.tidal import Tidal


try:
    browser = get_driver( os.path.join(os.getcwd(), "drivers") )
    tidal = Tidal(browser, "https://listen.tidal.com/artist/10003047", 'xxxxx@gmail.com', 'xxxxx')
    tidal.play_song()

finally:
    browser.close()
