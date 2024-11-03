from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.pilates_feed import call_class_pass_website

# Data to store output
path_output = 'data/class_pass_output.csv'

# Define the path to the ChromeDriver executable
chrome_driver_path = "/opt/homebrew/Caskroom/chromedriver/130.0.6723.91/chromedriver-mac-arm64/chromedriver"

# Create a Service object with the path
service = Service(chrome_driver_path)

# Initialize the Chrome driver with the Service
driver = webdriver.Chrome(service=service)

call_class_pass_website(driver, data_path=path_output)

print(f"Data saved to `{path_output}`")
