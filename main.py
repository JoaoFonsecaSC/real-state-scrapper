from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.vivareal.com.br/aluguel/santa-catarina/sao-jose/apartamento_residencial/?transacao=aluguel&onde=%2CSanta+Catarina%2CS%C3%A3o+Jos%C3%A9%2C%2C%2C%2C%2Ccity%2CBR%3ESanta+Catarina%3ENULL%3ESao+Jose%2C-27.59504%2C-48.613768%2C&tipos=apartamento_residencial')


time.sleep(10)
driver.execute_script("window.scrollTo(0, 1000);")
time.sleep(2)

titles, addresses, measures, prices, condo_prices, taxes, links = [], [], [], [], [], [], []


cards = driver.find_elements(By.CSS_SELECTOR, 'li[data-cy="rp-property-cd"]')


for card in cards:
    location_text = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-location-txt"]').text
    titles.append(location_text)
    addresses.append(location_text.split(" em ")[-1])
    
    measures.append(card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text)
    
    links.append(card.find_element(By.CSS_SELECTOR, 'a').get_attribute("href"))
    
    price_info = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]').text
    
    prices.append(price_info.split("/")[0].replace("Aluguel de ", "").strip())
    
    condo = price_info.split("Cond. R$ ")[1].split("\n")[0].split(" ")[0] if "Cond. R$ " in price_info else "0"
    condo_prices.append(condo)
    

    tax = price_info.split("IPTU R$ ")[1].split("\n")[0].split(" ")[0] if "IPTU R$ " in price_info else "0"
    taxes.append(tax)



df_rents_info = pd.DataFrame({
        'Title': titles,
        'Area': measures,
        'Address': addresses,
        'Price': prices,
        'Condo': condo_prices,
        'IPTU': taxes,
        'Link': links
    })

df_rents_info.to_csv('rents_info.csv',sep=';',index=False)

driver.quit()