from playwright.async_api import async_playwright
import product_parser, utils
import pandas as pd 
import time
import logging
import json
import asyncio

CONFIG = json.load(open("config.json","r"))
FILENAME = "Fienza_TONO_20250730.csv"

class FienzaCrawler:
    def __init__(self):
        self.all_products = []
        self.logger = self.setup_logger()

    def setup_logger(self):
        #Logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger

    async def crawl_page(self, page, url):
        #Checking for next page after crawled 1 page
        self.logger.info(f"Crawling: {url}")
        await page.goto(url, timeout=CONFIG["TIMEOUT"])
        #Wait for the page to load
        await page.wait_for_selector('li', timeout=CONFIG["TIMEOUT"])

        #Get html content
        html = await page.content()
        products = product_parser.parse_products(html)
        self.all_products.extend(products)

        #If page has new page returns True vice versa
        return product_parser.has_next_page(html)

    async def crawl_site(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=CONFIG["HEADLESS"])
            context = await browser.new_context()
            page = await context.new_page()

            #Intercept all requests for faster crawling
            page.route("**/*", lambda route: (
                route.abort() if route.request.resource_type in ["image", "stylesheet", "font"] else route.continue_()
            ))

            has_more = True
            current_page=1

            while has_more and current_page <10:
                url = await utils.get_page_url(current_page)
                has_more = await self.crawl_page(page, url)
                current_page += 1 
            await browser.close()

            #Save to csv files
            if self.all_products:
                await utils.save_to_csv(self.all_products, FILENAME)
                print(f"Saved {len(self.all_products)} product to CSV file")
            else:
                print("No product found")

            return self.all_products
#Handler function
async def main():
    crawler = FienzaCrawler()
    await crawler.crawl_site()

if __name__ == "__main__":
    asyncio.run(main())

