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
import time, re, logging
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#opti#     driver = webdriver.Firefox()ons.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)


def get_data(url):
    logging.info(f'Url: {url}')
    driver.get(url)
    body=WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.category-category_page_container-24J')))
    r = body.get_attribute('innerHTML')
    soup = BeautifulSoup(r, "html.parser")
    products = soup.find_all('a', {'class': 'item-images-1xN'})
    
    liens = ['https://www.almutlaqfurniture.com' + toto['href']  for toto in products]
    logging.info(f'Len products {len(liens)}')
    list_liens = []
    for t in liens:
        list_liens.append(t)
    return list_liens


def getnextpage():
    # if next url exist
    try:
        next_p = driver.find_element_by_xpath('//button[@aria-label="move to the next page"]')
    
        net_page = next_p.get_attribute('disabled')
        if net_page == 'true':
            return ''
        next_p.click()
        return str(driver.current_url)
    except:
        pass
        # logging.info('', url2)

    


# Extract new urls of Rugaib site from url categories

# url = 'https://rawae.com/search?subsubcategory=Accessories-box-Q3HaJ&page=1'
list_urls = []


def scrap_url_product(url):
    data = []
    cat1 = url['cat1']
    cat2 = url['cat2']
    cat3 = url['cat3']
    url1 = url['url']
    while True:
        urls_list = get_data(str(url1))

        time.sleep(1)
        for toto in urls_list:

            # logging.info(f'URL:', toto)
            data.append({
            'url':toto, 'categories1':cat1, 'categories2': cat2,'categories2': cat3
            })

        
        url1 = getnextpage()
        if url1 == '' or url1 == None:
            logging.info('Next page..')
            break
    # logging.info(data)
    logging.info( f'Scrape done .')
    return data

urls = [
    
    {'cat1': 'غرف النوم', 'cat2': 'أسِرَّة', 'cat3': 'سرير كينج', 'url':'https://www.almutlaqfurniture.com/bedroom/beds/king-doubled-bed.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'أسِرَّة', 'cat3': 'سرير فردي', 'url':'https://www.almutlaqfurniture.com/bedroom/beds/single-bed.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'دواليب الملابس', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/bedroom/wardrobe.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'المراتب', 'cat3': 'مراتب فردي', 'url':'https://www.almutlaqfurniture.com/bedroom/mattress/single-matteress.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'المراتب', 'cat3': 'مراتب كوين', 'url':'https://www.almutlaqfurniture.com/bedroom/mattress/queen-matteress.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'المراتب', 'cat3': 'مراتب كينج-مزدوج', 'url':'https://www.almutlaqfurniture.com/bedroom/mattress/king-matteress.html'},
    {'cat1': 'غرف النوم', 'cat2': 'خزائن ذات أدراج', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/bedroom/chest-of-drawers.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'طاولات الزينة والمرايا', 'cat3': 'طاولات الزينة', 'url':'https://www.almutlaqfurniture.com/bedroom/dressers-mirrors/dressing-table.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'طاولات الزينة والمرايا', 'cat3': 'مرايا', 'url':'https://www.almutlaqfurniture.com/bedroom/dressers-mirrors/dressing-mirror.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'طاولات جانبية للسرير', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/bedroom/night-stand.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'مستلزمات غرف النوم', 'cat3': 'ألواح و قواعد للسرير', 'url':'https://www.almutlaqfurniture.com/bedroom/bedroom-essentials/bed-slats.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'مستلزمات غرف النوم', 'cat3': 'أدراج للسرير', 'url':'https://www.almutlaqfurniture.com/bedroom/bedroom-essentials/bed-drawers.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'مستلزمات غرف النوم', 'cat3': 'وحدات حائط', 'url':'https://www.almutlaqfurniture.com/bedroom/bedroom-essentials/wall-unit.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'مفروشات السرير', 'cat3': 'وسائد', 'url':'https://www.almutlaqfurniture.com/bedroom/bedding/cushions.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'مفروشات السرير', 'cat3': 'مفارش السرير', 'url':'https://www.almutlaqfurniture.com/bedroom/bedding/bed-covers.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'غرف نوم كاملة', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/bedroom/bedroom-sets.html?page=1'},
    {'cat1': 'غرف النوم', 'cat2': 'غرف أطفال كاملة', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/bedroom/kids-room-sets.html?page=1'},
    
    {'cat1': 'غرف السفرة', 'cat2': 'طاولات السفرة', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/dining/dining-table.html?page=1'},
    {'cat1': 'غرف السفرة', 'cat2': 'كراسي السفرة', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/dining/dining-chair.html?page=1'},
    {'cat1': 'غرف السفرة', 'cat2': 'وحدات عرض', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/dining/display-cabinet.html?page=1'},
    {'cat1': 'غرف السفرة', 'cat2': 'بوفيهات', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/dining/buffet.html?page=1'},
    {'cat1': 'غرف السفرة', 'cat2': 'مرايا لغرفة السفرة', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/dining/dining-mirror.html?page=1'},
    {'cat1': 'غرف السفرة', 'cat2': 'أطقم السفرة', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/dining/dining-sets.html?page=1'},
    {'cat1': 'غرف السفرة', 'cat2': 'كراسي استرخاء', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/living/recliner.html?page=1'},
    
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب ومقاعد', 'cat3': 'مساند للقدمين', 'url':'https://www.almutlaqfurniture.com/living/sofas-seating/footstools.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب ومقاعد', 'cat3': 'كراسي بذراعين', 'url':'https://www.almutlaqfurniture.com/living/sofas-seating/armchair.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب ومقاعد', 'cat3': 'كنب مقعد واحد', 'url':'https://www.almutlaqfurniture.com/living/sofas-seating/01-seater-sofa.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب ومقاعد', 'cat3': 'كنب مقعدين', 'url':'https://www.almutlaqfurniture.com/living/sofas-seating/02-seater-sofa.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب ومقاعد', 'cat3': 'كنب 3 مقاعد', 'url':'https://www.almutlaqfurniture.com/living/sofas-seating/03-seater-sofa.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'كنب ومقاعد', 'cat3': 'أطقم كنب', 'url':'https://www.almutlaqfurniture.com/living/sofas-seating/sofa-sets.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'طاولات القهوة', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/living/coffee-table.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'وحدات للتلفاز', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/living/tv-unit.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'وحدات حائط', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/living/wall-unit.html?page=1'},
    {'cat1': 'غرف المعيشة', 'cat2': 'أطقم غرف المعيشة', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/living/living-sets.html?page=1'},

    {'cat1': 'اكسسوارات وديكور المنزل', 'cat2': 'أكسسوارات للمنزل', 'cat3': 'مزهريات', 'url':'https://www.almutlaqfurniture.com/decor-and-furnnishings/home-accessories/vases-bowls.html?page=1'},
    {'cat1': 'اكسسوارات وديكور المنزل', 'cat2': 'أكسسوارات للمنزل', 'cat3': 'ساعات حائط', 'url':'https://www.almutlaqfurniture.com/decor-and-furnnishings/home-accessories/clocks.html?page=1'},
    {'cat1': 'اكسسوارات وديكور المنزل', 'cat2': 'السجاد والمفروشات', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/decor-and-furnnishings/rugs-and-carpets.html?page=1'},
    {'cat1': 'اكسسوارات وديكور المنزل', 'cat2': 'الاضاءة', 'cat3': 'مصابيح معلقة', 'url':'https://www.almutlaqfurniture.com/decor-and-furnnishings/lighting/hanging-lamp.html?page=1'},
    {'cat1': 'اكسسوارات وديكور المنزل', 'cat2': 'الاضاءة', 'cat3': 'مصابيح طاولة', 'url':'https://www.almutlaqfurniture.com/decor-and-furnnishings/lighting/table-lamp.html?page=1'},
    {'cat1': 'اكسسوارات وديكور المنزل', 'cat2': 'الاضاءة', 'cat3': 'مصابيح أرضية', 'url':'https://www.almutlaqfurniture.com/decor-and-furnnishings/lighting/floor-lamp.html?page=1'},
    
    {'cat1': 'الاثاث المكتبي', 'cat2': 'خزانات الكتب', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/home-office/book-case.html?page=1'},
    {'cat1': 'الاثاث المكتبي', 'cat2': 'مكاتب', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/home-office/desk.html?page=1'},
    
    {'cat1': 'غرف كاملة', 'cat2': '', 'cat3': '', 'url':'https://www.almutlaqfurniture.com/full-rooms.html?page=1'},


    
]

df = pd.read_excel('/home/wafistos/Documents/Projects/scaping_wafi/almutlaqfurniture/Almutlaq_url_model.xlsx')
for i, url in enumerate(urls):
    logging.info(f'Count: {i}')
    try:
        data = scrap_url_product(url)
    except:
        logging.warning(f'Next in {url["url"]}')
        continue
    df1 = pd.DataFrame(data)
    df = pd.concat([df, df1], ignore_index=True)
    df.to_excel('Almut_update_url.xlsx')



