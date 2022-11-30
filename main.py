""" That's a program to parse reviews about some product from Wildberries web-site """
from datetime import date
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import pandas as pd

s: Service = Service('/Users/macbookpro/Desktop/chromedriver')
URL: str = 'https://www.wildberries.ru/catalog/21659599/feedbacks?imtId=10317392'
browser: webdriver = webdriver.Chrome(service=s)


def scroll_page(browser_local: webdriver):
    """ scrolling to the end of the page"""
    # scroll_pause_time: float = 3.0

    # Get scroll height
    last_height: browser_local = browser_local.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser_local.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        # time.sleep(scroll_pause_time)
        browser.implicitly_wait(60.0)

        # Calculate new scroll height and compare with last scroll height
        new_height: browser_local = browser_local.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height: browser_local = new_height


# def dump_result_in_txt(name_data_color_size_local: list[str], reviews_of_customers_local: list[str]):
#     """ take info and dump in txt file """
#     count: int = 1
#     with open("reviews.txt", "w", encoding="utf-8") as file:
#         for info_of_review, text_of_review in zip(name_data_color_size_local, reviews_of_customers_local):
#             file.write(f'Номер отзыва: {count}\n{info_of_review}\n{text_of_review}\n\n')
#             count += 1


def dump_result_in_pandas(name_data_color_size_local: list[list[str]], reviews_of_customers_local: list[str]):
    """ take info and dump in pandas series """
    for info_element, review_element in zip(name_data_color_size_local, reviews_of_customers_local):
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
        else:
            series.append(pd.Series(dct))
        count_of_review += 1
    return series


if __name__ == "__main__":
    browser.get(URL)
    scroll_page(browser)
    name_date_color_size = [i.text.split('\n') for i in browser.find_elements(By.CLASS_NAME, "feedback__info")]
    reviews_of_customers = [i.text for i in browser.find_elements(By.CLASS_NAME, "feedback__text")]
    print(dump_result_in_pandas(name_date_color_size, reviews_of_customers))
#new comment
