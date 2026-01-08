from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.vivareal.com.br/aluguel/santa-catarina/sao-jose/')


# titles=[]
# beds=[]
# measure=[]
# address=[]
# prices=[]
# links=[]


link_elements = driver.find_elements(By.CSS_SELECTOR, "li[data-cy='rp-property-cd'] a")
links=[]
for element in link_elements:
    links.append(element.get_attribute("href"))
print(links)


#Fechando o web driver
driver.close()