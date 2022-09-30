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
        # scrape_uniswap.py

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
import csv
import pandas as pd

df = pd.read_csv('uni_poly.csv')

df['metric'] = (df['Vol 7day']/df['TVL'])*df['Fees']
df_sort = df.sort_values("metric", ascending=False)
df_sort.head