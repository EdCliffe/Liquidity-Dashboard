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

uni_urls = ["https://info.uniswap.org/#/pools",
        "https://info.uniswap.org/#/polygon/pools",
        "https://info.uniswap.org/#/optimism/pools",
        "https://info.uniswap.org/#/arbitrum/pools",
        "https://info.uniswap.org/#/celo/pools",]

uni_filenames = ["uni_eth", "uni_poly", "uni_optimism", "uni_arbitrum", "uni_celo"]

for j in range(len(uni_urls)):
    driver.get(uni_urls[j])
    if j == 1:
        print("waiting 40")
        time.sleep(40)
    if j == 3:
        print("waiting 30")
        time.sleep(30)
    print("waiting 6")
    time.sleep(6)
    
    nums = []
    names = []
    uni_buttons= [ ]
    # gather page data
    for i in range(4):
        try:
            pairs = driver.find_elements_by_xpath('//div[@class="sc-chPdSV goKJOd sc-bMVAic jAcXPQ css-63v6lo"]')
        except NoSuchElementException:
            driver.get(uni_urls[j])
            print("waiting 20")
            time.sleep(20)
            pairs = driver.find_elements_by_xpath('//div[@class="sc-chPdSV goKJOd sc-bMVAic jAcXPQ css-63v6lo"]')

        print("gather page")
        # iterate through page elements to get data
        for row in pairs:
            names.append(row.text) # add data to list
        stats = driver.find_elements_by_xpath('//div[@class="sc-chPdSV goKJOd sc-bMVAic eOIWzG css-63v6lo"]')
        for row in stats:                                    
            nums.append(row.text)
        # click button 
        print("click button")
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[4]/div/div[13]/div[3]/div").click()
    
    # click buttons to return to page 1
    if j == 0:
        driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div[3]/div/div[4]/div/div[9]/div[1]/div").click()
        driver.find_element(By.XPATH,  '//*[@id="root"]/div/div[2]/div[3]/div/div[4]/div/div[13]/div[1]/div').click()
        driver.find_element(By.XPATH,  '//*[@id="root"]/div/div[2]/div[3]/div/div[4]/div/div[13]/div[1]/div').click()
        driver.find_element(By.XPATH,  '//*[@id="root"]/div/div[2]/div[3]/div/div[4]/div/div[13]/div[1]/div').click()
    if j in[1,2,3]:
        for i in range(4):
            driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div[3]/div/div[4]/div/div[13]/div[1]/div").click()
    
    # clean gathered data
    clean_names = []                   
    clean_fees = []
    for i in range(1,80,2):
        temp = names[i].split()
        clean_names.append(temp[0])
        clean_fees.append(temp[1])
    
    # swap m and b for 0's

    for i in range(len(nums)):
            
            if nums[i][0] == "<":
                nums[i] = nums[i][2:]
            else:
                nums[i] = nums[i][1:]
            
            k = 0 
            while k == 0:
                if nums[i][-1] == 'k':
                    nums[i] = nums[i][:-1]
                    nums[i] = int((float(nums[i]))*1000)
                    k+=1
                elif nums[i][-1] == 'm':
                    nums[i] = nums[i][:-1]
                    nums[i] = int((float(nums[i]))*1000000)
                    k+=1
                elif nums[i][-1] == 'b':
                    nums[i] = nums[i][:-1]
                    nums[i] = int((float(nums[i]))*1000000000)
                    k+=1
                else: 
                    k+=1

            # nums[i] = re.sub('k','000', nums[i])
            # nums[i] = re.sub('m','000000', nums[i])
            # nums[i] = re.sub('b','000000000', nums[i])
            # nums[i] = float(nums[i])
    
    # remove %s
    for i in range(len(clean_fees)):
        clean_fees[i] = clean_fees[i][:-1]

    print(clean_names)
    print(clean_fees)
    df = pd.DataFrame(columns = ["Pool", "Fees", "TVL", "Vol 24hr", "Vol 7day"]) 
    df["Pool"] = clean_names
    df["Fees"] = clean_fees
    df["TVL"] = [nums[i] for i in range(0,120,3)]
    df["Vol 24hr"] = [nums[i] for i in range(1,120,3)]
    df["Vol 7day"] = [nums[i] for i in range(2,120,3)]

    df.head
    df.to_csv(f'{uni_filenames[j]}.csv', index=False)
    print(f"{uni_filenames[j]} complete")

# %%
