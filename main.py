from bot.tidal import Tidal
import undetected_chromedriver.v2 as driver


try:
    browser = driver.Chrome()
    tidal = Tidal(
        browser,
        "https://listen.tidal.com/artist/10003047",
        "majesticeagle1@gmail.com",
        "snob86dew",
    )
    tidal.setup()
    tidal.stream_song()
except Exception as e:
    print(e)
finally:
    browser.close()
