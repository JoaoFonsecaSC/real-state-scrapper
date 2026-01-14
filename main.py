from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

driver.get('https://www.vivareal.com.br/aluguel/santa-catarina/sao-jose/apartamento_residencial/?transacao=aluguel&onde=%2CSanta+Catarina%2CS%C3%A3o+Jos%C3%A9%2C%2C%2C%2C%2Ccity%2CBR%3ESanta+Catarina%3ENULL%3ESao+Jose%2C-27.59504%2C-48.613768%2C&tipos=apartamento_residencial&page=1')

def accept_cookies():
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "cookie-notifier-cta")))
        cookie_btn.click()
        time.sleep(1)
    except:
        try:
            btn_adopt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='adopt']")))
            btn_adopt.click()
        except:
            pass

def wait_time():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

titles, addresses, measures, prices, condo_prices, taxes, links, beds = [], [], [], [], [], [], [], []

def get_data():
    cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-cy="rp-property-cd"]')))
    for card in cards:
        try:
            titles.append(card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-location-txt"]').text.split(" em ")[0])
            addresses.append(card.find_element(By.CSS_SELECTOR, 'a').get_attribute('title').split(" em ")[-1].strip())
            measures.append(card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text)
            beds.append(card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]').text)
            links.append(card.find_element(By.CSS_SELECTOR, 'a').get_attribute("href"))
            price_info = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]').text
            prices.append(price_info.split("/")[0].replace("Aluguel de ", "").strip())
            condo = price_info.split("Cond. R$ ")[1].split("\n")[0].split(" ")[0] if "Cond. R$ " in price_info else "0"
            condo_prices.append(condo)
            tax = price_info.split("IPTU R$ ")[1].split("\n")[0].split(" ")[0] if "IPTU R$ " in price_info else "0"
            taxes.append(tax)
        except Exception:
            continue

accept_cookies()
time.sleep(5)
total_pages = int(driver.find_elements(By.CLASS_NAME, 'olx-core-pagination__button')[-1].text)

for page in range(1, total_pages + 1):
    wait_time()
    get_data()
    if page < total_pages:
        try:
            btn_next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="próxima página"]')))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_next)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn_next)
            time.sleep(3)
        except (StaleElementReferenceException, TimeoutException):
            time.sleep(5)

df_rents_info = pd.DataFrame({
    'Title': titles, 'Area': measures, 'Beds': beds, 'Address': addresses,
    'Price': prices, 'Condo': condo_prices, 'IPTU': taxes, 'Link': links
})

df_rents_info.to_csv('rents_info.csv', sep=';', index=False, encoding='utf-8-sig')
driver.quit()