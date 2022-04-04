from contextlib import redirect_stderr
from typing import Match
import math
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .es_call import *
import json
from django.http import JsonResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
#from django.http import HttpResponse 
# Create your views here.
import time
def index(request):
    
    category_all=categoryAll()
    #category_all[0].category จะเอา ชื่อ category นั้น
    #category_all[0].total จะเอาจำนวนของ category นั้น

    collection_list = []
    category_collection1=categoryCollection(category="โทรศัพท์มือถือและแท็บเล็ต",size=15)
    category_collection2=categoryCollection(category="คอมพิวเตอร์และแล็ปท็อป",size=15)
    category_collection3=categoryCollection(category="กล้อง",size=15)
    category_collection4=categoryCollection(category="อุปกรณ์สำหรับเกมเมอร์",size=15)
    collection_list.append(category_collection1)
    collection_list.append(category_collection2)
    collection_list.append(category_collection3)
    collection_list.append(category_collection4)

    #category_collection[0][0].category เอาชื่อ categoryของ collection นั้น
    # #data ของ category ที่ส่งไป อยากได้เท่าไหร่กำหนด size หรือ category เอา
    #ส่วนตัวแปรมีไรบ้างดูใน categoryCollection()

    #print(collection_list[0][0].category) โทรศัพท์มือถือและแท็บเล็ต
    currentPercent=currentComparePercentage()
    namepercent = currentPercent[0]
    thaipercent = currentPercent[1]
    engpercent = currentPercent[2]
    return render(request,'index.html',{'category_all':category_all,'collection_list':collection_list,'category_selected':"all",'platform_selected':"all",'title':'Price Compare IT','thaipercent':thaipercent,'namepercent':namepercent,'engpercent':engpercent})

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
    
    if(sort == "relevant"):
        sort_name="ความสอดคล้อง"
    elif(sort == "asc"):
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
    print(response['total'])
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
        'platform_selected':pf,
        'title':'Search Product'
    })

def product(request,product_id): 
    category_all=categoryAll()
    response = esearchCompare(id=product_id)
    main_product = response[0]
    main_product_url = response[0]["URL"]
    main_product_url = main_product_url.replace('"', "")
    compares = len(response)
    return render(request,'product.html',{'pid':product_id,
            'products':response,
            'main_product':main_product,
            'main_product_url':main_product_url,
            'compares':compares,'category_selected':"all",
            'platform_selected':"all",
            'category_all':category_all,
            'title':'Product Compare'
            })

def todays_deals(request):
    category_all=categoryAll()
    return render(request,'todays-deals.html',{'category_all':category_all,'category_selected':"all",'platform_selected':"all"})\

        
def BI_REPORT(request):
    category_all=categoryAll()
    return render(request,'lookbook.html',{'category_all':category_all,'category_selected':"all",'platform_selected':"all"})

def test(request):
    category_all=categoryAll()
    return render(request,'test.html',{'category_all':category_all,'category_selected':"all",'platform_selected':"all"})

def login(request):
    # username=request.POST['username']
    # password=request.POST['password']
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return redirect('/')
    else:
        messages.success(request,'ชื่อหรือรหัสผ่านไม่ถูกต้อง')
        return redirect('/')

def logout(request):
    # username=request.POST['username']
    # password=request.POST['password']
    auth.logout(request)
    return redirect('/')

def changepercentage(request):
    name =  int(request.POST['name'])
    thai = int(request.POST['thaiword'])
    eng = int(request.POST['engword'])
    
    finish = updateComparePercentage(name,thai,eng)
    print(finish)
    time.sleep(2)
    return redirect('/')