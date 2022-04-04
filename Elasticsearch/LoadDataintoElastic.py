
#pip install elasticsearch

from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch(['http://localhost:9200'])

mainindex = "products"
tempindex = "tempindex"
filename = "/c/Users/OMEN/airflow/DataPrep/FinalData/FinalResult.csv"


if es.indices.exists(index=tempindex):
    es.indices.delete(index=tempindex)


es.indices.get_mapping(index=mainindex)

mapping = es.indices.get_mapping(index=mainindex)["products"]
mapping["mappings"].pop("_meta")
setting = es.indices.get_settings(index=mainindex)["products"]
pop_list = ["provided_name","creation_date","uuid","version"]
for t in pop_list:
    setting["settings"]["index"].pop(t)


setting.update(mapping)

es.indices.create(
    index=tempindex,
    body=setting
)

with open(filename,encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, skipinitialspace=True,delimiter=';')
    helpers.bulk(es, reader, index=tempindex)

es.delete_by_query(index=mainindex, body={"query": {"match_all": {}}})

helpers.reindex(es,source_index=tempindex,target_index=mainindex)

es.indices.delete(index=tempindex, ignore=[400, 404])




