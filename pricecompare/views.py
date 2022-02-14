from typing import Match
import math
from django.shortcuts import render
from django.core.paginator import Paginator
from .es_call import *
import json
from django.http import JsonResponse
#from django.http import HttpResponse 
# Create your views here.

def index(request):
    category_all=categoryAll()
    return render(request,'index.html',{'category_all':category_all})

def search_product(request): 
    name = request.GET['name']
    try:
        pf = request.GET['platform']
    except:
        pf = "all"
    try:
        categoryMenu = request.GET['category']
    except:
        categoryMenu = "all"
    try:
        page_num = request.GET['page']
    except:
        page_num = 1

    try:
        sort = request.GET['sort']
    except:
        sort = "relevant"
    sort_name = "ความสอดคล้อง"
    
    if(sort == "asc"):
        # data= sorted(data, key=lambda x: x.data["Price"], reverse=False)
        sort_name = "ราคาต่ำ->ราคาสูง"
    elif(sort == "desc"):
        # data = sorted(data, key=lambda x: x.data["Price"], reverse=True)
        sort_name = "ราคาสูง->ราคาต่ำ"
    elif(sort == "score"):
        # data = sorted(data, key=lambda x: x.data["Score"], reverse=True)
        sort_name = "คะแนนรีวิวสินค้า"

    response = esearch(Name=name,categoryMenu=categoryMenu,Page=page_num,sort=sort,platform=pf)

    data = response['data']
    total = math.ceil(int(response['total'])/60.0)
    if(total>150):
        total = 150
    category_all=categoryAll()
    return render(request,'collection.html',
    {
        'products':data,
        'search_item':name,
        'sort':sort,
        'sort_name':sort_name,
        'category_selected':categoryMenu,
        'page_num':page_num,
        'total':total,
        'category_all':category_all,
        'platform_selected':pf
    })

def product(request,product_id): 
    response = esearchCompare(id=product_id)
    main_product = response[0]
    main_product_url = response[0]["URL"]
    main_product_url = main_product_url.replace('"', "")
    compares = len(response)
    return render(request,'product.html',{'pid':product_id,
            'products':response,
            'main_product':main_product,
            'main_product_url':main_product_url,
            'compares':compares
            })