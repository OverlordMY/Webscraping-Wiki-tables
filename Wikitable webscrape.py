from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv


pd.set_option('display.max_columns', 5)

# Wikipedia like to List of countries by GDP

URL = r'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'

# Setting up Beautiful Soup
site = requests.get(URL).text
soup = BeautifulSoup(site, 'lxml')
all_tables = soup.find_all('table')


# Selecting the International Monetary Fund table
def International_Monetary_Fund():

    # Create global to retrieve dataframe from function
    global IMF

    left_tables = soup.find('table', class_='wikitable sortable')

    # Lists to append the data. There are 3 columns in the table
    A = []
    B = []
    C = []

    # Retrieving the Countries requires different method since they are links.
    for row in left_tables.find_all('tr'):
        names = row.find('a', href=True)
        if names:
            title = names.get('title')
            B.append(title)

    # Parsing data and adding to lists above
    for row in left_tables.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 3:
            A.append(cells[0].find(text=True))
            C.append(cells[2].find(text=True))

    # Placing lists into a dataframe
    IMF = pd.DataFrame(A, columns=['Rank'])
    IMF['Country'] = B
    IMF['GDP'] = C

    # Removing 'next line' from Series
    IMF['GDP'] = IMF['GDP'].replace(r'\n', '', regex=True)
    return IMF


def World_Bank():

    # Create global to retrieve dataframe from function
    global WB

    mid_table = soup.find_all('table')[7]

    # Lists to append the data. There are 3 columns in the table
    D = []
    E = []
    F = []

    # Retrieving the Countries requires different method since they are links.
    for row in mid_table.find_all('tr'):
        names = row.find('a', href=True)
        if names:
            title = names.get('title')
            E.append(title)

    # Parsing data and adding to lists above
    for row in mid_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 3:
            D.append(cells[0].find(text=True))
            F.append(cells[2].find(text=True))

    # Placing lists into a dataframe
    WB = pd.DataFrame(E, columns=['Country'])
    WB['Rank'] = D
    WB['GDP'] = F

    # Removing 'next line' from Series
    WB['GDP'] = WB['GDP'].str.replace(r'\n', '')
    return WB

def United_Nations():

    # Create global to retrieve dataframe from function
    global UN

    right_table = soup.find_all('table')[9]

    # Lists to append the data. There are 3 columns in the table
    G = []
    H = []
    I = []

    # Retrieving the Countries requires different method since they are links.
    for row in right_table.find_all('tr'):
        names = row.find('a', href=True)
        if names:
            title = names.get('title')
            H.append(title)

    # Parsing data and adding to lists above
    for row in right_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 3:
            G.append(cells[0].find(text=True))
            I.append(cells[2].find(text=True))

    # Placing lists into a dataframe
    UN = pd.DataFrame(H, columns=['Country'])
    UN['Rank'] = G
    UN['GDP'] = I

    # Removing 'next line' from Series
    UN['GDP'] = UN['GDP'].str.replace(r'\n', '')
    return UN

# Calling function
International_Monetary_Fund()
World_Bank()
United_Nations()

# Global dataframe
print(IMF)
print(WB)
print(UN)

# Writing data to csv
IMF.to_csv(r'C:\Users\Mat\PycharmProjects\web scrapping\International Monetary Fund.csv', index=False)
WB.to_csv(r'C:\Users\Mat\PycharmProjects\web scrapping\World Bank.csv', index=False)
UN.to_csv(r'C:\Users\Mat\PycharmProjects\web scrapping\United Nations.csv', index=False)
