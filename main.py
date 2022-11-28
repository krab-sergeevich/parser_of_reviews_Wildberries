""" That's a program to parse reviews about some product from Wildberries web-site """
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

s: Service = Service('/Users/macbookpro/Desktop/chromedriver')
URL: str = 'https://www.wildberries.ru/catalog/21659599/feedbacks?imtId=10317392'
browser: webdriver = webdriver.Chrome(service=s)


def scroll_page(browser_local: webdriver):
    """ scrolling to the end of the page"""
    scroll_pause_time: float = 1.5

    # Get scroll height
    last_height: browser_local = browser_local.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser_local.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height: browser_local = browser_local.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height: browser_local = new_height


def dump_result_in_txt(name_data_color_size_local: list[str], reviews_of_customers_local: list[str]):
    """ take info and dump in json file """
    count: int = 1
    with open("reviews.txt", "w", encoding="utf-8") as file:
        for info_of_review, text_of_review in zip(name_data_color_size_local, reviews_of_customers_local):
            file.write(f'Номер отзыва: {count}\n{info_of_review}\n{text_of_review}\n\n')
            count += 1


browser.get(URL)
scroll_page(browser)
name_date_color_size = [i.text for i in browser.find_elements(By.CLASS_NAME, "feedback__info")]
reviews_of_customers = [i.text for i in browser.find_elements(By.CLASS_NAME, "feedback__text")]
dump_result_in_txt(name_date_color_size, reviews_of_customers)

# options: dict = {'proxy': {
#     'http': "http://082DwD:c451Jd@91.188.243.73:9059",
#     'https': "https://082DwD:c451Jd@91.188.243.73:9059",
# }}
