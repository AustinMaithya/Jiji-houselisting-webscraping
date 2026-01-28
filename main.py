import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://jiji.co.ke"
LISTINGS_URL = "https://jiji.co.ke/houses-apartments-for-sale?query=houses"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# -------------------------------
# 1. Get listings page
# -------------------------------
response = requests.get(LISTINGS_URL, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

listings = soup.find_all("div", class_="masonry-item")
print(f"Found {len(listings)} listings")

# -------------------------------
# 2. Collect house links
# -------------------------------
house_links = []

for listing in listings:
    a_tag = listing.find("a", href=True)
    if a_tag:
        house_links.append(BASE_URL + a_tag["href"])

print(f"Collected {len(house_links)} house URLs")

# -------------------------------
# 3. Visit each house page
# -------------------------------
data = []

for house_url in house_links:
    r = requests.get(house_url, headers=headers)
    house_soup = BeautifulSoup(r.content, "lxml")

    # Price
    price_tag = house_soup.find("span", class_="qa-advert-price-view-value")
    price = price_tag.text.strip() if price_tag else "N/A"

    # Attributes (location, size, etc.)
    attributes = house_soup.find_all("div", class_="b-advert-title-inner qa-advert-title b-advert-title-inner--h1")

    description = attributes[0].text.strip() if len(attributes) > 0 else "N/A"
    

    data.append({
        "description": description,
        "Price": price,
        "URL": house_url
    })

    print(f"Description: {description}, Price: {price}")

# -------------------------------
# 4. Save to DataFrame
# -------------------------------
df = pd.DataFrame(data)
print(df.head())
df.to_csv("houses_for_sale.csv", index=False)