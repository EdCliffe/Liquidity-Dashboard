#%%
import time
import csv
import pandas as pd
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from IPython.display import display
import numpy as np
import re

chrome_options = Options()
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome("/usr/bin/chromedriver", options=chrome_options)
driver.maximize_window()

https = "https://"
fi = "curve.fi"
networks = ["", "polygon.", "arbitrum.",
            "aurora.", "avalanche.", "optimism.",
            "fantom.", "harmony.","xdai.","moonbeam.",
            "kava."]

networks_for_files = ["",]
networks_for_files[1:] = networks[1:][:-1]

curve_urls = [https + i + fi for i in networks ]
curve_filenames = ["curve_" + i for i in networks]
curve_filenames[0] = "curve_etherum"
