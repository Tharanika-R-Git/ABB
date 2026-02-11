from playwright.sync_api import sync_playwright
import pandas as pd
import time

brands = [
    "https://www.myntra.com/levis",
    "https://www.myntra.com/puma",
    "https://www.myntra.com/nike",
    "https://www.myntra.com/adidas",
    "https://www.myntra.com/hrx"
]

all_products = []

def scroll_page(page):
    """Scroll to load lazy products"""
    last_height = 0
    
    while True:
        page.mouse.wheel(0, 5000)
        time.sleep(2)

        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for brand_url in brands:
        print("Scraping:", brand_url)

        page.goto(brand_url)
        time.sleep(5)

        # Scroll to load products
        scroll_page(page)

        # Select product cards
        products = page.query_selector_all("li.product-base")

        count = 0

        for product in products:
            if count >= 30:
                break

            try:
                name = product.query_selector("h3.product-brand").inner_text()
                title = product.query_selector("h4.product-product").inner_text()
                price = product.query_selector("div.product-price").inner_text()

                link = product.query_selector("a").get_attribute("href")
                link = "https://www.myntra.com" + link

                all_products.append({
                    "Brand": name,
                    "Title": title,
                    "Price": price,
                    "Product Link": link,
                    "Source Brand Page": brand_url
                })

                count += 1

            except:
                continue

    browser.close()

df = pd.DataFrame(all_products)
df.to_csv("myntra_brand_products.csv", index=False)

print("Scraping Completed!")
