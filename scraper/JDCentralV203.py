#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import re
from urllib.parse import unquote
import urllib.parse
import time
import datetime

print(datetime.datetime.now())
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

from webdriver_manager.chrome import ChromeDriverManager
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
driver.get("https://www.jd.co.th/")
import numpy as np
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//body/div[8]/div/div/div/div/i"))).click()


# In[2]:


actions = ActionChains(driver)
element = driver.find_element_by_xpath("//*[@id='nav-section-app']/div/div[1]/div[2]/div/ul/li[1]")
actions.move_to_element(element).perform() #mouse hover
subcategories = driver.find_elements_by_xpath("//div[@class='sub-item']/a[@title]")
allsubcategoryList = []
subcategoryList = []
for t in subcategories:
    allsubcategoryList.append(t.get_attribute("href"))
for g in range(34,37):
    subcategoryList.append(allsubcategoryList[g])
#subcategoryList.append(allsubcategoryList[37])
#subcategoryList.append(allsubcategoryList[38])
for l in subcategoryList:
    print(unquote(l))


# In[3]:


DataBrick = {"Name":[],"Price":[],"URL":[],"Image":[],"Store":[],"Review":[],"Score":[],"Category":[],"Subcategory":[],"Type":[],"Brand":[]}


# In[4]:


subRange = len(subcategoryList)
for subcate in range(0,1):
    driver.get(subcategoryList[subcate])
    subcategory = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='trigger']/span")))
    print(subcategory.text)
    try:
        LoadElement = driver.find_element_by_xpath("//*[@id='J_bottomPage']/span[2]/em/b")
        driver.execute_script("arguments[0].scrollIntoView();",LoadElement)
        time.sleep(3)
        Pagesearch = driver.find_element_by_xpath("//*[@id='J_bottomPage']/span[2]/em/b")
        Pagesearch = int(Pagesearch.text)-1
    except:
        Pagesearch = 0
    if (Pagesearch != 0):
        for pager in range(1,2):

            product = driver.find_elements_by_xpath("//*[@class='gl-item high']")
            rangeP = len(product) + 1
            
            for p in range(1,rangeP):
                runp = str(p)
                try:
                    LoadElement = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-img']/a/img")
                    driver.execute_script("arguments[0].scrollIntoView();",LoadElement)
                except:
                    pass
                
            for p in range(1,rangeP):
                runp = str(p)
                category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='crumbs-nav-item']//span[@class='crumbs-link']")))
                subcategory = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='trigger']/span")))
                try:
                    title = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='name-content-global']").text
                    price = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-price']/strong[@class='J_price price_lighter']/span[@class='num']").text
                    store = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-shop']/span/a").text
                    pid = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-price']/strong").get_attribute("id")
                    
                    try:
                        review = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='comment-num']").text
                        score = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-commit']").get_attribute('p-star')
                        numbersRe = re.findall(r'\d+', review)
                        numbersSc = re.findall(r'\d+', score)
                        review = abs(int(numbersRe[0]))
                        score = abs(int(numbersSc[0]))
                    except:
                        review = 0
                        score = 0
                    
                    ImageLoadElement = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//div[@class='p-img']/a/img[1]")
                    t_end = time.time() + 5
                    while (ImageLoadElement.get_attribute('src').startswith("data:image") and time.time() < t_end):
                        driver.execute_script("arguments[0].scrollIntoView();",ImageLoadElement)
                        ImageLoadElement = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//div[@class='p-img']/a/img[1]")
                    ImageLoadElement = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//div[@class='p-img']/a/img[1]")
                    image = ImageLoadElement.get_attribute('src')  
                   
                    DataBrick["Name"].append(title)
                    DataBrick["Price"].append(price)
                    DataBrick["Store"].append(store)
                    DataBrick["URL"].append('https://www.jd.co.th/product/'+pid+'.html')
                    DataBrick["Image"].append(image)
                    DataBrick["Review"].append(review)
                    DataBrick["Score"].append(score)
                    DataBrick["Category"].append(category.text)
                    DataBrick["Subcategory"].append(subcategory.text)
                    DataBrick["Type"].append(tl)
                    DataBrick["Brand"].append(bl)
                except:
                    pass

            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pager']/a[@clstag='pageclick|keycount|th_list_page|next_page']"))).click()
            except:
                pass
    else:            
        product = driver.find_elements_by_xpath("//li[@class='gl-item high']")
        rangeP = len(product) + 1
        for p in range(1,rangeP):
            runp = str(p)
            try:
                LoadElement = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-img']/a/img")
                driver.execute_script("arguments[0].scrollIntoView();",LoadElement)
            except:
                pass
        for p in range(1,rangeP):
            runp = str(p)
            category = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='crumbs-nav-item']//span[@class='crumbs-link']")))
            subcategory = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='trigger']/span")))
            try:
                title = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='name-content-global']").text
                price = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-price']/strong[@class='J_price price_lighter']/span[@class='num']").text
                store = driver.find_element_by_xpath("//*[@class='p-shop']/span/a").text
                pid = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-price']/strong").get_attribute("id")

                try:
                    review = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='comment-num']").text
                    score = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//*[@class='p-commit']").get_attribute('p-star')
                    numbersRe = re.findall(r'\d+', review)
                    numbersSc = re.findall(r'\d+', score)
                    review = abs(int(numbersRe[0]))
                    score = abs(int(numbersSc[0]))
                except:
                    review = 0
                    score = 0
                
                ImageLoadElement = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//div[@class='p-img']/a/img[1]")
                t_end = time.time() + 5
                while (ImageLoadElement.get_attribute('src').startswith("data:image") and time.time() < t_end):
                    driver.execute_script("arguments[0].scrollIntoView();",ImageLoadElement)
                    ImageLoadElement = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//div[@class='p-img']/a/img[1]")
                ImageLoadElement = driver.find_element_by_xpath("//li["+runp+"][@class='gl-item high']//div[@class='p-img']/a/img[1]")
                image = ImageLoadElement.get_attribute('src')
                
                DataBrick["Name"].append(title)
                DataBrick["Price"].append(price)
                DataBrick["Store"].append(store)
                DataBrick["URL"].append('https://www.jd.co.th/product/'+pid+'.html')
                DataBrick["Image"].append(image)
                DataBrick["Review"].append(review)
                DataBrick["Score"].append(score)
                DataBrick["Category"].append(category.text)
                DataBrick["Subcategory"].append(subcategory.text)
                DataBrick["Type"].append(tl)
                DataBrick["Brand"].append(bl)
            except:
                pass


# In[5]:


JdCentralData = pd.DataFrame(zip(np.array(DataBrick["Name"]),np.array(DataBrick["Price"]),np.array(DataBrick["Review"]),np.array(DataBrick["Score"]),np.array(DataBrick["Category"]),np.array(DataBrick["Subcategory"]),np.array(DataBrick["Store"]),np.array(DataBrick["Image"]),np.array(DataBrick["URL"])),columns=['Name','Price','Review','Score','Category','Subcategory','Store','Image','URL'])
JdCentralData["Platform"] = "JDCentral"
driver.quit()




# In[7]:


JdCentralData.to_csv("/c/Users/OMEN/airflow/scraper/RawData/JdCentral.csv",encoding='utf-8-sig',sep=";",index=False)

print(datetime.datetime.now())


# In[ ]:




