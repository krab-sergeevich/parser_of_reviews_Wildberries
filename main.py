""" That's a program to parse reviews about some product from Wildberries web-site """
import csv
import logging
from datetime import date

import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

s: Service = Service('/Users/macbookpro/Desktop/chromedriver')
browser: webdriver = webdriver.Chrome(service=s)
logging.basicConfig(filename='app.log', filemode='w', format='%(process)d-%(levelname)s-%(message)s',
                    level=logging.INFO)


def scroll_page(browser_local: webdriver):
    """ scrolling to the end of the page"""
    last_height: browser_local = browser_local.execute_script("return document.body.scrollHeight")
    logging.info("Take height of the page")
    while True:
        browser_local.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.info("Scroll page to the down")
        browser.implicitly_wait(65.0)
        logging.info("Wait for loading new information")
        new_height: browser_local = browser_local.execute_script("return document.body.scrollHeight")
        logging.info("Take new height of the page")
        if new_height == last_height:
            break
        last_height: browser_local = new_height


def dump_result_csv(review_info_local: list[list[str]], review_text_local: list[str], number_local) -> None:
    """ take info and dump in csv file """
    with open(f'result{number_local}.csv', 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(['Имя заказчика', 'Дата отзыва', 'Цвет', 'Размер', 'Комментарий', 'Дата парсинга'])
        logging.info("Write first row to csv to create names of columns")
        for i, j in zip(review_info_local, review_text_local):
            writer.writerow([i[0], i[1], i[2][6:], i[3][8:], j, str(date.today().strftime("%d/%m/%Y"))])
        logging.info("Write infomation in csv file")


def dump_result_pandas(review_info_local: list[list[str]], review_text_local: list[str]) -> pd.Series:
    """ take info and dump in pandas series """
    for info_element, review_element in zip(review_info_local, review_text_local):
        count_of_review: int = 1
        ljust_formatter = max(len(review_element), len(info_element[3][8:]))
        dct = {"Номер отзыва": str(count_of_review).ljust(ljust_formatter),
               "Имя": info_element[0].ljust(ljust_formatter),
               "Дата отзыва": info_element[1].ljust(ljust_formatter),
               "Цвет": info_element[2][6:].ljust(ljust_formatter),
               "Размер": info_element[3][8:].ljust(ljust_formatter),
               "Отзыв": review_element.ljust(ljust_formatter),
               "Дата парсинга": str(date.today().strftime('%d/%m/%Y')).ljust(ljust_formatter)}
        if count_of_review == 1:
            series = pd.Series(dct)
            logging.info("Create pandas series and write information in series")
        else:
            series.append(pd.Series(dct))
            logging.info("Write infomation in series")
        count_of_review += 1
    return series


if __name__ == "__main__":
    list_of_links = ['https://www.wildberries.ru/catalog/21659599/feedbacks?imtId=10317392',
                     'https://www.wildberries.ru/catalog/37899721/feedbacks?imtId=28503636',
                     'https://www.wildberries.ru/catalog/103125061/feedbacks?imtId=79985311']
    for number, link in enumerate(list_of_links, 1):
        browser.get(link)
        logging.info("browset get link")
        scroll_page(browser)
        review_info = [row.text.split('\n') for row in browser.find_elements(By.CLASS_NAME, "feedback__info")]
        review_text = [review.text for review in browser.find_elements(By.CLASS_NAME, "feedback__text")]
        logging.info("Take name, date, color, size, text_of_reviews from page")
        dump_result_csv(review_info, review_text, number)
        logging.info("FINISHED!")
