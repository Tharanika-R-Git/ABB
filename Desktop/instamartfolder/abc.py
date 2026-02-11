import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://books.toscrape.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")

data = []

for book in books:
    name = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    rating = book.p["class"][1]

    data.append([name, price, rating])

df = pd.DataFrame(data, columns=["Book Name", "Price", "Rating"])

print(df)

df.to_csv("books.csv", index=False)
