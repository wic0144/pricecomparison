#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import pandas as pd
import re
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import unquote
import numpy as np


# In[2]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

from webdriver_manager.chrome import ChromeDriverManager
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)


# In[3]:


driver.get('https://www.lazada.co.th/')


# In[7]:


actions = ActionChains(driver)
element = driver.find_element_by_xpath("//*[@class='lzd-links-bar']/div/div[9]/span").click()
# actions.move_to_element(element).perform() #mouse hover
language = driver.find_element_by_xpath("//*[@class='lzd-links-bar']/div/div[9]/div/div/div").click()


# In[22]:


actions = ActionChains(driver)
element = driver.find_element_by_xpath("//*[@class='lzd-site-nav-menu-dropdown']/ul/li[1]")
actions.move_to_element(element).perform() #mouse hover
subcategories = driver.find_elements_by_xpath("//*[@class='lzd-site-nav-menu-dropdown']/ul/ul[1]/li/a[@href]")

allsubcategory = []
subcategory = []

for e in subcategories:
    allsubcategory.append(e.get_attribute("href"))
for g in range(0,12):
    subcategory.append(allsubcategory[g])
for l in subcategory:
    print(unquote(l))
    
DataBrick = {"Name":[],"Price":[],"URL":[],"Image":[],"Review":[],"Score":[],"Category":[],"Platform":[]}

import time

for subcate in range(0,6):
    driver.get(subcategory[subcate])
    subcategorylist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='lzd-site-nav-menu-dropdown']/ul/ul[1]/li/a")))
    print(subcategorylist.text)
    
    Pagesearch = driver.find_element_by_xpath("//*[@class='e5J1n']/ul/li[8]/a[@href]")
    Pagesearch = int(Pagesearch.text)
    #Pagesearch = Pagesearch - 1
    
    for pager in range(1,2):
            product = driver.find_elements_by_xpath("//*[@class='Bm3ON']")
            rangeP = len(product) + 1
            
            for p in range(1,2):
                runp = str(p)
                LoadElement = driver.find_element_by_xpath("//*[@class='Bm3ON']/div/div/div/div/a/div/img")
                driver.execute_script("arguments[0].scrollIntoView();",LoadElement)
            #print(rangeP)
            for p in range(1,rangeP):
                runp = str(p)
                # category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='crumbs-nav-item']//span[@class='crumbs-link']")))
                cate = driver.find_element_by_xpath("//*[@class='y9-OE']/div/div/div/a").text
                title = driver.find_element_by_xpath("//*[@class='_17mcb']/div["+runp+"]/div/div/div[2]/div[@class='RfADt']/a")
                #print(title.get_attribute('title'))
                price = driver.find_element_by_xpath("//*[@class='_17mcb']/div["+runp+"]/div/div/div[@class='buTCk']/div[@class='aBrP0']/span").text
                #print(price)
                pid = driver.find_element_by_xpath("//*[@class='_17mcb']/div["+runp+"]//div[@class='_95X4G']/a").get_attribute('href')
                ImageLoadElement = driver.find_element_by_xpath("//*[@class='_17mcb']/div["+runp+"]/div/div/div/div/a/div/img")
                t_end = time.time() + 2.5
                
                while (ImageLoadElement.get_attribute('src').startswith("https://laz-img-cdn.alicdn.com/tfs/TB1Yltkl4TpK1RjSZFKXXa2wXXa-720-720.png_340x340q80.jpg") and time.time() < t_end):
                    driver.execute_script("arguments[0].scrollIntoView();",ImageLoadElement)
                    ImageLoadElement = driver.find_element_by_xpath("//*[@class='_17mcb']/div["+runp+"]/div/div/div/div/a/img")
                image = ImageLoadElement.get_attribute('src')
                try:
                    review = driver.find_element_by_xpath("//*[@class='_17mcb']/div["+runp+"]/div/div/div/div[@class='_6uN7R']/div/span").text
                    #score = driver.find_elements_by_xpath("//*[@class='_17mcb']/div["+runp+"]/div/div//div[@class='buTCk']//div[@class='_6uN7R']/div[@class='mdmmT _32vUv']").get_attribute('p-star')
                    numbersRe = re.findall(r'\d+', review)
                    #numbersSc = re.findall(r'\d+', score)
                    review = abs(int(numbersRe[0]))
                    score = 0
                except:
                    review = 0
                    score = 0                
                DataBrick["Name"].append(title.get_attribute('title'))
                DataBrick["Price"].append(price)
                # DataBrick["Store"].append(store)
                DataBrick["URL"].append(pid)
                DataBrick["Image"].append(image)
                DataBrick["Review"].append(review)
                DataBrick["Score"].append(score)
                #DataBrick["Category"].append(category.text)
                DataBrick["Category"].append(cate)
            print(pager)
#             WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='ant-pagination']/li[@class='ant-pagination-next']"))).click()


# In[23]:


LazadaData = pd.DataFrame(zip(np.array(DataBrick["Name"]),np.array(DataBrick["Price"]),np.array(DataBrick["Review"]),np.array(DataBrick["Score"]),np.array(DataBrick["Image"]),np.array(DataBrick["Category"]),np.array(DataBrick["URL"])),columns=['Name','Price','Review','Score','Image','Category','URL'])
LazadaData["Platform"] = "Lazada"


# In[24]:


LazadaData


# In[8]:


LazadaData.to_csv("/c/Users/OMEN/airflow/scraper/RawData/Lazada.csv",encoding='utf-8-sig',sep=';',index=False)


# In[ ]:




