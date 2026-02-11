from playwright.sync_api import sync_playwright
import pandas as pd
import time

# ---------------------------------
# Puma Brand URL (Stable Filter URL)
# ---------------------------------
BASE_URL = "https://www.myntra.com/shoes?f=Brand%3APuma"

all_products = []


# ---------------------------------
# Scroll Products
# ---------------------------------
def scroll_page(page):

    last_height = page.evaluate("document.body.scrollHeight")

    while True:
        page.mouse.wheel(0, 4000)
        time.sleep(2)

        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


# ---------------------------------
# Extract Products
# ---------------------------------
def scrape_products(page):

    cards = page.query_selector_all("li.product-base")

    for card in cards:
        try:
            brand = card.query_selector("h3.product-brand").inner_text()
            name = card.query_selector("h4.product-product").inner_text()

            try:
                price = card.query_selector(
                    "span.product-discountedPrice, span.product-price"
                ).inner_text()
            except:
                price = ""

            link = card.query_selector("a").get_attribute("href")
            link = "https://www.myntra.com" + link

            all_products.append({
                "Brand": brand,
                "Product Name": name,
                "Price": price,
                "Product Link": link
            })

        except:
            pass


# ---------------------------------
# MAIN SCRAPER
# ---------------------------------
with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page_number = 1

    while True:

        url = f"{BASE_URL}&p={page_number}"
        print(f"\nOpening Page {page_number}")

        page.goto(url, timeout=60000)

        # Wait for products
        try:
            page.wait_for_selector("li.product-base", timeout=10000)
        except:
            print("No more products found. Stopping...")
            break

        # Scroll page fully
        scroll_page(page)

        # Count products before scraping
        cards = page.query_selector_all("li.product-base")

        if len(cards) == 0:
            break

        print("Products Found:", len(cards))

        scrape_products(page)

        page_number += 1

    browser.close()


# ---------------------------------
# Save CSV
# ---------------------------------
df = pd.DataFrame(all_products)
df.to_csv("puma_products.csv", index=False)

print("\n✅ Scraping Completed! Data saved in puma_products.csv")
