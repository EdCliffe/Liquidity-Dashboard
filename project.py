from bot import Scraper
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Define targets ====================

# Coin price

# https://info.uniswap.org/#/pools
# for each network
# gather each of the 5 pages of the top pools
# V2 - https://v2.info.uniswap.org/
# Ethereum, Polygon, optimism, Arbitrum, Celo

# https://app.1inch.io/#/1/earn/pools
# for each network, click expand for all visible entries, 
# gather info
# BNB network, ethereum

# https://curve.fi/pools
# After all the data is loaded,
# scrape metrics
# ethereum, arbitrum, AVAX, Fantom, harmony, optimism, polygon, xDai, Moonbeam

# https://pancakeswap.finance/info
# click through the pools to get each page
# BNB and ethereum

# https://app.balancer.fi/#/
# click extend and gather metrics
# Ethereum, polygon, arbitrum 

# gas fees for each network
# https://cointool.app/gasPrice
# click through each option

# can grab coin prices from here https://coinmarketcap.com/ , or from any of the swapping platforms..?

# defi tokens here https://coinmarketcap.com/view/defi/

# Scrape data from targets =============

class Liquidity_Scraper(Scraper):
    def __init__(self) -> None:
        super().__init__()
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

# Scrape Uniswap v3
    def scrape_uniswap_V3(self):
        self.sel_get_url("https://info.uniswap.org/#/pools")
        table = self.driver.find_element_by_xpath("/html/body/div/div/div[2]/div[3]/div/div[4]")
        for table_row in table:
            data = table_row
            print(data)

        # self.sel_click_xpath("/html/body/div/div/div[2]/div[3]/div/div[4]/div/div[13]/div[3]/div")
# Scrape Uniswap v2
    def scrape_uniswap_V2(self):
        self.sel_get_url("https://v2.info.uniswap.org/")

# scrape 1inch
    def scrape_1inch(self):
            self.sel_get_url("https://app.1inch.io/#/1/earn/pools")
# scrape curve
    def scrape_curve(self):
            self.sel_get_url("https://curve.fi/pools")

# scrape pancake
    def scrape_pancake(self):
            self.sel_get_url("https://pancakeswap.finance/info")

# scrape balancer
    def scrape_balancer(self):
            self.sel_get_url("https://app.balancer.fi/#/")
    
# scrape gas fees
    def scrape_gas(self):
            self.sel_get_url("https://cointool.app/gasPrice")

# scrape coin prices
    def scrape_coinprices(self):
            self.sel_get_url("https://coinmarketcap.com/")

# Set up SQL database ====================

# In GCP, Azure? 
# Add data to database

# store in tables, one table per source per day, can then do 1-week rolling analytics, removing 1 month old values




# Calculate metrics
# best looking pools that day
# average best over the last 1 week, taking price stability into account

# Scrape metrics from database into dashboard


#%%
import time
import pandas as pd
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome("/usr/bin/chromedriver", options=chrome_options)
driver.maximize_window()

url = "https://info.uniswap.org/#/pools"

driver.get('https://info.uniswap.org/#/pools')
time.sleep(4)
pairs = driver.find_elements_by_xpath('//div[@class="sc-chPdSV goKJOd sc-bMVAic jAcXPQ css-63v6lo"]')
stats = driver.find_elements_by_xpath('//div[@class="sc-chPdSV goKJOd sc-bMVAic eOIWzG css-63v6lo"]')

# click button 
driver.find_element(By.XPATH, "//div[@class='sc-GMQeP hXYrmI'").click()

# gather more tables, click button etc, make large list of all 6 pages, then combine at the end

names = []
for row in pairs:
    names.append(row.text)

nums = []
for row in stats:
    nums.append(row.text)

clean_names =[]

for i in range(1,21,2):
    clean_names.append(names[i])


df = pd.DataFrame(columns = ["Pool","TVL", "Vol 24hr", "Vol 7day"]) 
df["Pool"] = clean_names

df["TVL"] = [nums[i] for i in range(0,30,3)]
df["Vol 24hr"] = [nums[i] for i in range(1,30,3)]
df["Vol 7day"] = [nums[i] for i in range(2,30,3)]



