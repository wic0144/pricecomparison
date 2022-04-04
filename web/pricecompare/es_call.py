from unicodedata import name
from django.http import response
from elasticsearch import Elasticsearch 
from elasticsearch_dsl import Search, Q 
from elasticsearch_dsl import UpdateByQuery
db = "products"
dbc = "comparepercentage"
client = Elasticsearch(http_auth=('elastic', 'bM06IvoIFpIsmR8KsoxX'))  
#http_auth=('elastic', 'bM06IvoIFpIsmR8KsoxX')
#ตัว aggregate หา category ทั้งหมดที่ไม่ซ้ำกันที่อยู่ใน db มีจำนวนรวมของข้อมูลของแต่ละ category ด้วย

def currentComparePercentage():
    namepercentage = 0
    thaipercentage = 0
    engpercentage = 0
    response = client.search(
            index=dbc,
            body={
                "size": 1
                }
            )
    for hit in response["hits"]["hits"]:
        namepercentage = hit['_source']['name']
        thaipercentage = hit['_source']['thai']
        engpercentage = hit['_source']['english']
    return [namepercentage,thaipercentage,engpercentage]
def updateComparePercentage(name=0,thai=0,eng=0):
    script = "ctx._source.name ="+str(name)+";ctx._source.english ="+str(eng)+";ctx._source.thai ="+str(thai)

    update_body = {

        "query": {
            "bool": {
                "filter": {
                    "term": {"_id": 1}
                }
            }
        },

        "script": {
            "source": script,
            "lang": "painless"
        }
    }
    finish = client.update_by_query(index=dbc, body=update_body)
    return finish
def categoryAll():      
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


    class CategoryData:
        def _init_(self, data, compareSize):
            self.category = None
            self.total = None
    categoryList=[]
    total = response["hits"]['total']['value']
    
    for hit in response['aggregations']['langs']['buckets']:
        item = CategoryData()
        item.category = hit["key"]
        item.total = hit["doc_count"]
        categoryList.append(item)
    return categoryList 

def categoryCollection(category="",size=10):
    response = client.search(
                index=db,
                body={
                    "track_total_hits":True,
                    "size": size, 
                    "query": {
                        "term": {
                        "Category": {
                            "value": category
                        }
                        }
                    }
                    }
                )

    class CollectionData:
        def init(self, data,id, compareSize):
            self.category = None
            self.collection = []
            self.total = None
    class DataSet:
        def init(self, data,id, compareSize):
            self.data = []
            self.id = None
            self.compareSize = None
    item = CollectionData()
    item.category = category
    item.total = response["hits"]['total']['value']
    dataArraySet = []
    for hit in response["hits"]["hits"]:
        dataset = DataSet()
        dataset.data = hit["_source"]
        dataset.id = hit["_id"]
        dataset.compareSize = len(esearchCompare(id=hit["_id"]))
        dataArraySet.append(dataset)
    item.collection = dataArraySet
    return item
#ตัวค้นหาหลัก
def esearch(Name="",categoryMenu="all",Page=1,sort="relevant",platform="all"):
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


    zero_term_name = "none"
    array_query = []
    if(categoryMenu!="all"):
        array_query.append({"match": {"Category": {"query": categoryMenu}}})
    if(platform!="all"):
        array_query.append({"match": {"Platform": {"query": platform}}})
    if(Name==""):
        zero_term_name = "all"
    array_query.append({"match": {"Name": {"query": Name,"fuzziness": "1","zero_terms_query":zero_term_name}}})

    query_body = {"bool" : { "must": array_query}}
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
    percentage = currentComparePercentage()      
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
                                "minimum_should_match": str(percentage[0]) + "%"
                            }
                            }},
                            {"match":{
                            "thToken":{
                                "query": thToken ,
                                "minimum_should_match": str(percentage[1]) + "%"
                            }

                            }},
                            {"match":{
                                "enToken":{
                                "query": enToken ,
                                "minimum_should_match": str(percentage[2]) + "%"
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
    data_list = sorted(data_list, key=lambda x: x["Price"], reverse=False)
    return data_list

def product_collection_set(size=10,category=""): 
    results = []  
    for hit in response: 
        result_tuple = (hit.Name + ' ' + str(hit.Price))    
        results.append(result_tuple)  
    return results

def get_results(response): 
    results = []  
    for hit in response: 
        result_tuple = (hit.Name + ' ' + str(hit.Price))    
        results.append(result_tuple)  
    return results
