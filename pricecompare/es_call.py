from unicodedata import name
from django.http import response
from elasticsearch import Elasticsearch 
from elasticsearch_dsl import Search, Q 
db = "products"

#ตัว aggregate หา category ทั้งหมดที่ไม่ซ้ำกันที่อยู่ใน db มีจำนวนรวมของข้อมูลของแต่ละ category ด้วย
def categoryAll():      
    client = Elasticsearch()      

    response = client.search(
                index=db,
                body={
                    "size": 0,
                    "aggs" : {
                        "langs" : {
                            "terms" : { "field" : "Category",  "size" : 500 }
                        }
                    }
                    }
                )


    categoryList = []
    for hit in response['aggregations']['langs']['buckets']:
        categoryList.append(hit["key"]) 
    return categoryList  

#ตัวค้นหาหลัก
def esearch(Name="",categoryMenu="",Page=1,sort="relevant",platform=""):
    client = Elasticsearch()
    if(sort=="relevant"):
        field = "_score"
        sort_select = "desc"
    elif(sort=="asc"):
        field = "Price"
        sort_select = "asc"
    elif(sort=="score"):
        field = "Score"
        sort_select = "desc"
    else:
        field = "Price"
        sort_select = "desc"

    if(Name):
         query_body = {"bool" : { "should": [{"match": {"Name": {"query": Name,"fuzziness": "1"}} },{"match": {"Category": categoryMenu}},{"match": {"Platform": platform}}]}}
    else :
        if (categoryMenu=="all" and platform=="all"):
            query_body = {"match_all": {}}
        elif (categoryMenu=="all" or platform=='all'):
            if (categoryMenu!="all" and platform== 'all'):
                query_body = {"bool" : { "should": [{"match": {"Category": categoryMenu}}]}}
            elif (categoryMenu=="all" and platform != 'all'):
                query_body = {"bool" : { "should": [{"match": {"Platform": platform}}]}}
        else:
            query_body = {"bool" : { "should": [{"match": {"Category": categoryMenu}},{"match": {"Platform": platform}}]}}
            

        
        


    # if(categoryMenu=="all" and platform=="all" and Name==""):
    #     query_body = {"match_all": {}}


    # elif(categoryMenu=="all" and platform=="all" and Name!=""):
    #     query_body = {"bool" : 
    #     { "should": 
    #     [{"must": 
    #     {"Name": 
    #     {"query": Name,
    #     "fuzziness": "1"}} }]}}

    # elif (categoryMenu == "all"):
    #     query_body = {"bool" : { "should": [{"match": {"Name": {"query": Name,"fuzziness": "1"}} },{"match": {"Platform": platform}}]}}
    # elif(platform == "all"):
    #     query_body = {"bool" : { "should": [{"match": {"Name": {"query": Name,"fuzziness": "1"}} },{"match": {"Category": categoryMenu}}]}}
    # else:
    #     query_body = {"bool" : { "should": [{"match": {"Name": {"query": Name,"fuzziness": "1"}} },{"match": {"Category": categoryMenu}},{"match": {"Platform": platform}}]}} 
    q_body={
        "from" : (int(Page)-1)*(60), 
        "size" : 60,
        "track_total_hits":True, 
        "query":query_body
        ,
                "sort": [
                {
                    field: {
                        "order": sort_select
                    }
                }
        ]
    }

    response = client.search(index=db,body=q_body)

    class Data:
        def _init_(self, data, compareSize):
            self.data = None
            self.compareSize = None

    data=[]
    total = response["hits"]['total']['value']
    
    for hit in response["hits"]["hits"]:
        item = Data()
        item.id = hit['_id']
        item.data = hit["_source"]
        item.compareSize = len(esearchCompare(id=hit["_id"]))
        data.append(item)

    dataALL = {"data":data,"total":total}       
    return dataALL 
 
#ตัวเปรียบเที่ยบสินค้า
def esearchCompare(id=""):      
    client = Elasticsearch()

    qOne = Q("term", _id=id)
    sOne = Search(using=client, index=db).query(qOne)
    base = sOne.execute()
    if (base[0].thToken=="NULL"):
        thToken = ""
    else:
        thToken = base[0].thToken

    if (base[0].enToken=="NULL"):
        enToken = ""
    else:
        enToken = base[0].enToken

    if (base[0].Category == "NULL"):
        cat = ""
    else:
        cat = base[0].Category
    response = client.search(
                index=db,
                body={
                    "size":5,
                    "query" : {
                        "bool" : { 
                        "must": [
                            {"match":{
                            "Name":{
                                "query": base[0].Name,
                                "minimum_should_match": "70%"
                            }
                            }},
                            {"match":{
                            "thToken":{
                                "query": thToken ,
                                "minimum_should_match": "50%"
                            }

                            }},
                            {"match":{
                                "enToken":{
                                "query": enToken ,
                                "minimum_should_match": "95%"
                                }
                            }},
                            {"match":{
                                "Category":{
                                "query": cat ,
                                "minimum_should_match": "100%"
                                }
                            }}
                        ]
                        }
                    }
                        ,
                    "sort" : [
                        "_score",
                        { "Price" : "asc" },
                        { "Score" : "desc"}
                    ]
                    }
                )
    data_list = []
    for data in response["hits"]["hits"]:
        data_list.append(data["_source"])
    return data_list


def get_results(response): 
    results = []  
    for hit in response: 
        result_tuple = (hit.Name + ' ' + str(hit.Price))    
        results.append(result_tuple)  
    return results
