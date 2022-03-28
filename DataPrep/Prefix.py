# %%
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from decimal import Decimal
from pyspark.sql.functions import *
import pyspark.sql.functions as F
import pandas as pd
import os
import re
import sys
import numpy as np

# %%
appName = "DataPrep"
master = "spark://LAPTOP-NKV0VISO.localdomain:7077"
# master = "local[*]"

# %%
# Create Spark session
spark = SparkSession.builder \
    .config('spark.ui.port','8080') \
    .appName(appName) \
    .master(master) \
    .getOrCreate()

# %%
alldata = spark.read.format("csv")\
                    .option("header", True)\
                    .option("delimiter",";") \
                    .load("hdfs://localhost:9000/data_upload/master/JD+Shopee+Lazada.csv")

# %%
df = alldata.toPandas()

# %%
from pythainlp.corpus.common import thai_words
from pythainlp import word_tokenize, Tokenizer


# %%
df_copy = df

# %%
for index, row in df_copy.iterrows():
    x = re.findall('^Lazada', str(row["Platform"]))
    if x:
        row["Platform"]="Lazada"

# %%
for index, row in df_copy.iterrows():
    x = re.findall('^"Lazada', str(row["Platform"]))
    if x:
        row["Platform"]="Lazada"

# %%
df_copy.Platform.drop_duplicates()

# %%
df.Platform.drop_duplicates()

# %%
df_copy_copy = df_copy[df_copy.Platform.isin(['Shopee','Lazada','JDCentral'])]

# %%
df_copy_copy

# %%
df_copy_copy.Category.drop_duplicates()

# %%
drop=[]
df_copy_copy4 =df_copy_copy[df_copy_copy.Category.isin(['เครื่องทำน้ำอุ่น','อื่นๆ','ไมโครเวฟและเตาอบ','เตาแก๊ส','เครื่องใช้ไฟฟ้าภายในบ้าน','พัดลม','พัดลมไอเย็น','เครื่องดูดฝุ่นและอุปกรณ์ดูแลพื้น','เครื่องใช้ไฟฟ้าในครัวขนาดเล็ก','เครื่องปรับอากาศ','เตารีดและอุปกรณ์ดูแลผ้า','เครื่องซักผ้าและเครื่องอบผ้า','ตู้เย็น','พัดลม','พัดลม','พัดลม','เครื่องฟอกอากาศ'])]
for index, row in df_copy_copy4.iterrows():
        drop.append(index)

# %%
df_copy_copy = df_copy_copy.drop(drop)

# %%
df_copy_copy.Category.drop_duplicates()

# %%

# %%



# %%
df_copy_copy

# %%
df_copy_copy_final = df_copy_copy


# %%
#df['Subcategory'] = df['Subcategory'].map({'เมาส์และคีย์บอร์ด':'อุปกรณ์เสริมคอมพิวเตอร์',
                             #'อุปกรณ์อิเล็กทรอนิกส์อัจฉริยะ':'อุปกรณ์เสริมคอมพิวเตอร์',
                             #'อุปกรณ์จัดเก็บและเคลื่อนย้ายข้อมูล':'อุปกรณ์จัดเก็บข้อมูล'})
df_copy_copy_final['Subcategory'] = df_copy_copy['Subcategory'].replace(
    ['เมาส์และคีย์บอร์ด','อุปกรณ์อิเล็กทรอนิกส์อัจฉริยะ','อุปกรณ์จัดเก็บและเคลื่อนย้ายข้อมูล'],
    ['อุปกรณ์เสริมคอมพิวเตอร์','อุปกรณ์เสริมคอมพิวเตอร์','อุปกรณ์จัดเก็บข้อมูล'])
#df.replace(to_replace ="อุปกรณ์เชื่อมต่ออินเทอร์เน็ตและโปรแกรม",value ="อุปกรณ์เชื่อมต่ออินเทอร์เน็ตและโปรแกรม")
#df.replace(to_replace ="เมาส์และคีย์บอร์ด",value ="ชิ้นส่วนคอมพิวเตอร์")
#df.replace(to_replace ="กล้อง",value ="กล้อง")
#df.replace(to_replace ="อุปกรณ์เสริมกล้อง",value ="อุปกรณ์เสริมกล้อง")
#df.replace(to_replace ="ชิ้นส่วนคอมพิวเตอร์",value ="ชิ้นส่วนคอมพิวเตอร์")
df_copy_copy_final = df_copy_copy[df_copy_copy.Subcategory != "อุปกรณ์อิเล็กทรอนิกส์ในรถยนต์"]
df_copy_copy_final = df_copy_copy[df_copy_copy.Subcategory != "เครื่องเสียงและสื่อบันเทิง"]

# %%
df_copy_copy_final1 = df_copy_copy_final[df_copy_copy_final.Platform.isin(['JDCentral'])]

# %%
df_copy_copy_final2 =  df_copy_copy_final[df_copy_copy_final.Platform.isin(['Shopee','Lazada'])]

# %%
mapping = {
        'ฟิล์ม':'อุปกรณ์เสริมโทรศัพท์มือถือและแท็บเล็ต',
        'อุปกรณ์สำหรับเล่นเกม':'อุปกรณ์สำหรับเกมเมอร์',
        'อุปกรณ์ไอทีสวมใส่':'อุปกรณ์เสริมคอมพิวเตอร์',
        'ซอฟต์แวร์':'อุปกรณ์เชื่อมต่ออินเทอร์เน็ตและโปรแกรม',
        'กล้องวงจรปิด':'กล้อง',
        'อุปกรณ์เสริมมือถือ':'อุปกรณ์เสริมโทรศัพท์มือถือและแท็บเล็ต',
        'มือถือและอุปกรณ์เสริม':'อุปกรณ์เสริมโทรศัพท์มือถือและแท็บเล็ต',
        'กล้อง':'กล้อง',
        'อุปกรณ์เน็ตเวิร์ค':'อุปกรณ์เชื่อมต่ออินเทอร์เน็ตและโปรแกรม',
        'แล็ปท็อปและคอมตั้งโต๊ะ':'คอมพิวเตอร์และแล็ปท็อป',
        'แท็บเล็ต':'โทรศัพท์มือถือและแท็บเล็ต',
        'อุปกรณ์เสริมกล้อง':'อุปกรณ์เสริมกล้อง',
        'ชิ้นส่วนคอมพิวเตอร์':'ชิ้นส่วนคอมพิวเตอร์',
        'ปริ้นเตอร์และอุปกรณ์เสริม':'อุปกรณ์เสริมคอมพิวเตอร์',
        'อุปกรณ์เสริมคอมพิวเตอร์':'อุปกรณ์เสริมคอมพิวเตอร์',
        'เลนส์':'อุปกรณ์เสริมกล้อง',
        'กล้องและอุปกรณ์ถ่ายภาพ':'อุปกรณ์เสริมกล้อง',
        'เมมโมรี่การ์ด':'อุปกรณ์จัดเก็บข้อมูล',
        'อุปกรณ์จัดเก็บข้อมูล':'อุปกรณ์จัดเก็บข้อมูล',
        'โทรศัพท์มือถือ':'โทรศัพท์มือถือและแท็บเล็ต',
        'แบตเตอรี่สำรอง':'อุปกรณ์เสริมโทรศัพท์มือถือและแท็บเล็ต',
        'โทรศัพท์บ้าน':'โทรศัพท์มือถือและแท็บเล็ต',
        'อุปกรณ์กันรอยหน้าจอ':'อุปกรณ์เสริมโทรศัพท์มือถือและแท็บเล็ต',
        'เคสและซองมือถือ':'อุปกรณ์เสริมโทรศัพท์มือถือและแท็บเล็ต',
        'กล้องแอคชั่น':'กล้อง',
        'โทรศัพท์มือถือและแท็บเล็ต':'โทรศัพท์มือถือและแท็บเล็ต',
        'โดรน':'กล้อง',
        'กล้องและระบบรักษาความปลอดภัย':'กล้อง',
        'แล็ปท็อป':'คอมพิวเตอร์และแล็ปท็อป',
        'กล้องมิลเลอร์เลส':'กล้อง',
        'กล้องวิดีโอ':'กล้อง',
        'กล้องอินสแตนท์':'กล้อง',
        'คอมพิวเตอร์แบบตั้งโต๊ะ':'คอมพิวเตอร์และแล็ปท็อป',
        'กล้องคอมแพค':'กล้อง',
        'กล้อง DSLR':'กล้อง',
        'เครื่องเล่นเกมคอมโซล':'อุปกรณ์สำหรับเกมเมอร์',
        'คอมพิวเตอร์และแล็ปท็อป':'คอมพิวเตอร์และแล็ปท็อป'
    }


# %%
df_copy_copy_final2['Subcategory'] = df_copy_copy_final2.Category.map(mapping)

# %%
df_copy_copy.Subcategory.drop_duplicates()

# %%
df_copy_copy_final2

# %%
frames = [df_copy_copy_final1, df_copy_copy_final2]

# %%
result = pd.concat(frames)

# %%
result

# %%
result = result.rename(columns={"Category": "Category1"})
result = result.rename(columns={"Subcategory": "Category"})
result = result.rename(columns={"Category1": "Subcategory"})

# %%
result

# %%
Mobile_phones_and_tablets =  result[result.Category.isin(['โทรศัพท์มือถือและแท็บเล็ต'])]
Mobile_phone_and_tablet_accessories =  result[result.Category.isin(['อุปกรณ์เสริมโทรศัพท์มือถือและแท็บเล็ต'])]
Computers_and_laptops =  result[result.Category.isin(['คอมพิวเตอร์และแล็ปท็อป'])]
Storage_device =  result[result.Category.isin(['อุปกรณ์จัดเก็บข้อมูล'])]
Internet_connection_devices_and_programs =  result[result.Category.isin(['อุปกรณ์เชื่อมต่ออินเทอร์เน็ตและโปรแกรม'])]
Computer_accessories =  result[result.Category.isin(['อุปกรณ์เสริมคอมพิวเตอร์'])]
Computer_Parts =  result[result.Category.isin(['ชิ้นส่วนคอมพิวเตอร์'])]
Camera =  result[result.Category.isin(['กล้อง'])]
Camera_accessories =  result[result.Category.isin(['อุปกรณ์เสริมกล้อง'])]
Gamer_gear =  result[result.Category.isin(['อุปกรณ์สำหรับเกมเมอร์'])]

# %%
# Mobile_phones_and_tablets.to_csv('./result/Mobile_phones_and_tablets.csv',encoding='utf-8-sig',sep=';',index= False)
# Mobile_phone_and_tablet_accessories.to_csv('./result/Mobile_phone_and_tablet_accessories.csv',encoding='utf-8-sig',sep=';',index= False)
# Computers_and_laptops.to_csv('./result/Computers_and_laptops.csv',encoding='utf-8-sig',sep=';',index= False)
# Storage_device.to_csv('./result/Storage_device.csv',encoding='utf-8-sig',sep=';',index= False)
# Internet_connection_devices_and_programs.to_csv('./result/Internet_connection_devices_and_programs.csv',encoding='utf-8-sig',sep=';',index= False)
# Computer_accessories.to_csv('./result/Computer_accessories.csv',encoding='utf-8-sig',sep=';',index= False)
# Computer_Parts.to_csv('./result/Computer_Parts.csv',encoding='utf-8-sig',sep=';',index= False)
# Camera.to_csv('./result/Camera.csv',encoding='utf-8-sig',sep=';',index= False)
# Camera_accessories.to_csv('./result/Camera_accessories.csv',encoding='utf-8-sig',sep=';',index= False)
# Gamer_gear.to_csv('./result/Gamer_gear.csv',encoding='utf-8-sig',sep=';',index= False)

# %%
result.to_csv('/c/Users/OMEN/airflow/DataPrep/FinalData/FinalResult.csv',encoding='utf-8-sig',sep=';',index= False)

# %%
# result.to_csv('./result/result2.csv',encoding='utf-8-sig')

# %% [markdown]
# df_copy_copy.Category.drop_duplicates().to_csv('Subcate.csv',encoding='utf-8-sig',sep=';',index= False)

# %% [markdown]
# df_copy_copy.Category.drop_duplicates().to_csv('Subcate.csv',encoding='utf-8-sig')


