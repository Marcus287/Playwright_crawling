from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")

    products = []

    product_elements = soup.select('li.product')
    for product in product_elements:
        try:
            product_data = {
                'name' : product.find('h3').get_text(strip = True),
                'url': product.find_all('a', href=True)[1]['href'] if len(product.find_all('a')) > 1 else "Cannot Find product source links or maybe in index 0",
                'img' : product.select_one('img')['src'] if product.select_one('img') else "Cannot Parse Image"
                # Access each page
            }
            products.append(product_data)

        except Exception as e:
            logger.error(f"Crawling Data error with {e}")
            product_data = {
                'name':None,
                'img':None,
                'mode':"Crawling Error"
            }
            continue

    
    return products

def parse_product_details(html):
    return

def has_next_page(html):
    #CHeck if next paga avaiblilrt
    soup=BeautifulSoup(html, "html.parser")
    #next_button = soup.select_one('a.next.page_numbers')
    next_button = soup.select_one('nav.woocommerce-pagination')
    return next_button is not None