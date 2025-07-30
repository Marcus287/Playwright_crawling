import pandas as pd
from bs4 import BeautifulSoup
import requests
from playwright.async_api import async_playwright
import asyncio
import utils 

PATH = "data/Fienza_TONO_20250730.csv"
DF = pd.read_csv(PATH)

async def product_details(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        #Intercept all requests for faster crawling
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_selector('li')
            html = await page.content()


            #response = requests.get(url)
            #soup = BeautifulSoup(response.text, 'html.parser')
            soup = BeautifulSoup(html, 'html.parser')


            price = soup.find('span', class_="woocommerce-Price-amount amount").get_text(strip=True).lstrip('$')
            sku = soup.select_one('span.sku').get_text(strip=True)
            des = soup.select_one('.post-content.woocommerce-product-details__short-description')
            h5_element = soup.select_one('h5.fusion-responsive-typography-calculated') if soup.select_one('h5.fusion-responsive-typography-calculated') else ""
            des = f"{des}\n{h5_element}"
            specs = soup.select_one('div.wpcf-field-master-page a')['href'] if soup.select_one('div.wpcf-field-master-page a') else ""
            care_guide = soup.select_one('div.wpcf-field-care-guide a')['href'] if soup.select_one('div.wpcf-field-care-guide a') else ""
            brochure = soup.select_one('div.wpcf-field-range-brochure a')['href'] if soup.select_one('div.wpcf-field-range-brochure a') else ""

            return [sku, des, price, specs, care_guide, brochure]
        except Exception as e:
            return ["", "", "", "", "", "", f"{e}"]


async def concat_df():
    columns_name = ['sku','des','price','specs','care_guide','brochure']
    urls = DF['url']
    new_columns = []
    for url in urls:
        data = await product_details(url)
        new_columns.append(data)

    new_df = pd.DataFrame(new_columns, columns=columns_name)

    await utils.save_to_csv(new_df, "TONO20250730.csv")
    

asyncio.run(concat_df())
