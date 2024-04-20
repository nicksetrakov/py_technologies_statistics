import csv
import logging
import sys
import time
from dataclasses import astuple
from datetime import datetime
from item import Vacancy, VACANCY_FIELDS
from config import VACANCIES_URL

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s] - %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


def parse_single_vacancy(vacancy: WebElement) -> Vacancy:
    title = vacancy.find_element(By.CSS_SELECTOR, "a.h3.job-list-item__link").text

    logging.info("parse_single_vacancy(%s)", title)

    date = vacancy.find_element(
        By.CSS_SELECTOR, "span.mr-2.nobr"
    ).get_attribute("data-original-title")

    date = datetime.strptime(date, "%H:%M %d.%m.%Y")

    job_info = [
        element.text.replace("· ", "")
        for element in vacancy.find_elements(
            By.CSS_SELECTOR, ".job-list-item__job-info.font-weight-500 > span.nobr"
        )
    ]

    views, responses = [
        int(element.get_attribute("data-original-title").split()[0])
        for element in vacancy.find_elements(
            By.CSS_SELECTOR, "span.job-list-item__counts.d-none.d-lg-inline-block.nobr "
                             "> span.text-muted > span.nobr > span.mr-2"
        )
    ]
    salary = vacancy.find_elements(By.CLASS_NAME, "public-salary-item")

    return Vacancy(
        date=date,
        title=title,
        location=vacancy.find_element(By.CLASS_NAME, "location-text").text,
        job_info=job_info,
        description=vacancy.find_element(By.CLASS_NAME, "job-list-item__description").text,
        views=views,
        responses=responses,
        salary=salary[0].text if salary else None
    )


def parse_single_page(url: str, driver: webdriver.Chrome) -> list[Vacancy]:
    driver.get(url)
    details_button = driver.find_elements(By.CSS_SELECTOR, "a[data-toggle='show-more'] > span.nobr")

    for button in details_button:
        if button.is_displayed():
            button.click()
            time.sleep(0.1)

    vacancy_cards = driver.find_elements(By.CSS_SELECTOR, ".list-jobs__item.job-list__item")

    return [parse_single_vacancy(vacancy) for vacancy in vacancy_cards]


def write_to_csv(vacancies: list[Vacancy]) -> None:
    logging.info("Start writing to csv")

    with open("vacancies.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(VACANCY_FIELDS)
        writer.writerows([astuple(vacancy) for vacancy in vacancies])

    logging.info("Finished writing to csv")


def get_all_products() -> None:
    chrome_options = Options()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(VACANCIES_URL)

    pages = int(driver.find_elements(By.CLASS_NAME, "page-link")[-2].text)

    all_vacancies = []

    for page in range(1, pages + 1):
        logging.info("Parsing page %s", page)
        all_vacancies.extend(parse_single_page(VACANCIES_URL + f"&page={page}", driver))

    driver.quit()

    write_to_csv(all_vacancies)


if __name__ == '__main__':
    get_all_products()
