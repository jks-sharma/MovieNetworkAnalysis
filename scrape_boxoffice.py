import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_boxoffice(): 
    # URL of the Box Office Mojo page for worldwide top lifetime gross
    url = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW"

    # Sending a request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding the table that contains the movie data
    table = soup.find('table')

    # Extracting the header row and data rows
    headers = [header.text for header in table.find_all('th')]
    rows = table.find_all('tr')[1:]  # Skipping the header row

    # Extracting movie titles, total gross, and release years
    data = []
    for row in rows:
        cols = row.find_all('td')
        title = cols[1].text.strip()
        print(title)
        total_gross = cols[2].text.strip()  # Assuming the 6th column is the total gross
        year_text = cols[7].text.strip()  # Assuming the 3rd column is the release date
        print(year_text)
        # Extracting the year using regex
        year_match = re.search(r'\d{4}', year_text)
        if year_match:
            year = int(year_match.group())
            data.append([title, total_gross, year])

    # Filtering movies released from 2013 to 2023
    filtered_data = [entry for entry in data if 2013 <= entry[2] <= 2023]

    # Sorting the data by total gross (assuming it needs to be converted to int for sorting)
    filtered_data.sort(key=lambda x: int(x[1].replace(',', '').replace('$', '')), reverse=True)

    # Limiting to top 100
    top_100 = filtered_data[:101]

    # print top_100 to a csv file
    df = pd.DataFrame(top_100, columns=['Title', 'Total Gross', 'Year']) 
    df.to_csv('top_100_movies.csv', index=False)

scrape_boxoffice()