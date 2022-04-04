settings=$(curl -XGET "https://localhost:9200/test-index/_settings")
mapping=$(curl -XGET "https://localhost:9200/test-index/_mapping")
echo $settings | jq
echo $mapping | jq
cat config.json 

curl -XPUT "http://localhost:9200 /tempindex" -H 'Content-Type: application/json' -d config.json'

curl -XDELETE http://localhost:9200/index

curl -XPOST "http://localhost:9200/_reindex" -H 'Content-Type: application/json' -d'
{
  "source": {
    "index": "tempindex"
  },
  "dest": {
    "index": "index"
  }
}'

curl -XDELETE http://localhost:9200/tempindex