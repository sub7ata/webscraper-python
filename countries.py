import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

def parse_html(html):
    return BeautifulSoup(html, 'lxml')

def extract_table_data(soup):
    table = soup.find("table", class_="wikitable sortable sticky-header sort-under mw-datatable col2left col6left")
    if not table:
        raise Exception("Target table not found!")
    
    rows = table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]
    
    data = []
    for row in rows[2:]:
        cols = row.find_all(["th", "td"])
        data.append([col.text.strip() for col in cols])
    
    return headers, data

def process_data(data):
    sl_no, country, population, date = [], [], [], []
    
    for index, row in enumerate(data, start=1):
        if row:
            sl_no.append(index)
            if index == 2:
                country.append(row[0])
                population.append(row[1])
                date.append(row[3])
            else:
                country.append(row[1])
                population.append(row[2])
                date.append(row[4])
    
    return sl_no, country, population, date

def save_to_csv(filename, sl_no, country, population, date):
    df = pd.DataFrame({
        "Sl No.": sl_no,
        "Country": country,
        "Population": population,
        "Date": date
    })
    df.to_csv(filename, index=False, header=True)

def main():
    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    html = fetch_html(url)
    
    soup = parse_html(html)
    
    headers, data = extract_table_data(soup)
    sl_no, country, population, date = process_data(data)
    
    save_to_csv("countries_info.csv", sl_no, country, population, date)
    print("Scraping completed successfully!")

if __name__ == "__main__":
    main()
