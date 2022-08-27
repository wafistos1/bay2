import time
import os
import logging
import requests
import re
from dataclasses import dataclass
from random import randint
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def return_id_ele(name, soup):
    return soup.find('h5', text=name).next_element.next_element.next_element.next_element.next_element['id']

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


WORNG_MESSAGE = 'رقم الهاتف تم الحجز به مسبقاً يرجى الانتظار 30 يوم للحجز مرة اخرى'
SEVICE_TYPE_LIST = [
    {'1': '>الواقعات الحياتية' },
    {'2': '>تسجيل لأول مرة:'}
]
NAME_CIRCONSIPTION_LIST = [
    {'1': '>دائرة احوال الرصافة' },
    {'2': '>دائرة احوال بغداد الجديدة' },
    {'3': '>دائرة احوال الكرادة الشرقية' },
    {'4': '>دائرة احوال الراشدية' },
    {'4': '>دائرة احوال الموصل الايمن' },
]
MEAL_LIST = [
    {'1': '>صباحي'},
]
NUMBER_FAMILY_LIST = [
    {'1': '>1'},
    {'2': '>2'},
    {'3': '>3'},
    {'4': '>4'},
    {'4': '>4'},
    {'5': '>5'},
    {'6': '>6'},
    {'7': '>7'},
    {'8': '>8'},
    {'9': '>9'},
]
click_for_confirmation = 'اضغط هنا لإكمال عملية الحجز'
click_phone_confirmation = 'تسجيل الدخول'
@dataclass
class Person:
    """Class for keeping track of an item in inventory."""
    first_name: str
    last_name: str
    third_name: str
    phone: str
    id_service_type: str  #  'نوع المعاملة'
    name_cir: str # اسم دائرة الاحوال
    meal: str #  الوجبة
    familly_number: str # 'عدد افراد الاسرة'


# Open link
driver.get('https://reg.nid-moi.gov.iq/')

def get_data_first_page(person: Person, driver):
    # Enter name1 --- > phone
    wait = WebDriverWait(driver, 10)
    first_name = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//input[@name="FirstName"]')))
    first_name.send_keys(person.first_name)
    last_name = driver.find_element_by_xpath('//input[@name="SecondName"]').send_keys(person.last_name)
    third_name = driver.find_element_by_xpath('//input[@name="ThirdName"]').send_keys(person.third_name)
    phone = driver.find_element_by_xpath('//input[@name="Phone"]').send_keys(person.phone)

    # Fresh data
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    
    # Set servie type 'نوع المعاملة'
    id_service_type =name_cir = return_id_ele('نوع المعاملة', soup)
    wait.until(EC.element_to_be_clickable((By.ID, f'{id_service_type}'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[@aria-label="{person.id_service_type}"]'))).click()
    # driver.find_element_by_id(f'{id_service_type}').click()
    # driver.find_element_by_xpath(f'//li[@aria-label="{person.id_service_type}"]').click()
    
    # Set Name circonsiption 'اسم دائرة الاحوال'
    name_cir = return_id_ele('اسم دائرة الاحوال', soup)
    # driver.find_element_by_id(f'{name_cir}').click()
    # driver.find_element_by_xpath(f'//li[@aria-label="{person.name_cir}"]').click()
    wait.until(EC.element_to_be_clickable((By.ID, f'{name_cir}'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[@aria-label="{person.name_cir}"]'))).click()
    
    # Set Meal الوجبة
    name_toto = return_id_ele('الوجبة', soup)
    # driver.find_element_by_id(f'{name_toto}').click()
    # driver.find_element_by_xpath(f'//input[@id="search-{name_toto}"]').click()
    # driver.find_element_by_xpath(f'//li[@aria-label="{person.meal}"]').click()
    wait.until(EC.element_to_be_clickable((By.ID, f'{name_toto}'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f'//input[@id="search-{name_toto}"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[@aria-label="{person.meal}"]'))).click()
    
    # Set Family number 'عدد افراد الاسرة'
    familly_number = return_id_ele('عدد افراد الاسرة', soup)
    # driver.find_element_by_id(f'{familly_number}').click()
    # driver.find_element_by_xpath(f'//input[@id="search-{familly_number}"]').click()
    # driver.find_element_by_xpath(f'//li[@aria-label="{person.familly_number}"]').click()
    wait.until(EC.element_to_be_clickable((By.ID, f'{familly_number}'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f'//input[@id="search-{familly_number}"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, f'//li[@aria-label="{person.familly_number}"]'))).click()
    
    # Click next
    enter_button = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//span[text()="تسجيل الدخول"]')))
    enter_button.click()

def get_confirmation_page(person: Person, driver):
    wait = WebDriverWait(driver, 10)
    confirme_input = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//input[@name="ConfirmCode"]')))
    confirme_input.send_keys(person.phone)
    time.sleep(2)
    # register_btn = driver.find_element_by_class_name('rz-button-text')
    register_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'rz-button-text')))
    register_btn.click()
    time.sleep(4)
    # confirmation_btn = driver.find_element_by_class_name('btn-success')
    confirmation_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-success')))
    confirmation_btn.click()
    click_for_confirmation = 'اضغط هنا لإكمال عملية الحجز'
    return driver.find_element_by_xpath(f'//span[text()="{click_for_confirmation}"]').text


if __name__=='__main__':
    driver.get('https://reg.nid-moi.gov.iq/')
    time.sleep(1)
    person = Person(
    'احمد',
    'سلام',
    'سلام',
    '07824255360',
    SEVICE_TYPE_LIST[0]['1'],
    NAME_CIRCONSIPTION_LIST[0]['1'],
    MEAL_LIST[0]['1'],
    NUMBER_FAMILY_LIST[0]['1'],
    )

    get_data_first_page(person, driver)
    logging.info('Go Reservation Page.')
    time.sleep(1)
    RESERVATION = get_confirmation_page(person, driver)
    if RESERVATION != WORNG_MESSAGE:
        logging.info('Reservation Success')
    else:
        logging.info('Fail reservation.')
