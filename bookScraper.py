from bs4 import BeautifulSoup
import requests
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from tqdm import tqdm

import book_scrapUtil 

base_url = "http://books.toscrape.com/"


def get_soup(url):
    return BeautifulSoup(requests.get(url).content, 'lxml')

# Extrai os urls de cada categoria dos livros
data_url = {}

soup = get_soup(base_url)
category_list_level0 = soup.find('ul', {'class': 'nav nav-list'})
category_list_level1 = category_list_level0.find('ul')

for category in category_list_level1.find_all('li'):
    name = category.find('a').text
    name = name.strip()
    data_url[name] = {} 
    url = category.find('a')['href']
    data_url[name] = url

# Configuração do chromedriver
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)

timeout = 3

# Extração das urls de cada um dos livros
book_urls = {}
for category in tqdm(data_url):
    
        book_urls[category] = []

        url = base_url + data_url[category]
        driver.get(url)
        try: 
            element_present = EC.presence_of_element_located(
                (By.CLASS_NAME, 'col-sm-8 col-md-9'))
            
            WebDriverWait(driver, timeout).until(element_present)
        except:
            pass
    
        next_page = True
        c = 1
        while next_page:
            extracted_book_urls = book_scrapUtil.extract_book_urls(driver)
            book_urls[category] += extracted_book_urls
            next_page, button = book_scrapUtil.go_next_page(driver)
            
            if next_page:
                c += 1
                next_url = base_url + data_url[category] + f'&page-{c}'
                driver.get(next_url)
                try: 
                    element_present = EC.presence_of_element_located(
                        (By.CLASS_NAME, 'col-sm-8 col-md-9'))
                    
                    WebDriverWait(driver, timeout).until(element_present)
                except:
                    pass

# Prepara as urls para extração dos dados dos livros
consolidated_data = []

for category in data_url:
    
    for url in book_urls[category]:
        consolidated_data.append((category, url))

df_consolidated_data = pd.DataFrame(consolidated_data, columns=['category', 'book_url'])

# Extração dos dados dos livros
start_urls = df_consolidated_data['book_url'].unique().tolist()
data = []
for url in tqdm(start_urls):
    soup = get_soup(url)
    for div in soup.find_all('div', class_ = 'col-sm-6 product_main'):
        data.append(book_scrapUtil.book_extract(div))

# Salva os dados em formato CSV
df_books = pd.DataFrame.from_records(data)
df_dataFinal = pd.concat([df_consolidated_data['category'], df_books], axis=1)
df_dataFinal.to_csv('./consolidate_book_data.csv', index=False)