from django.http import response
from elasticsearch import Elasticsearch 
from elasticsearch_dsl import Search, Q 
db = "product"

def esearchDataSize(Name=""):      
    client = Elasticsearch()      
    q = Q("match", Name=Name)
    s = Search(using=client, index=db).query(q)[0:2000] 

    response = s.execute()
    size = len(response)
    print(size)

    #print('Total %s hits found.' % response.hits.total)   
    #search = get_results(response)        
    return size  

def esearchAll():      
    client = Elasticsearch()
    q = Q("match_all")
    s = Search(using=client, index=db).query(q)[0:100]          

    class Data:
        def _init_(self, data, compareSize):
            self.data = None
            self.compareSize = None

    response = s.execute()

    data = []
    for hit in response:
        item = Data()
        item.data = hit
        item.compareSize = len(esearchCompare(id=hit.meta.id))
        data.append(item)

    #print('Total %s hits found.' % response.hits.total)   
    #search = get_results(response)        
    return data  

def esearch(Name=""):      
    client = Elasticsearch()      
    #q = Q("match", Name=Name, minimum_should_match=0.9)
    # q = Q('bool',
    #     should=[Q('match', Name=Name)],minimum_should_match=1
    # )

    response = client.search(
                index=db,
                body={
                        "size":100,
                        "query": {
                            "match": {
                            "Name": {
                                "query": "Samsung Galaxy Tab A7 Lite 3/32G",
                                "minimum_should_match": "95%"
                            }
                            }
                        }
                    }
                )
    #s = Search(using=client, index=db).query(q)[0:100]

    class Data:
        def _init_(self, data, compareSize):
            self.data = None
            self.compareSize = None

    #response = s.execute()

    print(response["hits"]["hits"][1]["_id"])
    data = []
    for hit in response["hits"]["hits"]:
        item = Data()
        item.data = hit["_source"]
        item.compareSize = len(esearchCompare(id=hit["_id"]))
        data.append(item)
    # data = []
    # for hit in response["hits"]["hits"]:
    #     item = Data()
    #     item.data = hit["_source"]
    #     item.compareSize = len(esearchCompare(id=hit.meta.id))
    #     data.append(item)

    #print('Total %s hits found.' % response.hits.total)   
    #search = get_results(response)       
    return data  

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
        enToken = base[0].enToken
    else:
        enToken = base[0].enToken        
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
