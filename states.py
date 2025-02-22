import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

def parse_html(html):
    return BeautifulSoup(html, 'lxml')

def extract_table_data(soup):
    table = soup.find("table", class_="wikitable sortable plainrowheaders")
    if not table:
        raise Exception("Target table not found!")
    
    rows = table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]
    
    data = []
    for row in rows[1:]:
        cols = row.find_all(["th", "td"])
        data.append([col.text.strip() for col in cols])
    
    return headers, data

def process_data(data):
    sl_no, state, vehiclecode, capital, statehood, population, official_languages = [], [], [], [], [], [], []
    
    for index, row in enumerate(data, start=1):
        if row:
            sl_no.append(index)
            state.append(row[0])
            vehiclecode.append(row[2])
            
            if len(row) > 10:
                capital.append(row[4])
                statehood.append(row[6])
                population.append(row[7])
                official_languages.append(row[9])
            else:
                capital.append(row[3])
                statehood.append(row[5])
                population.append(row[6])
                official_languages.append(row[8])
    
    return sl_no, state, vehiclecode, capital, statehood, population, official_languages

def save_to_csv(filename, sl_no, state, vehiclecode, capital, statehood, population, official_languages):
    df = pd.DataFrame({
        "Sl No.": sl_no,
        "State": state,
        "Vehicle Code": vehiclecode,
        "Capital": capital,
        "Statehood": statehood,
        "Population": population,
        "Official Languages": official_languages
    })
    df.to_csv(filename, index=False, header=True)

def main():
    url = "https://en.wikipedia.org/wiki/States_and_union_territories_of_India"
    html = fetch_html(url)
    
    soup = parse_html(html)
    headers, data = extract_table_data(soup)
    sl_no, state, vehiclecode, capital, statehood, population, official_languages = process_data(data)
    
    save_to_csv("state_info.csv", sl_no, state, vehiclecode, capital, statehood, population, official_languages)
    print("Scraping completed successfully!")

if __name__ == "__main__":
    main()
