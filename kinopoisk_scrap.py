import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import xlsxwriter

workbook=xlsxwriter.Workbook('kinopoisk.xlsx')
worksheet=workbook.add_worksheet()

temp1=True
temp2=True
temp3=True
print('Kinopoisk-scraper says HELLO:)\n')
while(temp1):
    print('Input option for sorting:name/rating')
    option=input().lower()
    if option=='name' or option=='rating':
        temp1=False
    else:
        print('Incorrect input!Please, try again\n')

while(temp2):
    print('Input year')
    year=input()
    try:
        year=int(year)
        if year>2020:
            print('Sorry, we can"t to look into the future. Please, try again\n')
        elif year<=0:
            print('Incorrect input!Please, try again\n')
        else:
            temp2=False
    except:
        print('Incorrect input!Please, try again\n')

while(temp3):
    print('How many pages you want to explore?')
    pages=input()
    try:
        pages=int(pages)
        if pages<=0:
            print('Incorrect input!Please, try again\n')
        else:
            temp3=False
    except:
        print('Incorrect input!Please, try again\n')

url = f'https://www.kinopoisk.ru/s/type/film/list/1/order/{option}/m_act[year]/'
driver=selenium.webdriver.Firefox()
def scroll_to_bottom(driver):

    old_position = 0
    new_position = None


    while new_position != old_position:
        MovieNames=driver.find_elements_by_class_name('name')
                # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
    return MovieNames

def scrap():
    MovieNames=[]
    MovieLinks=[]
    flag=True
    i=1
    while(i<=int(pages)):
        try:
            Scrap_Result=[]
            Movie_info=[]
            driver.get(f'{url}{year}/page/{i}/')
            Scrap_Result=scroll_to_bottom(driver)
            for elem in Scrap_Result:
                info=elem.find_elements_by_class_name('js-serp-metrika')
                Movie_info.append(info)
            for data in Movie_info:
                for movie in data:
                    MovieLinks.append(movie.get_attribute('href'))
                    MovieNames.append(movie.text)
                flag=movie.text
            i+=1
        except:
            break
    return MovieNames,MovieLinks

def write_to_file(*args):
    for i,column in enumerate(args):
        worksheet.write_column(0,i,column)
        worksheet.set_column(i,i,len(max(column))+10)
title,link=scrap()
write_to_file(title,link)
print(f'Done!{len(title)} films sorted by {option} are waiting for u in Excel file "kinopoisk"')
workbook.close()
driver.quit()
