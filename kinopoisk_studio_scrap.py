import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter

studio_list=[]
studio_values=[]

url = f'https://www.kinopoisk.ru/s'
driver=selenium.webdriver.Firefox()
driver.get(url)
check_studio=driver.find_element(By.NAME,"m_act[company]")
all_studios=Select(check_studio)
##wating for the values to load
element = WebDriverWait(driver,10).until(EC.element_to_be_selected(all_studios.options[0]))
studios=all_studios.options

for index in range(2, len(studios)):
    studio_list.append((studios[index].text))
    studio_values.append((studios[index].get_attribute('value')))
    
driver.quit()
print(studio_list,studio_values)
