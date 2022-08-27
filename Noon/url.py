from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup



def get_data(url, driver):
    driver.get(url)
    r = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class':'productContainer'})
    len(products)
    list_products = ['https://www.noon.com' + pr.find('a')['href'] for pr in products]
    print('Len products', len(list_products))
    data = []
    for t in list_products:
        data.append({
            'url': t,
            })
    return list_products


def getnextpage(driver):
    try:
        next_page = driver.find_element_by_xpath('//a[@aria-label="Next page"]')
        next_page.click()
        time.sleep(5)
        url = driver.current_url
        return url
    except:
        return None 


list_urls = []


def scrap_url_product(url, driver):
    data = []
    
    urls_list = get_data(url, driver)
    for toto in urls_list:
        data.append({
        'url':toto,
        })

    # print(data)
    print( f'Scrape done .')
    return data


df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/Noon/Noon_url_model.xlsx')

list_url = [
    'https://www.noon.com/saudi-ar/home-and-kitchen/p-14163/?f[price][max]=1490&f[price][min]=100&page=1&gclid=CjwKCAjw55-HBhAHEiwARMCszju6ufkQ8FbPDLdcQeRzGYERMzunUKH1k3A5KVVXkFvtWuqvL-ThARoCxboQAvD_BwE',
    ]
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

#url = 'https://www.noon.com/saudi-ar/home-and-kitchen/p-14163/?f[price][max]=1490&f[price][min]=100&page=1&gclid=CjwKCAjw55-HBhAHEiwARMCszju6ufkQ8FbPDLdcQeRzGYERMzunUKH1k3A5KVVXkFvtWuqvL-ThARoCxboQAvD_BwE'
for i in range(1, 135):
    print('Count: ', i)
    url = f'https://www.noon.com/saudi-ar/home-and-kitchen/p-14163/?limit=150&page={i}&gclid=CjwKCAjw55-HBhAHEiwARMCszju6ufkQ8FbPDLdcQeRzGYERMzunUKH1k3A5KVVXkFvtWuqvL-ThARoCxboQAvD_BwE'
    data = scrap_url_product(url, driver)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Noontesst.xlsx')

print('End scrape')
driver.quit()
