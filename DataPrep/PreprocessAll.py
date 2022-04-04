#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession
from pyspark.sql.types import *
from decimal import Decimal
from pyspark.sql.functions import *
import pyspark.sql.functions as F
import pandas as pd
import os
import re
import sys


# In[2]:


appName = "DataPrep"
master = "spark://LAPTOP-NKV0VISO.localdomain:7077"
# master = "spark://192.168.56.1:7077"
# master = "local[*]"


# In[3]:



spark = SparkSession.builder.config('spark.ui.port','8080').appName(appName).master(master).getOrCreate()


# In[37]:


dfShopee = spark.read.format("csv").option("header", True).option("delimiter",";").load("hdfs://localhost:9000/data_upload/Shopee.csv")


# In[38]:


dfLazada = spark.read.format("csv").option("header", True).option("delimiter",";").load("hdfs://localhost:9000/data_upload/master/Lazada.csv")


# In[39]:


dfJD = spark.read.format("csv").option("header", True).option("delimiter",";").load("hdfs://localhost:9000/data_upload/master/JdCentral.csv")




dfShopee.printSchema()


# In[9]:


dfLazada.printSchema()


# In[10]:


dfJD.printSchema()


# In[40]:


dfLazada = dfLazada.withColumnRenamed("Platform,,,,,,,,,,,,","Platform")
dfShopee = dfShopee.withColumnRenamed("Score","Review").withColumnRenamed("rating_star","Score")
dfLazada = dfLazada.where(col("Price").isNotNull())
dfJD = dfJD.withColumn("Score", col("Score") / 20)
dfShopee = dfShopee.where(col("Name").isNotNull())
dfShopee = dfShopee.where(col("Score").isNotNull())


# In[41]:


dfShopee = dfShopee.select(col("Name"),col("Price"),col("Review"),col("Score"),col("Image"),col("Category"),col("URL"),col("Platform"),col("brand"),col("historical_sold"),col("view_count"),col("shop_location"))
dfJD = dfJD.select(col("Name"),col("Price"),col("Review"),col("Score"),col("Image"),col("Category"),col("URL"),col("Platform"),col("Store"),col("Subcategory"))
dfLazada = dfLazada.select(col("Name"),col("Price"),col("Review"),col("Score"),col("Image"),col("Category"),col("URL"),col("Platform"))


# In[42]:


dfShopee.printSchema()


# In[43]:


dfLazada.printSchema()


# In[44]:


dfJD.printSchema()


# In[45]:


newdf = dfShopee.unionByName(dfJD, allowMissingColumns = True)
newdf = newdf.unionByName(dfLazada, allowMissingColumns = True)
newdf = newdf.dropDuplicates(['URL'])


# In[46]:


newdf.show()


# In[20]:


# newdf = newdf.withColumnRenamed("Category","SubCategory")


# In[23]:


# newdf = newdf.withColumn("Category", lit(''))


# In[30]:


newdf


# In[31]:


count_df = newdf.select('Category').groupBy('Category').count().sort('count', ascending=False)


# df_new = count_df.toPandas()
# df_new.to_csv('test.csv',encoding='utf-8-sig',index= False)

# In[33]:


count_df.show(100000)


# In[50]:


count_df = count_df.toPandas()
# count_df.to_csv('CT2.csv',encoding='utf-8-sig',index= False)


# In[47]:


keyword = []
thkeyword = []
numkeyword = []
string = ""
thstring = ""
numstring = ""
p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
for row in newdf.rdd.collect():
    line = re.sub(r"[^A-Za-z-?\d+\.?\d*]", " ", row["Name"].strip())
    thline = re.sub(r"[^\u0E00-\u0E7F-?\d+\.?\d*]", " ", row["Name"].strip())
    words = line.split()
    thwords = thline.split()
    for word in words:
        string += word + " "
        if re.search(p, word) is not None:
            for catch in re.finditer(p, word):
                numstring += catch[0] + " " # catch is a match object
    for thword in thwords: 
        thstring += thword + " "
    keyword.append(string)
    thkeyword.append(thstring)
    numkeyword.append(numstring)
    string = ""
    thstring = ""
    numstring = ""


# In[48]:


df_new = newdf.toPandas()


# In[49]:


df_new["enToken"] = keyword
df_new["thToken"] = thkeyword


# In[50]:


df_new['Score'] = df_new['Score'].fillna(0)
df_new['URL'] = df_new['URL'].dropna()
df_new['Platform'] = df_new['Platform'].dropna()
df_new['enToken'] = df_new['enToken'].replace('' ,'NULL')
df_new['thToken'] = df_new['thToken'].replace('' ,'NULL')


# In[51]:


for index, row in df_new.iterrows():
    row['Price'] = row['Price'].translate({ ord(c): None for c in '"฿,'  })


# In[53]:


len(df_new)


# In[54]:


df_new.to_csv('/c/Users/OMEN/airflow/DataPrep/FinalData/JD+Shopee+Lazada.csv',encoding='utf-8-sig',sep=';',index= False)

