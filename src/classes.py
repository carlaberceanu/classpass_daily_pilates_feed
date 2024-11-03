import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Chrome options
options = Options()
options.add_experimental_option("detach", True)

# Initialize the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the ClassPass page after login
driver.get("https://classpass.com/search")
driver.maximize_window()
time.sleep(5)  # Adjust sleep time as needed to allow the page to load fully

# Scrape Pilates classes
class_details = []
classes = driver.find_elements(By.CLASS_NAME, "BxPdL9O4XrbxTWkq4Fmn")  # Main container for each class item

for cls in classes:
    try:
        # Extract time
        time_element = cls.find_element(By.CSS_SELECTOR, "div[data-qa='ScheduleItem.time']")
        class_time = time_element.text

        # Extract class name
        name_element = cls.find_element(By.TAG_NAME, "h2")
        class_name = name_element.text

        # Extract instructor name
        instructor_element = cls.find_element(By.CSS_SELECTOR, "div[data-qa='ScheduleItem.teacher-name']")
        instructor_name = instructor_element.text

        # Extract venue (location)
        venue_element = cls.find_element(By.CSS_SELECTOR, "div[data-qa='ScheduleItem.venue']")
        venue_name = venue_element.text

        # Extract credits
        credits_element = cls.find_element(By.CSS_SELECTOR, "button[data-qa='ScheduleItem.action']")
        credits = credits_element.text.split()[0]  # Extract number before "credits"

        # Determine class type based on class name (if known)
        class_type = "Reformer" if "Reformer" in class_name else "Mat" if "Mat" in class_name else "Unknown"

        # Append to list
        class_details.append({
            "Time": class_time,
            "Name": class_name,
            "Instructor": instructor_name,
            "Venue": venue_name,
            "Credits": credits,
            "Type": class_type
        })
    except Exception as e:
        print(f"Error while scraping a class: {e}")

# Convert to DataFrame for easy analysis and display
df = pd.DataFrame(class_details)

# Display the scraped data
print(df)
