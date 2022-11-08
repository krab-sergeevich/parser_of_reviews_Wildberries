""" That's a program to parse reviews about some product from Wildberries web-site """
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire import webdriver


def scroll_page():
    """ scrolling to the end of the page"""


def parse_info_and_dump():
    """ take info and dump in csv file """


options = {'proxy': {
    'http': "http://082DwD:c451Jd@91.188.243.73:9059",
    'https': "https://082DwD:c451Jd@91.188.243.73:9059",
}}
s = Service('/Users/macbookpro/Desktop/chromedriver')
URL = 'https://www.wildberries.ru/catalog/21659599/feedbacks?imtId=10317392'
browser = webdriver.Chrome(service=s, seleniumwire_options=options)
browser.get(URL)
print(browser.find_element(By.CLASS_NAME, 'feedback__text').text)
time.sleep(1)
