import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import re

# URL of the web page
url = "https://www.libreriaisla.com/collections/editorial-patria"

# Send GET request to fetch the web page content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all product titles (Títulos) and authors (Autores) on the page
product_titles = soup.find_all(class_="tt-title prod-thumb-title-color")

# Extract the text content of each title and author 
titles = [title.text.strip() for title in product_titles]

#Create list to extract author from each item in page
authors = []
for title in product_titles:
    newurl = "https://www.libreriaisla.com/"+title.find('a').attrs['href']

    #Get a new soup for the title
    response = requests.get(newurl)
    newsoup=BeautifulSoup(response.content, "html.parser")

    #Find author in new soup
    full_description = newsoup.find(attrs={'itemprop':"description"})
    author_name = ''
    if full_description:
        # author_elems = full_description(text=re.compile(r'Autor'))
        # if len(author_elems) > 0:
        #     author_name = author_elems[0].parent.findNext().attrs['title']
        try:
            author_elems = full_description(text=re.compile(r'^Editorial$'))
            author_name = author_elems[0].parent.find_previous_sibling('a').attrs['title']
        except:
            print('Error finding author for: {}'.format(newurl))
    authors.append(author_name)



# Create a dataframe using the extracted data
data = {
    "Title": titles,
    "Authors": authors
}
df = pd.DataFrame(data)

# Data Cleaning

# Remove leading/trailing whitespaces
df['Title'] = df['Title'].str.strip()

# Remove duplicates
df = df.drop_duplicates()

# Remove empty rows
df = df.dropna()

# # 4. Convert data types if needed
# # Example: Convert 'Author' column to string
# df['Author'] = df['Author'].astype(str)

# Convert the dataframe to a table format
table = tabulate(df, headers="keys", tablefmt="grid")

# Print the table
print(table)
