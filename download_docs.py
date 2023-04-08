from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os
from time import sleep
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

chrome_options = Options()

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-error")
chrome_options.add_argument("--ignore-ssl-errors")

chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Set the URL prefix to search for
# url_prefix = "https://developers.cloudability.com/docs"

# Set the output PDF filename
pdf_filename = "output.pdf"

# Set up the Chrome driver
# driver_path = "/usr/local/bin/chromedriver"
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# driver = webdriver.Chrome(driver_path, options=options)

# Open the Wayback Machine search page for the URL prefix
driver.get(
    f"https://web.archive.org/web/*/https://developers.cloudability.com/docs/*")

# # Wait for the page to load and get the search results table
wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located((By.ID, "resultsUrl")))

# # Extract the URLs from the search results table
soup = BeautifulSoup(driver.page_source, 'html.parser')
wait = WebDriverWait(driver,5)

url_list = [a['href'] for a in soup.select('#resultsUrl a')]

# url_list = [
#     "20210919111840/https://developers.cloudability.com/docs/allocations"]


# Create a PDF object and set its properties
pdf = FPDF()
pdf.set_title("Wayback Machine Archives")
pdf.set_author("Web Archive")
pdf.set_subject("Archived URLs")
pdf.set_keywords("wayback machine, archive, urls")
pdf.add_page()

# Create a canvas object to add the web pages to the PDF
c = canvas.Canvas(pdf_filename, pagesize=letter)
url_list.pop(0)

# Loop through the URLs and download their archived pages
for url in url_list:
    # Get the archive URL for the current URL
    archive_url = f"https://web.archive.org/{url}"

    # Open the archive URL and take a screenshot
    driver.get(archive_url)
    sleep(5)  # Wait for the page to load
    # Wait for the donate modal to load and then close it
    # wait.until(EC.presence_of_element_located(
    #     (By.ID, "banner-close-image-white"))).click()

    screenshot_path = f"{url.split('/')[-2]}.png"
    driver.save_screenshot(screenshot_path)
    pdf.image(screenshot_path, x=10, y=10, w=190)

    # Scroll down the page and take additional screenshots
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    while current_position < scroll_height:
        driver.execute_script(
            f"window.scrollTo(0, {current_position + 620});")
        current_position += 620
        sleep(5)  # Wait for the page to scroll and images to load
        screenshot_path = f"{url.split('/')[-2]}_{current_position}.png"
        driver.save_screenshot(screenshot_path)

    # Add the screenshots to the PDF file
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=url, ln=1, align="C")
    for i in range(1, int(scroll_height/620) + 2):
        image_path = f"{url.split('/')[-2]}_{i*620}.png"
        pdf.add_page()
        pdf.image(image_path, x=10, y=10, w=190)
        os.remove(image_path)

    # Remove the first screenshot, which was already added to the PDF
    os.remove(f"{url.split('/')[-2]}.png")

    # Close the driver
    # driver.quit()

# Save the PDF file
pdf.output(pdf_filename)

# Print a message indicating the output filename
print(f"PDF created: {pdf_filename}")
