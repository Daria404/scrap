import bs4
import requests
import excel_w
from excel_w import workbook
import xlsxwriter
from kinopoisk_studio_scrap import studio_list, studio_values

url = 'https://www.kinopoisk.ru/s/type/film/list/1/m_act[company]/'
studio_res = []


def studios_films():
    for i, value in enumerate(studio_values):
        page = requests.get(f'{url}{value}')
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        studio_films = soup.find(
            "span", {"class": "search_results_topText"}).getText()
        studio_films = studio_films.split(' ')
        res = studio_films[-1]
        studio_res.append(res)
    return studio_res


films = studios_films()
excel_w.write_to_file(studio_list, studio_values, films)
workbook.close()
print('Done!')
