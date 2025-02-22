import requests
import pandas as pd
from bs4 import BeautifulSoup


base_site = "https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population"
r = requests.get(base_site)
soup = BeautifulSoup(r.content, 'lxml')

table1 = soup.find("table", class_="sortable wikitable sticky-header static-row-numbers col1left col4left")
table2 = soup.find("table", class_="sortable wikitable sticky-header col2left col5left")

rows = table1.find_all("tr") + table2.find_all("tr")

data = []
for row in rows[1:]:
    cols = row.find_all("td")
    data.append([col.text.strip() for col in cols])

sl_no, city, state = [], [], []
i = 1
for _row in data:
    if len(_row) >= 5:
        sl_no.append(i)
        if i >= 47:
            city.append(_row[1])
            state.append(_row[4])
        elif i <= 45:
            city.append(_row[0])
            state.append(_row[3])
        i += 1

min_length = min(len(sl_no), len(city), len(state))
sl_no, city, state = sl_no[:min_length], city[:min_length], state[:min_length]

movies_info = pd.DataFrame({"Sl no.": sl_no, "City": city, "State": state})

movies_info.to_csv("city_info.csv", index=False, header=True)

print("Scraping completed successfully!")
