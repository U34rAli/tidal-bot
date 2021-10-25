
import os
from selenium.webdriver.common.keys import Keys
from bot.driver import get_driver

driver = get_driver( os.path.join(os.getcwd(), "drivers") )
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()