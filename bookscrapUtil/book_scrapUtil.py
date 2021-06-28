from selenium.common.exceptions import NoSuchElementException
import re
# A função recebe uma instancia do webdriver do navegador e retorna uma
# lista dos links dos livros em uma página html.
def extract_book_urls(driver):
    a_list = driver.find_elements_by_xpath('//div[@class="image_container"]/a')
    urls = [a.get_attribute('href') for a in a_list]
    dedup_urls = list(set(urls))
    return dedup_urls

# A função recebe uma instancia do webdriver do navegador e retorna o link para a próxima página
def go_next_page(driver):
    try:
        button = driver.find_element_by_xpath('//li[@class="next"]/a')
        return True, button
    except NoSuchElementException:
        return False, None

# Retorna o número de estrelas do livro de acordo com o primeiro nome da classe css
# do paragráfo que contém essa informação.
def star_rating(p):
    if p['class'][1] == 'One':
        return 1
    elif p['class'][1] == 'Two':
        return 2
    elif p['class'][1] == 'Three':
        return 3
    elif p['class'][1] == 'Four':
        return 4
    elif p['class'][1] == 'Five':
        return 5
    else:
        return 0

# Retorna True se o icone indicando que o livro está em estoque está presente
# e False se não.   
def InStock(div):
    if div.find_all('i', class_ = 'icon-ok'):
        return True
    else:
        return False

# Retorna as informações do livro
def book_extract(div):
    name = div.find('h1').string
    stars = div.find_all('p', class_=re.compile("star-rating"))
    stars = star_rating(stars[0])
    price = div.find_all('p', class_ = 'price_color')
    price = float(price[0].string.replace('£', ''))
    In_stock = InStock(div)
    
    return {
        "Name": name,
        "Stars": stars,
        "Price": price,
        "In Stock": In_stock
    }