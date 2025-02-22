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
    table = soup.find("table", class_="wikitable sortable")
    if not table:
        raise Exception("Target table not found!")
    
    rows = table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]
    
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        data.append([col.text.strip() for col in cols])
    
    return headers, data

def process_data(data):
    sl_no, district, population, headquarters = [], [], [], []
    
    for row in data:
        if row:
            sl_no.append(row[0])
            district.append(row[2])
            population.append(row[7])
            headquarters.append(row[3])
    
    return sl_no, district, population, headquarters

def save_to_csv(filename, sl_no, district, population, headquarters):
    df = pd.DataFrame({
        "Sl No.": sl_no,
        "District": district,
        "Headquarters": headquarters,
        "Population": population
    })
    df.to_csv(filename, index=False, header=True)

def main():
    url = "https://en.wikipedia.org/wiki/List_of_districts_of_West_Bengal"
    html = fetch_html(url)
    
    soup = parse_html(html)
    headers, data = extract_table_data(soup)
    sl_no, district, population, headquarters = process_data(data)
    
    save_to_csv("districts_info.csv", sl_no, district, population, headquarters)
    print("Scraping completed successfully!")

if __name__ == "__main__":
    main()
