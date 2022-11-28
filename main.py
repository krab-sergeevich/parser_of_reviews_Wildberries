""" That's a program to parse reviews about some product from Wildberries web-site """
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

s: Service = Service('/Users/macbookpro/Desktop/chromedriver')
URL: str = 'https://www.wildberries.ru/catalog/21659599/feedbacks?imtId=10317392'
browser: webdriver = webdriver.Chrome(service=s)

