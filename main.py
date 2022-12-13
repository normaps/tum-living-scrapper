from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
import csv
# Define the structure of the data
csv_header = ['Available Date', 'Area', 'Rooms', 'Rent Price']

with open('tum_living.csv', 'w') as file:
    # 2. Create a CSV writer
    writer = csv.writer(file)
    # 3. Write data to the file
    writer.writerow(csv_header)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://living.tum.de/listings?viewMode=list")

    delay = 3 # seconds
    try:
        driver.maximize_window()
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.glide')))
        pages = driver.find_elements(By.CSS_SELECTOR, '.bx--pagination-nav__list-item')
        pageIndex = 1
        while pageIndex < len(pages) - 1:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.glide')))
            pages = driver.find_elements(By.CSS_SELECTOR, '.bx--pagination-nav__list-item')
            src = driver.page_source
            areas = re.findall(r'([0-9]+)\sm²', src)
            dates = re.findall(r'(?:immediately|[0-9]{2}\.[0-9]{2}\.[0-9]{4})', src)
            rooms = re.findall(r'(?<=<span class="listing-info-panel_title__)[a-zA-Z0-9]+">([0-9]{1}|[0-9]{1}\.'
                               r'[0-9]{1})?(?=<\/span>.+Rooms<\/span>)', src)
            prices = re.findall(r'([0-9]+)\s€', src)
            index = 0
            for area in areas:
                row = [dates[index], area, rooms[index], prices[index]]
                writer.writerow(row)
                index = index+1

            pageIndex += 1
            currentPage = pages[pageIndex].find_element(By.TAG_NAME, 'button')
            driver.execute_script("arguments[0].click();", currentPage)

    except TimeoutException:
        print("Loading took too much time!")
        driver.quit()
