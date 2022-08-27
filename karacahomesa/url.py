
import time
import os
import requests
import re, logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from random import randint
import pandas as pd
import numpy as np

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)



list_urls = [
    {'cat1': 'مفارش', 'cat2': 'مفارش مواليد', 'cat3': 'بطانيات مواليد', 'url': 'https://karacahomesa.com/category/yyPXP'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مواليد', 'cat3': 'مفارش مواليد', 'url': 'https://karacahomesa.com/category/lzmEa'},
    {'cat1': 'مفارش', 'cat2': 'مفارش أطفال', 'cat3': '', 'url': 'https://karacahomesa.com/category/DYmNj'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مفرد', 'cat3': '', 'url': 'https://karacahomesa.com/category/xWgqa'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مزدوج', 'cat3': 'مفارش مزدوج كوين', 'url': 'https://karacahomesa.com/category/rXPZy'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مزدوج', 'cat3': 'مفارش مزدوج كينج', 'url': 'https://karacahomesa.com/category/KvQzq'},
    {'cat1': 'مفارش', 'cat2': 'مفارش مزدوج', 'cat3': 'مفارش مزدوج سوبر كينج', 'url': 'https://karacahomesa.com/category/aRYZn'},
    {'cat1': 'مفارش', 'cat2': 'مفارش عرائس', 'cat3': '', 'url': 'https://karacahomesa.com/category/AxOwe'},
    {'cat1': 'مفارش', 'cat2': 'بطانيات ولحافات', 'cat3': 'لحافات خفيفة', 'url': 'https://karacahomesa.com/category/eorKO'},
    {'cat1': 'مفارش', 'cat2': 'بطانيات ولحافات', 'cat3': 'لحافات قطنية', 'url': 'https://karacahomesa.com/category/Xobrw'},
    {'cat1': 'مفارش', 'cat2': 'بطانيات ولحافات', 'cat3': 'بطانيات شتوية', 'url': 'https://karacahomesa.com/category/qNgWN'},
    {'cat1': 'مفارش', 'cat2': 'بطانيات ولحافات', 'cat3': 'أطقم لحافات', 'url': 'https://karacahomesa.com/category/zXzaG'},
    {'cat1': 'مفارش', 'cat2': 'إكسسوارات السرير', 'cat3': 'مخدات', 'url': 'https://karacahomesa.com/category/xNqzY'},
    {'cat1': 'مفارش', 'cat2': 'إكسسوارات السرير', 'cat3': 'شراشف', 'url': 'https://karacahomesa.com/category/aoXgZ'},
    {'cat1': 'مفارش', 'cat2': 'إكسسوارات السرير', 'cat3': 'حشوات لحافات', 'url': 'https://karacahomesa.com/category/bGzXX'},
    {'cat1': 'مفارش', 'cat2': 'إكسسوارات السرير', 'cat3': 'لبادات و واقيات مراتب', 'url': 'https://karacahomesa.com/category/OeABw'},
    #
    {'cat1': 'الحمام', 'cat2': 'مناشف استحمام', 'cat3': '', 'url': 'https://karacahomesa.com/category/evbry'},
    {'cat1': 'الحمام', 'cat2': 'أطقم مناشف', 'cat3': '', 'url': 'https://karacahomesa.com/category/vwxWl'},
    {'cat1': 'الحمام', 'cat2': 'مناشف يد', 'cat3': '', 'url': 'https://karacahomesa.com/category/XPDeb'},
    {'cat1': 'الحمام', 'cat2': 'أرواب استحمام', 'cat3': 'أرواب استحمام أطفال', 'url': 'https://karacahomesa.com/category/ReDEy'},
    {'cat1': 'الحمام', 'cat2': 'أرواب استحمام', 'cat3': 'أرواب استحمام مفرد', 'url': 'https://karacahomesa.com/category/nNQRe'},
    {'cat1': 'الحمام', 'cat2': 'أرواب استحمام', 'cat3': 'أطقم أرواب استحمام', 'url': 'https://karacahomesa.com/category/WogRR'},
    {'cat1': 'الحمام', 'cat2': 'دعاسات حمام', 'cat3': '', 'url': 'https://karacahomesa.com/category/pnwQK'},
    {'cat1': 'الحمام', 'cat2': 'إكسسوارات مغسلة', 'cat3': '', 'url': 'https://karacahomesa.com/category/zZGvo'},
    {'cat1': 'الحمام', 'cat2': 'إكسسوارات البانيو', 'cat3': '', 'url': 'https://karacahomesa.com/category/RXXEV'},
    {'cat1': 'الحمام', 'cat2': 'ستائر حمام', 'cat3': '', 'url': 'https://karacahomesa.com/category/oPblO'},
    {'cat1': 'الحمام', 'cat2': 'صابون وجل استحمام', 'cat3': '', 'url': 'https://karacahomesa.com/category/gOnaN'},
    {'cat1': 'الحمام', 'cat2': 'العناية بالجسم', 'cat3': '', 'url': 'https://karacahomesa.com/category/jqbOe'},
    #
    {'cat1': 'المائدة', 'cat2': 'مفارش سفرة', 'cat3': '', 'url': 'https://karacahomesa.com/category/joDZY'},
    {'cat1': 'المائدة', 'cat2': 'صحون وأطقم', 'cat3': '', 'url': 'https://karacahomesa.com/category/eXaeY'},
    {'cat1': 'المائدة', 'cat2': 'آلات ومحضرات الطعام', 'cat3': '', 'url': 'https://karacahomesa.com/category/Oqzydg'},
    {'cat1': 'المائدة', 'cat2': 'أواني طبخ', 'cat3': '', 'url': 'https://karacahomesa.com/category/QjZYY'},
    {'cat1': 'المائدة', 'cat2': 'قوالب كيك', 'cat3': '', 'url': 'https://karacahomesa.com/category/QdNqlz'},
    {'cat1': 'المائدة', 'cat2': 'ملاعق فاخرة', 'cat3': '', 'url': 'https://karacahomesa.com/category/XKZvO'},
    {'cat1': 'المائدة', 'cat2': 'إكسسوارات المطبخ', 'cat3': '', 'url': 'https://karacahomesa.com/category/Dljlw'},
    {'cat1': 'المائدة', 'cat2': 'أكواب وفناجيل', 'cat3': '', 'url': 'https://karacahomesa.com/category/AapEA'},
    {'cat1': 'المائدة', 'cat2': 'كاسات وإستكانات', 'cat3': '', 'url': 'https://karacahomesa.com/category/bWARn'},
    {'cat1': 'المائدة', 'cat2': 'أباريق الشاي', 'cat3': '', 'url': 'https://karacahomesa.com/category/GVBBW'},
    {'cat1': 'المائدة', 'cat2': 'مستلزمات الضيافة', 'cat3': '', 'url': 'https://karacahomesa.com/category/ZoZQl'},
    {'cat1': 'المائدة', 'cat2': 'شمعدانات وفوانيس', 'cat3': '', 'url': 'https://karacahomesa.com/category/Bqmry'},
    {'cat1': 'المائدة', 'cat2': 'أطباق فاخرة للزينة', 'cat3': '', 'url': 'https://karacahomesa.com/category/rxdAX'},
    {'cat1': 'المائدة', 'cat2': 'أواني زجاجية للزينة', 'cat3': '', 'url': 'https://karacahomesa.com/category/wXbWN'},
    {'cat1': 'المائدة', 'cat2': 'أواني خزفية للزينة', 'cat3': '', 'url': 'https://karacahomesa.com/category/RldXP'},
    {'cat1': 'المائدة', 'cat2': 'سلات دانتيل', 'cat3': '', 'url': 'https://karacahomesa.com/category/XEYyz'},
    #
    {'cat1': 'المنزل', 'cat2': 'فازات ومزهريات', 'cat3': '', 'url': 'https://karacahomesa.com/category/vYOXE'},
    {'cat1': 'المنزل', 'cat2': 'تحفيات وتماثيل', 'cat3': '', 'url': 'https://karacahomesa.com/category/KbrjE'},
    {'cat1': 'المنزل', 'cat2': 'نباتات وأزهار', 'cat3': '', 'url': 'https://karacahomesa.com/category/arveO'},
    {'cat1': 'المنزل', 'cat2': 'آنية نباتات وأزهار', 'cat3': '', 'url': 'https://karacahomesa.com/category/nEyRee'},
    {'cat1': 'المنزل', 'cat2': 'مخدات ديكور', 'cat3': '', 'url': 'https://karacahomesa.com/category/ODvqz'},
    {'cat1': 'المنزل', 'cat2': 'خزائن وصناديق الألعاب', 'cat3': '', 'url': 'https://karacahomesa.com/category/Pdemng'},
    {'cat1': 'المنزل', 'cat2': 'لوحات جدارية', 'cat3': '', 'url': 'https://karacahomesa.com/category/EZbGdA'},
    {'cat1': 'المنزل', 'cat2': 'إطارات صور', 'cat3': '', 'url': 'https://karacahomesa.com/category/PlAqO'},
    {'cat1': 'المنزل', 'cat2': 'أبجورات وإضاءة', 'cat3': '', 'url': 'https://karacahomesa.com/category/gVqPV'},
    {'cat1': 'المنزل', 'cat2': 'قطع سجاد', 'cat3': '', 'url': 'https://karacahomesa.com/category/bXwZX'},
    {'cat1': 'المنزل', 'cat2': 'ساعات فاخرة', 'cat3': '', 'url': 'https://karacahomesa.com/category/DXQKg'},
    {'cat1': 'المنزل', 'cat2': 'تلبيسات كنب', 'cat3': '', 'url': 'https://karacahomesa.com/category/ZXgzQ'},
    #
    {'cat1': 'معطرات', 'cat2': 'معطرات مفارش', 'cat3': '', 'url': 'https://karacahomesa.com/category/POGZe'},
    {'cat1': 'معطرات', 'cat2': 'معطرات ملابس', 'cat3': '', 'url': 'https://karacahomesa.com/category/xWgAa'},
    {'cat1': 'معطرات', 'cat2': 'معطرات سيارات', 'cat3': '', 'url': 'https://karacahomesa.com/category/nEprGn'},
    {'cat1': 'معطرات', 'cat2': 'العود والبخور', 'cat3': '', 'url': 'https://karacahomesa.com/category/EZaZYQ'},
    {'cat1': 'معطرات', 'cat2': 'شموع معطرة', 'cat3': '', 'url': 'https://karacahomesa.com/category/KzBwE'},
    {'cat1': 'معطرات', 'cat2': 'عطور أعواد البامبو', 'cat3': '', 'url': 'https://karacahomesa.com/category/wdAyz'},
    {'cat1': 'معطرات', 'cat2': 'عطور زيتية للفواحات', 'cat3': 'كولكشن العطور 10 مل', 'url': 'https://karacahomesa.com/category/BDaAl'},
    {'cat1': 'معطرات', 'cat2': 'عطور زيتية للفواحات', 'cat3': 'عطور زيتية منزلية 100 مل', 'url': 'https://karacahomesa.com/category/rVWqp'},
    {'cat1': 'معطرات', 'cat2': 'عطور زيتية للفواحات', 'cat3': 'عطور زيتية منزلية 500 مل', 'url': 'https://karacahomesa.com/category/wVewR'},
    {'cat1': 'معطرات', 'cat2': 'فواحات إلكترونية', 'cat3': '', 'url': 'https://karacahomesa.com/category/DwAed'},
    #
    {'cat1': 'المواليد', 'cat2': 'العناية بالمواليد', 'cat3': '', 'url': 'https://karacahomesa.com/category/WPbAq'},
    {'cat1': 'المواليد', 'cat2': 'ملابس حديثي الولادة', 'cat3': '', 'url': 'https://karacahomesa.com/category/Qladr'},
    {'cat1': 'المواليد', 'cat2': 'إكسسوارات المواليد', 'cat3': '', 'url': 'https://karacahomesa.com/category/Oavyw'},
    {'cat1': 'المواليد', 'cat2': 'سجادة المواليد', 'cat3': '', 'url': 'https://karacahomesa.com/category/qaaox'},
    {'cat1': 'المواليد', 'cat2': 'سراير المواليد', 'cat3': '', 'url': 'https://karacahomesa.com/category/XWqQd'},
    {'cat1': 'المواليد', 'cat2': 'سراير المواليد - حجم كبير', 'cat3': '', 'url': 'https://karacahomesa.com/category/DoamV'},
    #
    {'cat1': 'مستلزمات', 'cat2': 'العناية بكبار السن', 'cat3': '', 'url': 'https://karacahomesa.com/category/qQxdWn'},
    {'cat1': 'مستلزمات', 'cat2': 'العناية بالأشخاص ذوي الإعاقة', 'cat3': '', 'url': 'https://karacahomesa.com/category/ePGXKR'},
    #
    {'cat1': 'أثاث', 'cat2': 'كنب وجلسات', 'cat3': '', 'url': 'https://karacahomesa.com/category/DvQdV'},
    {'cat1': 'أثاث', 'cat2': 'كراسي مكتب', 'cat3': '', 'url': 'https://karacahomesa.com/category/zvwEDd'},
    {'cat1': 'أثاث', 'cat2': 'أرجوحات استرخاء', 'cat3': '', 'url': 'https://karacahomesa.com/category/qRzVY'},
    {'cat1': 'أثاث', 'cat2': 'رفوف وفواصل', 'cat3': '', 'url': 'https://karacahomesa.com/category/vBnbl'},
    {'cat1': 'أثاث', 'cat2': 'علاقات ملابس', 'cat3': '', 'url': 'https://karacahomesa.com/category/WlXdyR'},
    {'cat1': 'أثاث', 'cat2': 'طاولات تقديم', 'cat3': '', 'url': 'https://karacahomesa.com/category/xnprG'},
    {'cat1': 'أثاث', 'cat2': 'طاولات قهوة', 'cat3': '', 'url': 'https://karacahomesa.com/category/BymPr'},
    {'cat1': 'أثاث', 'cat2': 'طاولات تلفزيون', 'cat3': '', 'url': 'https://karacahomesa.com/category/XOaEb'},
    {'cat1': 'أثاث', 'cat2': 'أثاث الأطفال', 'cat3': '', 'url': 'https://karacahomesa.com/category/qQxmVY'},
    {'cat1': 'أثاث', 'cat2': 'طاولات وكراسي الأطفال', 'cat3': '', 'url': 'https://karacahomesa.com/category/ZYXrvb'},
    {'cat1': 'أثاث', 'cat2': 'خزائن أحذية', 'cat3': '', 'url': 'https://karacahomesa.com/category/QrBGY'},
    # {'cat1': '', 'cat2': '', 'cat3': '', 'url': ''},
]


def get_data(url, driver, count):
    logging.info('URL: %s', url)
    url = url + f'?page={count}'
    driver.get(url)
    body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    r = body.get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    time.sleep(1)
    products = soup.find_all('div', {'class': 'product'})
    liens = [toto.find('a')['href']  for toto in products]
    logging.info('Len products %s', len(liens))
    return liens

def scrap_url_product(url1):
    cat1 = url1['cat1']
    cat2 = url1['cat2']
    cat3 = url1['cat3']
    url = url1['url']
    data = []
    count = 1
    while True:
        urls_list = get_data(url, driver, count)
        if len(urls_list) == 0:
            break
        for toto in urls_list:
            data.append({
            'url':toto,
            'cat1': cat1,
            'cat2': cat2,
            'cat3': cat3,
            })

        count += 1
        url = url.split('?')[0]
    logging.info( 'Scrape Categorie Done --> Next .')
    return data
df = pd.read_excel('karacahomesa_url_model.xlsx')   
for i, url in enumerate(list_urls):
    logging.info('Count: %s', i)
    data = scrap_url_product(url)
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('karacahomesa_url_update.xlsx')
logging.info('Scraping URL Done.')

