
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot.driver import get_driver

browser = get_driver( os.path.join(os.getcwd(), "drivers") )
browser.get("https://listen.tidal.com/artist/10003047")

try:
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "login-button"))
    )
    element.click()
    print("Page is ready!")

finally:
    browser.quit()

browser.close()