from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from urllib.parse import quote_plus
import time
import os

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

GCP_KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chave-gcp.json")


CITIES = [
    ("São José", "Sao Jose", "sao-jose", "-27.59504", "-48.613768"),
    ("Palhoça", "Palhoca", "palhoca", "-27.645399", "-48.668056"),
    ("Florianópolis", "Florianopolis", "florianopolis", "-27.596904", "-48.549477"),
]

def build_url(display, ascii_name, slug, lat, lng):
    onde = f",Santa Catarina,{display},,,,,city,BR>Santa Catarina>NULL>{ascii_name},{lat},{lng},"
    return (
        f"https://www.vivareal.com.br/aluguel/santa-catarina/{slug}/apartamento_residencial/"
        f"?transacao=aluguel&onde={quote_plus(onde)}"
        f"&tipos=apartamento_residencial&page=1"
    )

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

def accept_cookies():
    try:
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, "cookie-notifier-cta")))
        cookie_btn.click()
    except:
        pass

data_rows = []

def get_data(city):
    try:
        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-cy="rp-property-cd"]')))
        for card in cards:
            try:
                t = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-location-txt"]').text.split(" em ")[0]
                a = card.find_element(By.CSS_SELECTOR, 'a').get_attribute('title').split(" em ")[-1].strip()
                m = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text
                b = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]').text
                l = card.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
                price_info = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]').text
                p = price_info.split("/")[0].replace("Aluguel de ", "").strip()
                c = price_info.split("Cond. R$ ")[1].split("\n")[0].split(" ")[0] if "Cond. R$ " in price_info else "0"
                tx = price_info.split("IPTU R$ ")[1].split("\n")[0].split(" ")[0] if "IPTU R$ " in price_info else "0"
                data_rows.append((city, t, m, b, a, p, c, tx, l))
            except:
                continue
    except:
        pass

def scrape_city(display, ascii_name, slug, lat, lng):
    driver.get(build_url(display, ascii_name, slug, lat, lng))
    accept_cookies()
    time.sleep(5)

    try:
        total_pages = int(driver.find_elements(By.CLASS_NAME, 'olx-core-pagination__button')[-1].text)
    except (IndexError, ValueError):
        total_pages = 1

    for page in range(1, total_pages + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        get_data(display)
        if page < total_pages:
            try:
                btn_next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="próxima página"]')))
                driver.execute_script("arguments[0].click();", btn_next)
                time.sleep(3)
            except:
                break

for city in CITIES:
    scrape_city(*city)

driver.quit()

spark = SparkSession.builder \
    .appName("VivaRealScraper") \
    .config("spark.jars.packages", "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5") \
    .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
    .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", GCP_KEY_PATH) \
    .getOrCreate()

if data_rows:
    schema = StructType([
        StructField("City", StringType(), True),
        StructField("Title", StringType(), True),
        StructField("Area", StringType(), True),
        StructField("Beds", StringType(), True),
        StructField("Address", StringType(), True),
        StructField("Price", StringType(), True),
        StructField("Condo", StringType(), True),
        StructField("IPTU", StringType(), True),
        StructField("Link", StringType(), True)
    ])
    
    df = spark.createDataFrame(data_rows, schema=schema)
    df.coalesce(1).write.mode("overwrite").parquet("gs://rent_scrapper/raw/rents_info.parquet")