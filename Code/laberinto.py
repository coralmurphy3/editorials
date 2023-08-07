import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

# Specify the URL of the website you want to scrape
url = "https://librerialaberintopr.com/collections/ediciones-laberinto?page=2"

# Send a GET request to the website
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all product titles on the page
product_titles = soup.find_all(class_="h4 grid-view-item__title product-card__title")

# Extract the text content of each title and author
titles = [title.text.strip() for title in product_titles]

# Create a dataframe using the extracted data
data = {
    "Title": titles,
}
df = pd.DataFrame(data)

# Data Cleaning Tasks

# 1. Remove leading/trailing whitespaces
df['Title'] = df['Title'].str.strip()

# 2. Remove duplicates
df = df.drop_duplicates()

# 3. Remove empty rows
df = df.dropna()


# Convert the dataframe to a table format
table = tabulate(df, headers="keys", tablefmt="grid")

# Print the table
print(table)
