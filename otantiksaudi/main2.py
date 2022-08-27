from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import os
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np
import requests
import pandas as pd
import re
from selenium.webdriver.support.ui import Select
from dataclasses import dataclass, field


def try_except(name):
        try:
            return name.first_selected_option.text
        except:
            return None
        
        
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


@dataclass
class Ansaaj:
    # sku: str = field(init=False)
    # titles: str = field(init=False)
    # price: str = field(init=False)
    # special_price: str = field(init=False)
    # description: str = field(init=False)
    # base_image: str = field(init=False)
    # add_images: str = field(init=False)
    # size: str = field(init=False)
    # qty: str = field(init=False)
    # type_: str= field(init=False)
    # list_selects: list[str] = field(init=False)
    # driver: webdriver = field(init=True)

    def __init__(self, driver):
        self.sku = None
        self.titles = None
        self.price = None
        self.special_price = None
        self.description = None
        self.base_image = None
        self.add_images = None
        self.size = None
        self.qty = None
        self.type_ = None
        self.free_colors = None
        self.size_products = None
        self.pieces_numbers = None
        self.list_selects = []
        self.driver = driver
        
    


    def get_url(self, url):
        self.driver.get(url)
        
    def send_soup(self):
        text = self.driver.find_element_by_tag_name('body').get_attribute('innerHTML')
        soup = BeautifulSoup(text, 'html.parser')
        return soup 
    
    def extract_url(self):
        pass
    
    def extract_product(self, url):
        soup = self.send_soup()
        try:
            self.sku = soup.find('span', {'class': 'sku'}).text.strip()
        except:
            pass
        
        self.titles = soup.find('h1', {'class': 'product_title entry-title wd-entities-title'}).text.strip()
        
        try:
            self.price = soup.find('p', {'class': 'price'}).find('del').text.replace('ر.س', '').strip()
            self.special_price = soup.find('p', {'class': 'price'}).find('ins').text.replace('ر.س', '').strip()
        except:
            self.price = soup.find('p', {'class': 'price'}).text.replace('ر.س', '').strip()
            self.special_price = 0
        try:
            self.qty = soup.find('p', {'class': 'stock in-stock'}).text.replace('متوفر في المخزون', '').strip()
        except:
            self.qty = ''
        self.type_ = soup.find('span', {'class': 'posted_in'}).text.replace('التصنيف:', '').strip()
        try:
            self.description = soup.find('div', {'id': 'tab-description'}).text.strip()
        except:
            pass
        images = soup.find_all('figure', {'class': 'woocommerce-product-gallery__image'})
        list_img = [img.find('img')['src'].split('') for img in images]
        self.base_image = list_img[0]
        self.add_images = ','.join(list_img[1:])
        
        
        selects = self.driver.find_elements_by_xpath('//select')
        for sele in selects:
            #print(sele.get_attribute('id'))
            if sele.get_attribute('id') != 'rating' and sele.get_attribute('id') != 'pa_color' and sele.get_attribute('id') != 'pa_style':
                self.list_selects.append(sele.get_attribute('id'))
    
    def scrap_product(self, url):
        print('Iam in scrap_product')
        selects = driver.find_elements_by_xpath('//select')
        len(selects)
        list_selects = [sele.get_attribute('id') for sele in selects if sele.get_attribute('id') != 'rating' and sele.get_attribute('id') != 'pa_color' and sele.get_attribute('id') != 'pa_style']
        
        if len(list_selects) == 1:
            print('Choices 1')
            try:
                # المقاس
                size_name = list_selects[0]
                btn = driver.find_elements_by_xpath(f'//select[@id="{size_name}"]//option')
                count = len(btn)
                select = Select(driver.find_element_by_id(size_name))
                data = []
                for i in range(1, count):
                    print('Count: ', i )
                    select.select_by_index(i)
                    self.size_products = try_except(select)
                    time.sleep(2)
                    self.extract_product(url)
                    try:
                        self.price = driver.find_element_by_xpath('//div[@class="single_variation_wrap"]//span[@class="price"]//del').text
                        self.special_price = driver.find_element_by_xpath('//div[@class="single_variation_wrap"]//span[@class="price"]//ins').text
                    except:
                        try:
                            self.price = driver.find_element_by_xpath('//div[@class="single_variation_wrap"]//span[@class="price"]').text
                            self.special_price = ''
                        except:
                            
                            pass
                    
                    
                    data.append( {
                            'sku': self.sku,
                            'name': self.titles,
                            'price': self.price,
                            'special_price': self.special_price,
                            'link_url': url['url'],
                            'qty': self.qty,
                            'type_': self.type_,
                            'free_colors': self.free_colors,
                            'size_products': self.size_products,
                            'pieces_numbers': self.pieces_numbers,
                            'description': self.description,
                            'list_select': self.list_selects,
                            'base_images': self.base_image,
                            'additionnel_images': self.add_images,
                            'categories1': url['cat1'],   
                            'categories2': url['cat2'],   
                        })
            except:
                size_name = list_selects[0]
                print(size_name)
                elements = driver.find_elements_by_xpath(f'//div[@data-id="pa_size"]//div')
                count = len(elements)
                print('len: ', count)
                # select = Select(driver.find_element_by_id(size_name))
                for ele in elements:
                    time.sleep(1)
                    ele.click()
                    self.size_products = ele.text
                    self.extract_product(url)
                    try:
                        self.price = driver.find_element_by_xpath('//div[@class="single_variation_wrap"]//span[@class="price"]//del').text
                        self.special_price = driver.find_element_by_xpath('//div[@class="single_variation_wrap"]//span[@class="price"]//ins').text
                    except:
                        try:
                            self.price = driver.find_element_by_xpath('//div[@class="single_variation_wrap"]//span[@class="price"]').text
                            self.special_price = ''
                        except:
                            
                            pass
                    
                    data.append( {
                            'sku': self.sku,
                            'name': self.titles,
                            'price': self.price,
                            'special_price': self.special_price,
                            'link_url': url['url'],
                            'qty': self.qty,
                            'type_': self.type_,
                            'free_colors': self.free_colors,
                            'size_products': self.size_products,
                            'pieces_numbers': self.pieces_numbers,
                            'description': self.description,
                            'list_select': self.list_selects,
                            'base_images': self.base_image,
                            'additionnel_images': self.add_images,
                            'categories1': url['cat1'],   
                            'categories2': url['cat2'],   
                        })
            return data          
            
        elif len(list_selects) == 2:
            print('Choices 2')
            # المقاس
            size_name = list_selects[0]
            btn = driver.find_elements_by_xpath(f'//select[@id="{size_name}"]//option')
            count = len(btn)
            print('Count: ', count)
            select = Select(driver.find_element_by_id(size_name))

            # نوع الشرشف
            type_ = list_selects[1]
            btn1 = driver.find_elements_by_xpath(f'//select[@id="{type_}"]//option')
            #btn1 = driver.find_elements_by_xpath('//select[@id="pa_%d9%86%d9%88%d8%b9-%d8%a7%d9%84%d8%b4%d8%b1%d8%b4%d9%81"]//option[@class="attached enabled"]')
            count1 = len(btn1)
            print('Count: ', count1)
            select1 = Select(driver.find_element_by_id(type_))
            data = []
            # MAIN FOR LOOP 
            for i in range(1, count):
                try:
                    select.select_by_index(i)
                    self.size_products = try_except(select)
                    time.sleep(2)
                except:
                    continue
                for j in range(1, count1):
                    print('i: ', i)
                    print('j: ', j)
                    try:
                        select1.select_by_index(j)
                        time.sleep(3)
                    except:
                        continue
                    self.extract_product(url)
                    try:
                        self.price = driver.find_element_by_xpath('//div[@class="single_variation_wrap"]//span[@class="price"]').text
                    except:
                        pass
                    try:
                        self.special_price = driver.find_element_by_xpath('//div[@class="single_variation_wrap"]//span[@class="price"]').text
                    except:
                        pass
                    self.pieces_numbers = try_except(select1)
                    data.append( {
                        'sku': self.sku,
                        'name': self.titles,
                        'price': self.price,
                        'special_price': self.special_price,
                        'link_url': url['url'],
                        'qty': self.qty,
                        'type_': self.type_,
                        'free_colors': self.free_colors,
                        'size_products': self.size_products,
                        'pieces_numbers': self.pieces_numbers,
                        'description': self.description,
                        'list_select': self.list_selects,
                        'base_images': self.base_image,
                        'additionnel_images': self.add_images,
                        'categories1': url['cat1'],   
                        'categories2': url['cat2'],   
                    })
            return data

        else:
            print('Choices 3')
            self.extract_product(url)
            data = []
            data.append( {
            'sku': self.sku,
            'name': self.titles,
            'price': self.price,
            'special_price': self.special_price,
            'link_url': url['url'],
            'qty': self.qty,
            'type_': self.type_,
            'free_colors': self.free_colors,
            'size_products': self.size_products,
            'pieces_numbers': self.pieces_numbers,
            'description': self.description,
            'list_select': self.list_selects,
            'base_images': self.base_image,
            'additionnel_images': self.add_images,
            'categories1': url['cat1'],   
            'categories2': url['cat2'],   
            })
            return data  
        
            
        
    def return_data(self, url):
        self.extract_product(url)
        return {
        'sku': self.sku,
        'name': self.titles,
        'price': self.price,
        'special_price': self.special_price,
        'link_url': url['url'],
        'qty': self.qty,
        'type_': self.type_,
        'free_colors': self.free_colors,
        'size_products': self.size_products,
        'pieces_numbers': self.pieces_numbers,
        'description': self.description,
        'list_select': self.list_selects,
        'base_images': self.base_image,
        'additionnel_images': self.add_images,
        'categories1': url['cat1'],   
        'categories2': url['cat2'],   
        }    
        
    def save_data(self):
        pass    
    
    def scraping(self, url):
        print('Iam in scraping')
        selects = driver.find_elements_by_xpath('//select')
        data = []
        list_selects = [sele.get_attribute('id') for sele in selects ]
        if 'pa_color' in list_selects:
            print('Color find')
            toto = driver.find_elements_by_xpath('//div[@data-id="pa_color"]//div')
            print(len(toto))
            for i, t in enumerate(toto):
                print('i', i)
                t.click()
                self.free_colors = t.text
                print('colors: ', self.free_colors)
                time.sleep(2)
                data =  data + self.scrap_product(url)
        else:
            print('No color')
            data =  data + self.scrap_product(url)
        return data       


df = pd.read_excel('anssaj_product_model1.xlsx')
urls = pd.read_excel('ansaaj_url1.xlsx')
list_urls = []
for index, row in urls.iterrows():
    list_urls.append(
        {
            'url': row['url'],
            'cat1': row['cat1'],
            'cat2': row['cat2'],
        }
    )

for i, url in enumerate(list_urls):
    ansaaj = Ansaaj(driver)
    print('Count: ', i)
    url1 = url['url']
    
    print('URL: ', url1)
    ansaaj.get_url(url1)
    
    data = ansaaj.scraping(url)

    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('anssaj_product_up1.xlsx')