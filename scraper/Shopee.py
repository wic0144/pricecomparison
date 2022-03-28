#!/usr/bin/env python
# coding: utf-8

# In[8]:


import requests
import json
import pandas as pd
import time
Shopee_url = 'https://shopee.com.my'
# keyword_search = '11044958'
page = 100

DataBrick ={"Name":[],"Price":[],"historical_sold":[],"brand":[],
          "Score":[],"view_count":[],"Category":[],"Image":[],
          "Platform":[],"URL":[],"rating_star":[],"shop_location":[]}

Category={11044951: 'มือถือและอุปกรณ์เสริม',
 11044958: 'คอมพิวเตอร์และแล็ปท็อป',
 11044963: 'กล้องและอุปกรณ์ถ่ายภาพ',
#  11044955: 'เครื่องใช้ไฟฟ้าภายในบ้าน',
 11045117: 'โทรศัพท์มือถือ',
 11045118: 'แท็บเล็ต',
 11045119: 'เคสและซองมือถือ',
 11045113: 'อุปกรณ์เสริมมือถือ',
 11045115: 'อุปกรณ์กันรอยหน้าจอ',
 11045116: 'แบตเตอรี่สำรอง',
 11045112: 'อุปกรณ์ไอทีสวมใส่',
 11045114: 'อุปกรณ์เน็ตเวิร์ค',
#  11045025: 'อื่นๆ',
 11045191: 'อุปกรณ์เสริมคอมพิวเตอร์',
 11045192: 'อุปกรณ์สำหรับเล่นเกม',
 11045193: 'อุปกรณ์เน็ตเวิร์ค',
 11045194: 'อุปกรณ์จัดเก็บข้อมูล',
 11045195: 'แล็ปท็อปและคอมตั้งโต๊ะ',
 11045196: 'ปริ้นเตอร์และอุปกรณ์เสริม',
 11045197: 'ซอฟต์แวร์',
 11045198: 'ชิ้นส่วนคอมพิวเตอร์',
#  11045032: 'อื่นๆ',
 11045270: 'กล้อง',
 11045268: 'กล้องแอคชั่น',
 11045269: 'กล้องวงจรปิด',
 11045265: 'เลนส์',
 11045266: 'เมมโมรี่การ์ด',
 11045264: 'อุปกรณ์เสริมกล้อง',
 11045267: 'ฟิล์ม',
#  11045037: 'อื่นๆ',
#  11045158: 'ไมโครเวฟและเตาอบ',
#  11045159: 'พัดลมไอเย็น',
#  11045160: 'พัดลม',
#  11045161: 'โทรศัพท์บ้าน',
#  11045162: 'เตารีดและอุปกรณ์ดูแลผ้า',
#  11045163: 'เตาแก๊ส',
#  11045164: 'ตู้เย็น',
#  11045165: 'เครื่องฟอกอากาศ',
#  11045166: 'เครื่องปรับอากาศ',
#  11045167: 'เครื่องทำน้ำอุ่น',
#  11045168: 'เครื่องดูดฝุ่นและอุปกรณ์ดูแลพื้น',
#  11045169: 'เครื่องซักผ้าและเครื่องอบผ้า',
#  11045170: 'เครื่องใช้ไฟฟ้าในครัวขนาดเล็ก',
#  11045029: 'อื่นๆ'
         }


# In[9]:


for keyword_search in Category:
    headers = {'User-Agent': 'Chrome','Referer': '{}search?match_id={}'.format(Shopee_url, keyword_search)}
    for i in range(1,2):
    # Shopee API request
        url = 'https://shopee.co.th/api/v4/search/search_items?by=relevancy&match_id={}&limit=60&newest=180&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2&page={}'.format(keyword_search,i)
        r = requests.get(url, headers = headers).json()
        for item in r['items']:
            test= item['item_basic']['name']
            test =test.replace(" ", "-")
            test =test.replace("·", "-")
            test =test.replace("\t", "-")
            test =test.replace("''", "")
            test =test.replace('"', "")
            DataBrick['Name'].append(item['item_basic']['name'])
            DataBrick['Price'].append(item['item_basic']['price_min'])
            DataBrick['historical_sold'].append(item['item_basic']['historical_sold'])
            DataBrick['brand'].append(item['item_basic']['brand'])        
            DataBrick['Score'].append(item['item_basic']['liked_count'])        
            DataBrick['view_count'].append(item['item_basic']['view_count'])
            DataBrick['Platform'].append('Shopee')
            DataBrick['Image'].append("https://cf.shopee.co.th/file/{}_tn".format(item['item_basic']['image']))
            DataBrick['URL'].append("https://shopee.co.th/{}-i.{}.{}".format(test,item['item_basic']['shopid'],item['item_basic']['itemid']))
            DataBrick['rating_star'].append(item['item_basic']['item_rating']['rating_star'])
            DataBrick['shop_location'].append(item['item_basic']['shop_location'])
            DataBrick['Category'].append(Category.get(keyword_search))


# In[10]:


len(DataBrick['Name'])
# DataBrick['Name']


# In[11]:


Shopeedata = pd.DataFrame(zip(DataBrick['Name'],DataBrick['brand'],DataBrick['Price'] 
,DataBrick['historical_sold'],DataBrick['Score'],DataBrick['view_count'],DataBrick['Category']
,DataBrick['Image'],DataBrick['Platform'],DataBrick['URL'],DataBrick['rating_star'],DataBrick['shop_location'])
,columns=["Name","brand","Price","historical_sold",
          "Score","view_count","Category","Image",
          "Platform","URL","rating_star","shop_location"])


# In[13]:


Shopeedata['Price'] = Shopeedata['Price']/100000.0


# In[ ]:


Shopeedata.to_csv("/c/Users/OMEN/airflow/scraper/RawData/Shopee.csv",encoding='utf-8-sig',sep=";",index= False)

