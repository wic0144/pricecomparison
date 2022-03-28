from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Product

@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'jd'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 1
    }
    class Django:
         model = Product
         fields = [
             'Name',
             'Price',
         ]