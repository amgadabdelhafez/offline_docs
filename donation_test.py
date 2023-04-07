from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

driver = webdriver.Chrome()

# Set cookie expiration time to one hour in the future
expires = datetime.now() + timedelta(hours=1)


try:
    base_url = "https://web.archive.org"
    archive_url = "https://web.archive.org/web/20210919111840/https://developers.cloudability.com/docs/allocations"
    driver.get(base_url)
    # cookie_1 = {"name": "donation", "value": "x", "domain": ".web.archive.org",
    #             "path": "/web/20210919111840/https://developers.cloudability.com/"}
    # cookie_2 = {"name": "donation", "value": "x", "domain": ".archive.org",
    #             # Set the cookie expiration time
    #             "path": "/"
    #             }

    cookie = {'domain': '.archive.org', 'expiry': 1680764654, 'httpOnly': False,
              'name': 'donation', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'x'}

    # driver.add_cookie(cookie_1)
    driver.add_cookie(cookie)
    driver.refresh()

    # Find the element that contains the Shadow Root
    element_with_shadow_root = driver.find_element_by_css_selector(
        "your-css-selector")

    # Execute JavaScript to open the Shadow Root
    driver.execute_script(
        "arguments[0].shadowRoot.querySelector('your-shadowroot-selector').open()", element_with_shadow_root)

    # Find the button inside the Shadow Root
    button_inside_shadow_root = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "your-button-selector"))
    )

    # Click the button
    button_inside_shadow_root.click()

finally:
    driver.quit()
