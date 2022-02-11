from typing import Match
import math
from django.shortcuts import render
from django.core.paginator import Paginator
from .es_call import *
#from django.http import HttpResponse 
# Create your views here.

def index(request):
    return render(request,'index.html')

def search_product(request): 
    name = request.GET['name']
    try:
        categoryMenu = request.GET['collection']
    except:
        categoryMenu = "all"
    #categoryMenu  = request.GET['selectedcategory']
    try:
        page_num = request.GET['page']
    except:
        page_num = 1
        
    try:
        sort = request.GET['sort']
    except:
        sort = "relevant"
    sort_name = "ความสอดคล้อง"
    if(name):
        response = esearch(Name=name,categoryMenu=categoryMenu,Page=page_num)
    else:
        response = esearchAll(categoryMenu=categoryMenu)
 
    if(sort == "asc"):
        response = sorted(response, key=lambda x: x.data["Price"], reverse=False)
        sort_name = "ราคาต่ำ->ราคาสูง"
    elif(sort == "desc"):
        response = sorted(response, key=lambda x: x.data["Price"], reverse=True)
        sort_name = "ราคาสูง->ราคาต่ำ"
    elif(sort == "score"):
        response = sorted(response, key=lambda x: x.data["Score"], reverse=True)
        sort_name = "คะแนนรีวิวสินค้า"
    
 
    
    
    total = math.ceil(int(response['total'])/60)
    return render(request,'collection.html',
    {
        'products':response['data'],
        'search_item':name,
        # 'size':product_paginator.page_range,
        # 'page':page,
        # 'counts':product_paginator.count,
        'sort':sort,
        'sort_name':sort_name,
        'category_selected':categoryMenu,
        'page_num':page_num,
        'total':total
    })

def product_compare(request,product_id): 
    response = esearchCompare(id=product_id)
    main_product_name = response[0]["Name"]
    main_product_price = response[0]["Price"]
    main_product_img = response[0]["Image"]
    main_product_url = response[0]["URL"]
    main_product_url = main_product_url.replace('"', "")
    compares = len(response)
    return render(request,'product_compare.html',{'pid':product_id,
            'products':response,
            'main_product_name':main_product_name,
            'main_product_img':main_product_img,
            'main_product_price':main_product_price,
            'main_product_url':main_product_url,
            'compares':compares
            })