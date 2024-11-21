from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time
import csv

# Define the path to the ChromeDriver executable
CHROME_DRIVER = "/opt/homebrew/Caskroom/chromedriver/130.0.6723.91/chromedriver-mac-arm64/chromedriver"

# Create a Service object with the path
service = Service(CHROME_DRIVER)

# Initialize the Chrome driver with the Service
driver = webdriver.Chrome(service=service)

# Set up CSV file for data output
csv_file = open('data/class_pass_21_11_2024.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['tags', 'pilates', 'name', 'location', 'avg_rating', 'num_ratings'])

# Start scraping process
driver.get('https://classpass.com/search/london/pilates')
index = 1

while True:
    print(f'Scraping page: {index}')
    time.sleep(2)

    studios = driver.find_elements("xpath", '//li[@data-component="SearchResultsList"]')
    print(f'Studios = {len(studios)}')

    for studio in studios:
        data_dict = {}
        try:
            tags = studio.find_element("xpath", './/div[@data-qa="VenueItem.activities"]').text.lower()
            pilates = 'pilates' in tags
            tags = tags.split(',')
        except:
            tags = None
            pilates = None

        name = studio.find_element("xpath", './/a[@data-qa="VenueItem.name"]').text

        try:
            location = studio.find_element("xpath", './/div[@data-qa="VenueItem.location"]').text
        except:
            location = None

        try:
            avg_rating = float(studio.find_element("xpath", './/span[@class="ratings__rating ratings--child"]/span').text)
        except:
            avg_rating = None

        try:
            num_ratings = studio.find_element("xpath", './/span[@class="ratings__count ratings--child"]').text
        except:
            num_ratings = None

        data_dict['tags'] = tags
        data_dict['pilates'] = pilates
        data_dict['name'] = name
        data_dict['location'] = location
        data_dict['avg_rating'] = avg_rating
        data_dict['num_ratings'] = num_ratings

        writer.writerow(data_dict.values())

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        next_button = driver.find_element("xpath", '//nav[@role="navigation"]/button[2]')
        next_button.click()
        index += 1

    except ElementClickInterceptedException:
        try:
            ad_button = driver.find_element("xpath", '//button[@aria-label="hide promotion"]')
            ad_button.click()
            next_button.click()
            index += 1
        except:
            break

driver.quit()
csv_file.close()

