from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import random
import re

driver = webdriver.Chrome()

driver.get("https://seekingalpha.com/stock-ideas/cramers-picks?page=1")

csv_file = open('Lightning_round_URLS2.csv', 'w')
# Windows users need to open the file using 'wb'
# csv_file = open('reviews.csv', 'wb')
writer = csv.writer(csv_file)
writer.writerow(['TITLE', 'TIME', 'URL', 'TITLE'])
# Page index used to keep track of where we are.
index = 1
pageCount = 50
while True:
    time.sleep(random.uniform(2, 5))
    try:
        url_list = ['https://seekingalpha.com/stock-ideas/cramers-picks?page=' + str(x) for x in range(2, pageCount)]
        for i in range(0, pageCount):
            #time.sleep(random.uniform(2, 5))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            driver.get(str(url_list[i]))
            print("Scraping Page number " + str(index)+ str(url_list[i]))
            #stopped on Scraping Page number 39https://seekingalpha.com/stock-ideas/cramers-picks?page=40
            index = index + 1
            #time.sleep(random.uniform(5, 10))
            # Find all the URLs.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #time.sleep(random.uniform(2, 5))

            URLS = driver.find_elements_by_xpath('//div[@class="media-body"]')
            print(URLS)
            for URL in URLS:
                # Initialize an empty dictionary for each review
                #https://seekingalpha.com/stock-ideas/cramers-picks?page=2
                #https://seekingalpha.com/stock-ideas/cramers-picks?page=3
                URL_dict = {}
                TITLE = URL.find_element_by_xpath('.//a[@class="a-title"]').text
                if str(TITLE) in URL_dict.values():
                    break
                if re.search('Lightning Round', TITLE):
                # Use Xpath to locate the title, content, username, date.
                # Once you locate the element, you can use 'element.text' to return its string.
                # To get the attribute instead of the text of each element, use 'element.get_attribute()'
                    TIME = URL.find_element_by_xpath('.//div[@class="a-info"]/span[3]').text
                    URL = URL.find_element_by_xpath('.//a[@class="a-title"]').get_attribute('href')
                    print(TIME)
                    print(TITLE)
                    print(URL)
                    URL_dict['title'] = TITLE
                    URL_dict['time'] = TIME
                    URL_dict['url'] = URL
                    writer.writerow(URL_dict.values())

        # Locate the next button on the page.
        # button = driver.find_element_by_xpath('//span[@class="bv-content-btn-pages-next"]')
        # driver.execute_script("arguments[0].click();", button)
        # button.click()
    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
        break
