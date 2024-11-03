import csv
import time

from selenium.common.exceptions import ElementClickInterceptedException


def call_class_pass_website(driver, data_path: str, location: str = 'london', activity: str = 'pilates'):
    """ Initialized chrome driver and scrapes Class Pass Website"""

    # Set up CSV file for data output
    csv_file = open(data_path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)
    writer.writerow(['tags', 'livestream', 'name', 'location', 'avg_rating', 'num_ratings'])

    # Start scraping process
    driver.get(f'https://classpass.com/search/{location}/{activity}')
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
                livestream = 'livestream' in tags
                tags = tags.split(',')
            except:
                tags = None
                livestream = None

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
            data_dict['livestream'] = livestream
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
