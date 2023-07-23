import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

# Specify the URL of the website you want to scrape
url = "https://libros787.com/collections/la-impresora"

# Send a GET request to the website
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all product titles and authors on the page
product_titles = soup.find_all(class_="productitem--title")
product_authors = soup.find_all(class_="product-vendor")

# Extract the text content of each title and author
titles = [title.text.strip() for title in product_titles]
authors = [author.text.strip() for author in product_authors]

# Create a dataframe using the extracted data
data = {
    "Title": titles,
    "Author": authors
}
df = pd.DataFrame(data)

# Data Cleaning Tasks

# 1. Remove leading/trailing whitespaces
df['Title'] = df['Title'].str.strip()
df['Author'] = df['Author'].str.strip()

# 2. Remove duplicates
df = df.drop_duplicates()

# 3. Remove empty rows
df = df.dropna()

# 4. Convert data types if needed
# Example: Convert 'Author' column to string
df['Author'] = df['Author'].astype(str)

# Convert the dataframe to a table format
table = tabulate(df, headers="keys", tablefmt="grid")

# Print the table
print(table)
