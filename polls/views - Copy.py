from django.http import HttpResponse
from mysite.settings import DATABASES
from .models import Loadtypes
from django.shortcuts import render
from django.template import loader
from django.views.generic import ListView
from django.http import JsonResponse
import random
import pyodbc
import datetime
import jdatetime
import serial
import json
import sys
import base64
import os
from random import randint
from django.views.decorators.csrf import csrf_exempt
import time

CURRENT_WEIGHT = 0
WEIGHTS = {}
LASTWIGHTSDATE = {}
LASTEDITED = time.time()


def getweightfromclient(request,token,weight):
    global CURRENT_WEIGHT

    if request.method == 'GET':

        CURRENT_WEIGHT = weight
        WEIGHTS.setdefault(token,[]).append(weight)
        if len(WEIGHTS[token])==5:
            del WEIGHTS[token][0]
        LASTWIGHTSDATE[token] = time.time()
    return JsonResponse(WEIGHTS)

def stuff(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
   
    x = CURRENT_WEIGHT
    try:
        if (time.time() - LASTWIGHTSDATE[ip]) < 3:
            if len(set(WEIGHTS[ip]))==1:
                weight = WEIGHTS[ip][-1]
                return JsonResponse({'status':'true','msg': weight})
            else:
                weight = WEIGHTS[ip][-1]
                return JsonResponse({'status':'false','msg': weight})                
        else:
            return JsonResponse({'status':'false','msg':'باسکول قطع است!'})
    except: 
        weight = 0
        return JsonResponse({'status':'false','msg':'باسکول قطع است!'})

def lastedited(request):
    now = time.time()
    if (now - LASTEDITED) < 2:
        return JsonResponse({'reload': True})
    else:
        return JsonResponse({'reload': False})

def write_to_DB(conn,query_string, data, tbl):

    cursor = conn.cursor()
    
    #print ("executing Query")
    for i,row in enumerate(data):
        for j,itm in enumerate(row):
            if type(itm) == bytes or type(itm)==bytearray:
                ls = list(data[i])
                ls[j] = itm.decode('utf-8')
                tp = tuple(ls)
                data[i] = tp
            if type(itm) == datetime.date:
                ls = list(data[i])
                ls[j] = str(itm)
                tp = tuple(ls)
                data[i] = tp
              
    if len(data) > 0:
        
        for itm in data:
            #tpl = tuple([x for x in itm])
            cursor.execute(query_string, itm)
        cursor.commit()

def index(request):
    latest_question_list = [1,2]#Loadtypes.objects.order_by('-type')[:5]
    template = loader.get_template('polls/public/index_scrach.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def report_page(request):
    latest_question_list = [1,2]#Loadtypes.objects.order_by('-type')[:5]
    template = loader.get_template('polls/public/reports.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def print_page(request,carid,nationalid,reciept):
    image_path = 'polls/static/IDphotos/' + nationalid
    
    if os.path.isfile(image_path + '.jpg'):
        image_path = image_path + '.jpg'
    elif os.path.isfile(image_path + '.png'):
        image_path = image_path + '.png'
    elif os.path.isfile(image_path + '.jpeg'):
        image_path = image_path + '.jpeg'
    else:
        image_path = "polls/static/IDphotos/notfound.jpg"

    #image_path = 'polls/static/IDphotos/' + nationalid + '.jpg' #os.path.join("static/IDphotos",nationalid + '.jpg')
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

        
    ctx = {}
    ctx["image"] = image_data
    
    return render(request, 'polls/public/print_raw.html', ctx)

def edit_page(request,carid,nationalid,reciept):
    return render(request, 'polls/public/editloads.html')

def fastresults_page(request):
    return render(request, 'polls/public/fastresults.html')

def getfastresults(request,id,carid,name):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query_string =  "select distinct NationalID, FirstName, LastName,  "
    cursor.execute(query_string)
    
    data = []
    for row in cursor.fetchall():
        d = {}
        d['vnumber'] = str(row[0])
        d['nationalid'] = str(row[1])
        d['loadedweight'] = str(row[2])
        d['unloadedweight'] = str(row[3])
        d['loaddateshamsi'] = str(row[4])
        
        data.append(d)
    
    return JsonResponse(json.dumps(data),safe=False)
    
def chart_page(request):
    latest_question_list = [1,2]#Loadtypes.objects.order_by('-type')[:5]
    template = loader.get_template('polls/public/chartjs.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def autocarnumber(request):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query_string = "select distinct a.VehicleNumber from (select vehicleNumber from temp_loadings union select  vehicleNumber from InLoadings union select vehicleNumber from OutLoadings) a"

    cursor.execute(query_string)
    
    try:
        results = cursor.fetchall()
        numbers = [x[0] for x in results]
 
        new_id = randint(10,99)
        new_num = randint(100,999)
        char = 'ت'
        
        if len(results) > 80000:
            char = 'خ'
        if len(results) > 160000:
            char = 'ف'
        
        carid = str(new_id) + char + str(new_num)
        while (carid) in numbers:
            new_id = str(randint(10,99))
            new_num = str(randint(100,999))
            carid = str(new_id) + char + str(new_num)
        
        return JsonResponse({"id": new_id,"number":new_num,"char":char})
    except:
        new_id = '10'
        new_num = '100'
        char = 'ت'
        return sonResponse({"id": new_id,"number":new_num,"char":char})

def oautocarnumber(request):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query_string = "select distinct a.VehicleNumber from (select vehicleNumber from OtherLoadings) a"

    cursor.execute(query_string)
    
    try:
        results = cursor.fetchall()
        numbers = [x[0] for x in results]
 
        new_id = randint(10,99)
        new_num = randint(100,999)
        char = 'ت'
        
        if len(results) > 80000:
            char = 'خ'
        if len(results) > 160000:
            char = 'ف'
        
        carid = str(new_id) + char + str(new_num)
        while (carid) in numbers:
            new_id = str(randint(10,99))
            new_num = str(randint(100,999))
            carid = str(new_id) + char + str(new_num)
        
        return JsonResponse({"id": new_id,"number":new_num,"char":char})
    except:
        new_id = '10'
        new_num = '100'
        char = 'ت'
        return sonResponse({"id": new_id,"number":new_num,"char":char})

def searchid(request, id):
    
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query_string ="""select NationalID, NationalID, FirstName, LastName, BankAccount, Mobile,FathersName from dbo.Suppliers where NationalID = '{}' 
                     UNION
                     select CustomerID, CustomerID, FirstName, LastName, BankAccount, Mobile,FathersName from dbo.Customers where CustomerID = '{}' """.format(id,id)

    cursor.execute(query_string)
    results = cursor.fetchall()
    

    data = {}
    for row in results:
        data['customernumber'] = row[1]
        data['firstname'] = row[2]
        data['lastname'] = row[3]
        data['mobile'] = row[5]
        data['bank'] = row[4]
        data['fathername'] = row[6]

    if len(data)>0:
        query_string = "select CustomerID, VehicleNumber from dbo.InLoadings where CustomerID = '{}' ".format(data['customernumber'])
        cursor.execute(query_string)
        res = cursor.fetchall()
        if len(res)==0:
            query_string = "select CustomerID, VehicleNumber from dbo.OutLoadings where CustomerID = '{}' ".format(data['customernumber'])
            cursor.execute(query_string)
            res = cursor.fetchall()            
        try:
            vnumber = res[0][1]#.split(' ')
        except:
            vnumber = " "

        
        idx1 = vnumber.index('(')
        idx2 = vnumber.index(')')

        data['vletter'] = vnumber[idx2 + 4]
        data['vcode'] = vnumber[idx2+1:idx2+4]
        data['vid'] = vnumber[idx2+5:]
        data['vregion'] = vnumber[idx1+1:idx2]


        return JsonResponse(data)
    else:
        return JsonResponse({'status':'false','message':'Not Found!'}, status=500)

def initlocations(request):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query = "select village from Villages"
    cursor.execute(query)
    
    villages = []
    for itm in cursor.fetchall():
        if itm not in villages:
            villages.append(itm[0])
            
    query = "select address from Customers"
    cursor.execute(query)

    for itm in cursor.fetchall():
        if itm not in villages:
            villages.append(itm[0])
    
    data = {'villages': villages}
    return JsonResponse(json.dumps(data),safe=False)
    
def initnames(request):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query = "select FirstName, LastName from Suppliers "
    cursor.execute(query)
    
    names = []
    for itm in cursor.fetchall():
        if itm not in names:
            names.append(itm[0] + '|' + itm[1])
            
    query = "select FirstName, LastName from Customers"
    cursor.execute(query)

    for itm in cursor.fetchall():
        if itm not in names:
            names.append(itm[0] + '|' + itm[1])
    
    data = {'names': names}
    return JsonResponse(json.dumps(data),safe=False)

def initialization(request):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query = "select Type from VehiclesTypes"
    cursor.execute(query)
    
    cars = []
    for itm in cursor.fetchall():
        cars.append(itm[0])
        
    query = "select Type from LoadTypes"
    cursor.execute(query)
    
    loads = []
    for itm in cursor.fetchall():
        loads.append(itm[0])

    data = {'cars': cars, 'loads': loads}
    return JsonResponse(json.dumps(data),safe=False)

def dailystatistics(request):

    results = {}
    now = datetime.datetime.now()
    shamsi=jdatetime.datetime.fromgregorian(datetime=now)
    shamsi = str(shamsi).split(' ')[0]
    shamsi = shamsi.replace('-','/')
    
    
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query1 = "select count(distinct(InvoiceNumber)) from dbo.InLoadings where SUBSTRING(EnterDateShamsi,1,10) = '{}' and Deleted=0".format(shamsi)
    query2 = "select count(distinct(InvoiceNumber)) from dbo.OutLoadings where SUBSTRING(ExitDateShamsi,1,10) = '{}' and Deleted=0 ".format(shamsi)
    query3 = "select sum(PureWeight) from dbo.InLoadings where SUBSTRING(EnterDateShamsi,1,10) = '{}' and Deleted=0".format(shamsi)
    query4 = "select sum(PureWeight) from dbo.OutLoadings where SUBSTRING(ExitDateShamsi,1,10) = '{}' and Deleted=0".format(shamsi)

    cursor.execute(query1)
    re = cursor.fetchall()
    results['inputinvoices'] = re[0][0]
    
    cursor.execute(query2)
    re = cursor.fetchall()
    results['outputinvoices'] = re[0][0]
    
    cursor.execute(query3)
    re = cursor.fetchall()
    results['suminweight'] = re[0][0]
    
    cursor.execute(query4)
    re = cursor.fetchall()
    
    results['sumoutweight'] = re[0][0]
    for key in results:
        if results[key] == None:
            results[key] = 0;
    return JsonResponse(results)

@csrf_exempt
def temp_as_full(request):
    if request.method=="POST":
        
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])

        data = json.loads(request.body)
        id = data['ID']
        fname = data['Fname']
        lname = data['Lname']
        faname = data['Faname']
        mobile = data['Mobile']
        bankacc = data['Bankacc']
        driver =  data['Driver']
        vnumber = data['Vnumber']
        ltype = data['Ltype']
        vtype = data['Vtype']
        fweight = data['Fweight']
        location = data['Location']

        now = datetime.datetime.now()
        shamsi=jdatetime.datetime.fromgregorian(datetime=now)
        
        shamsi = str(shamsi).split(' ')[0]
        
        year, month, day = shamsi.split('-')
        hour, minute, second = str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)
        dateshamsi = year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second
        
        
        
        query = """insert into temp_loadings(EnterDate ,EnterDateShamsi ,Driver ,VehicleNumber ,CustomerID ,FirstName ,LastName ,Mobile ,FatherName ,BanckAccount ,LoadedWeight ,LoadType ,VehicleType, Location) 
        values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        result = ""
        write_to_DB(conn,query, [(now,dateshamsi,driver,vnumber,id,fname,lname,mobile,faname,bankacc,fweight,ltype,vtype, location)],'temp_loadings')
        try:
            
            result = "successfull"
        except:
            e = sys.exc_info()[0]
            print (e)
            result = "failed"
    return JsonResponse({'msg':result})
    
@csrf_exempt
def temp_as_empty(request):
    if request.method=="POST":
        
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])

        data = json.loads(request.body)
        id = data['ID']
        fname = data['Fname']
        lname = data['Lname']
        faname = data['Faname']
        mobile = data['Mobile']
        bankacc = data['Bankacc']
        driver =  data['Driver']
        vnumber = data['Vnumber']
        ltype = data['Ltype']
        vtype = data['Vtype']
        fweight = data['Fweight']
        location = data['Location']

        now = datetime.datetime.now()
        shamsi=jdatetime.datetime.fromgregorian(datetime=now)
        
        shamsi = str(shamsi).split(' ')[0]
        
        year, month, day = shamsi.split('-')
        hour, minute, second = str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)
        dateshamsi = year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second
        
        
        
        query = """insert into temp_loadings(EnterDate ,EnterDateShamsi ,Driver ,VehicleNumber ,CustomerID ,FirstName ,LastName ,Mobile ,FatherName ,BanckAccount ,UnLoadedWeight ,LoadType ,VehicleType, Location) 
        values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        result = ""
        write_to_DB(conn,query, [(now,dateshamsi,driver,vnumber,id,fname,lname,mobile,faname,bankacc,fweight,ltype,vtype, location)],'temp_loadings')
        try:
            
            result = "successfull"
        except:
            e = sys.exc_info()[0]
            print (e)
            result = "failed"
    return JsonResponse({'msg':result})


@csrf_exempt
def oregister(request):
    if request.method=="POST":
        
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])

        data = json.loads(request.body)
        id = data['ID']
        fname = data['Fname']
        vnumber = data['Vnumber']
        ltype = data['Ltype']
        vtype = data['Vtype']
        fweight = data['Fweight']
        sweight = data['Sweight']
        location = data['Location']
        
        try:
            x = int(sweight)
        except:
            sweight = 0;
        now = datetime.datetime.now()
        shamsi=jdatetime.datetime.fromgregorian(datetime=now)
        
        shamsi = str(shamsi).split(' ')[0]
        
        year, month, day = shamsi.split('-')
        hour, minute, second = str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)
        dateshamsi = year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second
        
        
        
        query = """insert into OtherLoadings(EnterDate ,EnterDateShamsi ,VehicleNumber ,CustomerID ,FirstName ,LoadedWeight ,UnLoadedWeight ,LoadType ,VehicleType, Location) 
        values(?,?,?,?,?,?,?,?,?,?)"""
        result = ""
        write_to_DB(conn,query, [(now,dateshamsi,vnumber,id,fname,fweight,sweight,ltype,vtype,location)],'OtherLoadings')
        try:
            
            result = "successfull"
        except:
            e = sys.exc_info()[0]
            print (e)
            result = "failed"
    return JsonResponse({'msg':result})

@csrf_exempt
def delete_from_temps(request):
    global LASTEDITED
    if request.method == "POST":
        loads = json.loads(request.body)
        data = loads['id']
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
        cursor = conn.cursor()
        query = "delete from temp_loadings where VehicleNumber=N'{}' ".format(data)

        result = ""
        try:
            cursor.execute(query)
            cursor.commit()
            conn.close()
            result = "باسکول با موفقیت حذف گردید"
            LASTEDITED = time.time()
            return JsonResponse({'msg': result})
        except:
            result = "failed"
            return JsonResponse({'status':'false','msg':'خطا در دسترسی به پایگاه داده. لطفا صفحه را ببندید و مجددا اقدام بفرمایید'})

@csrf_exempt
def delete_full_invoice(request):
    global LASTEDITED
    if request.method == "POST":
        loads = json.loads(request.body)
        data = loads['id']
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
        cursor = conn.cursor()
        if data.startswith('1'):
            #query = "delete from InLoadings where InvoiceNumber='{}' ".format(data)
            query = "update InLoadings set Deleted=1 where InvoiceNumber='{}' ".format(data)
        elif data.startswith('2'):
            #query = "delete from OutLoadings where InvoiceNumber='{}' ".format(data)
            query = "update OutLoadings set Deleted=1 where InvoiceNumber='{}' ".format(data)
        else:
            return JsonResponse({'status':'false','msg':'شماره فاکتور نامعتبر است. لطفا صفحه را ببندید و مجددا اقدام بفرمایید'})

        result = ""
        try:
            cursor.execute(query)
            cursor.commit()
            conn.close()
            result = "باسکول با موفقیت حذف گردید"
            LASTEDITED = time.time()
            return JsonResponse({'msg': result})
        except:
            return JsonResponse({'status':'false','msg':'خطا در دسترسی به پایگاه داده. لطفا صفحه را ببندید و مجددا اقدام بفرمایید'})

def register_temp_edits(request):
    global LASTEDITED
    if request.method=="POST":
        
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])

        data = json.loads(request.body)
        id = data['ID']
        fname = data['Fname']
        lname = data['Lname']
        faname = data['Faname']
        mobile = data['Mobile']
        bankacc = data['Bankacc']
        driver =  data['Driver']
        vnumber = data['Vnumber']
        ltype = data['Ltype']
        vtype = data['Vtype']
        location = data['Location']
        loadedweight = data['loadedweight']
        unloadedweight = data['unloadedweight']
        if len(str(loadedweight).strip())>0:
            column = "LoadedWeight"
            value = loadedweight
        if len(str(unloadedweight).strip())>0:
            column = "UnLoadedWeight"
            value = unloadedweight
        
        now = datetime.datetime.now()
        shamsi=jdatetime.datetime.fromgregorian(datetime=now)
        
        shamsi = str(shamsi).split(' ')[0]
        
        year, month, day = shamsi.split('-')
        hour, minute, second = str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)
        dateshamsi = year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second
        

        query = """
        update temp_loadings set CustomerID='{}', Driver=N'{}', VehicleNumber=N'{}', FirstName=N'{}', LastName=N'{}', Mobile='{}', FatherName=N'{}', BanckAccount='{}', {}={}, LoadType=N'{}', VehicleType=N'{}', Location=N'{}' where VehicleNumber=N'{}'
        """.format(id,driver,vnumber,fname,lname,mobile,faname,bankacc,column,value,ltype,vtype,location,vnumber)
        result = ""

        try:
            curs = conn.cursor()
            curs.execute(query)
            curs.commit()
            result = "تغییرات با موفقیت ثبت گردید. جهت مشاهده صفحه را بازیابی کنید"
            LASTEDITED = time.time()
        except:
            e = sys.exc_info()[0]
            print (e)
            result = "ثبت تغییرات با خطا مواجه شد. لطفا صفحه را ببندید و مجددا تلاش کنید"
    return JsonResponse({'msg':result})

def register_full_edits(request):
    global LASTEDITED
    if request.method=="POST":
        
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
        cursor = conn.cursor()
        data = json.loads(request.body)
        reciept = data['Reciept']
        id = data['ID']
        fname = data['Fname']
        lname = data['Lname']
        faname = data['Faname']
        mobile = data['Mobile']
        bankacc = data['Bankacc']
        driver =  data['Driver']
        vnumber = data['Vnumber']
        ltype = data['Ltype']
        vtype = data['Vtype']
        location = data['Location']
        loadedweight = data['loadedweight']
        unloadedweight = data['unloadedweight']

        now = datetime.datetime.now()
        shamsi=jdatetime.datetime.fromgregorian(datetime=now)
        
        shamsi = str(shamsi).split(' ')[0]
        
        year, month, day = shamsi.split('-')
        hour, minute, second = str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)
        dateshamsi = year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second

        loadtypeid, cartypeid = get_types_ids(conn, ltype,vtype)

        if not len(str(loadedweight).strip())>0:
            return JsonResponse({'status':'false','msg':'مقدار وزن پر صحیح نمی باشد'})        
        if not len(str(unloadedweight).strip())>0:
            return JsonResponse({'status':'false','msg':'مقدار وزن خالی صحیح نمی باشد'})
        if float(str(loadedweight).strip()) <  float(str(unloadedweight).strip()):
            return JsonResponse({'status':'false','msg':'وزن پر نمیتواند از وزن خالی کوچکتر باشد'})        
        
        if reciept.startswith('1'):            
            query = """      
            if not exists(select * from Suppliers where NationalID='{}') 
            insert into dbo.Suppliers(NationalID,FirstName,LastName,FathersName,BankAccount,Mobile,CreateDate) 
            values('{}',N'{}',N'{}',N'{}','{}','{}',GETDATE())
            else update Suppliers set 
            FirstName=N'{}', LastName=N'{}', FathersName=N'{}',BankAccount='{}', Mobile='{}', ModifiedDate=GETDATE() where NationalID='{}'    
            """.format(id,id,fname,lname,faname,bankacc,mobile,fname,lname,faname,bankacc,mobile,id)
            cursor.execute(query)
            cursor.commit()
                
            query = """      
            Update InLoadings set 
            Driver=N'{}' ,VehicleNumber=N'{}' ,CustomerID='{}' ,LoadedWeight={} ,UnloadedWeight={} ,
            PureWeight={} ,LoadType=N'{}' ,VehicleType=N'{}', Location=N'{}', ModifiedDate = GETDATE() where InvoiceNumber='{}'
            """.format(driver,vnumber,id,loadedweight,unloadedweight,float(loadedweight)-float(unloadedweight),loadtypeid,cartypeid,location,reciept)
            cursor.execute(query)
            cursor.commit()
            LASTEDITED = time.time()
            return JsonResponse({'msg':'تغییرات با موفقیت ثبت گردید. جهت مشاهده صفحه را مجددا بارگزاری کنید'})                
        elif reciept.startswith('2'):
            query = """      
            if not exists(select * from Customers where CustomerID='{}') 
            insert into dbo.Customers(CustomerID,FirstName,LastName,FathersName,BankAccount,Mobile,CreateDate) 
            values('{}',N'{}',N'{}',N'{}','{}','{}',GETDATE())
            else update Customers set 
            FirstName=N'{}', LastName=N'{}', FathersName=N'{}',BankAccount='{}', Mobile='{}', ModifiedDate=GETDATE() where CustomerID='{}'    
            """.format(id,id,fname,lname,faname,bankacc,mobile,fname,lname,faname,bankacc,mobile,id)
            cursor.execute(query)
            cursor.commit()
                
            query = """      
            Update OutLoadings set 
            Driver=N'{}' ,VehicleNumber=N'{}' ,CustomerID='{}' ,LoadedWeight={} ,UnloadedWeight={} ,
            PureWeight={} ,LoadType=N'{}' ,VehicleType=N'{}', Location=N'{}', ModifiedDate = GETDATE() where InvoiceNumber='{}'
            """.format(driver,vnumber,id,loadedweight,unloadedweight,float(loadedweight)-float(unloadedweight),loadtypeid,cartypeid,location,reciept)
            cursor.execute(query)
            cursor.commit()
            LASTEDITED = time.time()
            return JsonResponse({'msg':'تغییرات با موفقیت ثبت گردید. جهت مشاهده صفحه را مجددا بارگزاری کنید'})
        else:
            return JsonResponse({'status':'false','msg':'شماره فاکتور نامعتبر است. لطفا صفحه را ببندید و مجددا اقدام بفرمایید'})        

def read_temp_loadings(request):
    
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query_string =  "select VehicleNumber, CustomerID, LoadedWeight, UnloadedWeight, EnterDateShamsi from dbo.temp_loadings "
    cursor.execute(query_string)
    
    data = []
    for row in cursor.fetchall():
        d = {}
        d['vnumber'] = str(row[0])
        d['nationalid'] = str(row[1])
        d['loadedweight'] = str(row[2])
        d['unloadedweight'] = str(row[3])
        d['loaddateshamsi'] = str(row[4])
        
        data.append(d)
    
    return JsonResponse(json.dumps(data),safe=False)

def get_types_ids(conn, load, car):
    curs = conn.cursor()
    query = "select ID from LoadTypes where Type = N'{}' ".format(load)
    curs.execute(query)
    result = curs.fetchall()
    id_load = result[0][0]
    
    query = "select ID from VehiclesTypes where Type = N'{}'".format(car)
    curs.execute(query)
    result = curs.fetchall()
    id_car = result[0][0]
    
    return id_load, id_car

def get_next_invoice(conn,table):        
    now = datetime.datetime.now()
    shamsi=jdatetime.datetime.fromgregorian(datetime=now)
    shamsi = str(shamsi).split(' ')[0]
    year, month, day = shamsi.split('-')
    cursor = conn.cursor()
    query = "select InvoiceNumber from {} where ExitDate = (select max(ExitDate) from {})".format(table,table)
  
    cursor.execute(query)
    results = cursor.fetchall()
    try:
        lastinvoice = results[0][0]
  
        counter = str(int(lastinvoice[8:])+1).zfill(5)
    
        if lastinvoice[1:7] == (year[2:]+month+day):
            nextinvoice = lastinvoice[:7] + counter
        else:
            nextinvoice = lastinvoice[0] + year[2:] + month + day + '00000'
    except:
        if table == 'InLoadings':
            nextinvoice = '1' + year[2:] + month + day + '00000'
        else:
            nextinvoice = '2' + year[2:] + month + day + '00000'
    
    return nextinvoice

@csrf_exempt
def register(request):
    
    postdata = {}
    if request.method == "POST":
        loads = json.loads(request.body)
        data = loads['vnumber']
        weight = loads['weight']
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
        cursor = conn.cursor()
        query = """select ID,CAST(EnterDate as VARCHAR),EnterDateShamsi,Driver,VehicleNumber,CustomerID,FirstName,LastName,Mobile,FatherName,BanckAccount,CAST(LoadedWeight as FLOAT),CAST(UnloadedWeight as FLOAT),LoadType,VehicleType,Location
        from temp_loadings where VehicleNumber=N'{}' 
        """.format(data)
        cursor.execute(query)
        
        results = cursor.fetchall()
        

        for row in results:
            loaddate = row[1]
            loaddateshamsi = row[2]
            driver = row[3]
            car = row[4]
            postdata['carid'] = car
            customerid = row[5]
            postdata['id'] = customerid
            firstname = row[6]
            lastname = row[7]
            mobile = row[8]
            fathername = row[9]
            bankacc = row[10]
            loadedweight = row[11]
            unloadedweight = row[12]
            loadtype = row[13]
            cartype = row[14]
            location = row[15]

            loadtypeid, cartypeid = get_types_ids(conn, loadtype,cartype)

            table = ""
            if loadedweight == None:
                table = "OutLoadings"
                loadedweight = float(weight)#CURRENT_WEIGHT
            if unloadedweight == None:
                table = "InLoadings"
                unloadedweight = float(weight)#CURRENT_WEIGHT

            if loadedweight < unloadedweight:
                return JsonResponse({'status':'false','msg':'باسکول نامعتبر است. وزن پر نمیتواند کوچک تر از وزن خالی باشد. لطفا تنظیمات را بررسی بفرمایید'}) 
                
            if table=="InLoadings":#loadedweight >= unloadedweight:
                #table = "InLoadings"
                query = """
                
                  if not exists(select * from Suppliers where NationalID='{}') 
                      insert into dbo.Suppliers(NationalID,FirstName,LastName,FathersName,BankAccount,Mobile,CreateDate) 
                      values('{}',N'{}',N'{}',N'{}','{}','{}',GETDATE())
                  else update Suppliers set FirstName=N'{}', LastName=N'{}', FathersName=N'{}',BankAccount='{}', Mobile='{}', ModifiedDate=GETDATE() where NationalID='{}'
                
                """.format(customerid,customerid,firstname,lastname,fathername,bankacc,mobile,firstname,lastname,fathername,bankacc,mobile,customerid)
                
                cursor.execute(query)
                cursor.commit()
            elif table=="OutLoadings":#unloadedweight > loadedweight:
                #table = "OutLoadings"
                
                query = """
                
                  if not exists(select * from Customers where CustomerID='{}') 
                      insert into dbo.Customers(CustomerID,FirstName,LastName,FathersName,BankAccount,Mobile,CreateDate) 
                      values('{}',N'{}',N'{}',N'{}','{}','{}',GETDATE())
                  else update Customers set FirstName=N'{}', LastName=N'{}', FathersName=N'{}',BankAccount='{}', Mobile='{}', ModifiedDate=GETDATE() where CustomerID='{}'
                
                """.format(customerid,customerid,firstname,lastname,fathername,bankacc,mobile,firstname,lastname,fathername,bankacc,mobile,customerid)
                cursor.execute(query)
                cursor.commit()
                
                
            invoicenum = get_next_invoice(conn,table)
            postdata['reciept'] = invoicenum
            
            now = datetime.datetime.now()
            shamsi=jdatetime.datetime.fromgregorian(datetime=now)
        
            shamsi = str(shamsi).split(' ')[0]
        
            year, month, day = shamsi.split('-')
            hour, minute, second = str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)
            dateshamsi = year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second


            query = """insert into {}(InvoiceNumber ,EnterDate ,EnterDateShamsi, ExitDate, ExitDateShamsi ,Driver ,VehicleNumber ,CustomerID ,LoadedWeight ,UnloadedWeight ,PureWeight ,LoadType ,VehicleType, Location, CreateDate, ModifiedDate) 
                    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""".format(table)
            
           
            data = [(invoicenum,str(loaddate),loaddateshamsi,now,dateshamsi,driver,car,customerid,loadedweight,unloadedweight,abs(loadedweight-unloadedweight),loadtypeid,cartypeid, location, now, now)]
 
            write_to_DB(conn,query,data,table)
            
            query = "delete from temp_loadings where VehicleNumber=N'{}' ".format(car)
          
            cursor.execute(query)
            cursor.commit()
            
    return JsonResponse(postdata)

@csrf_exempt
def report_search(request):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    cursor = conn.cursor()    

    data = json.loads(request.body)
    id = data['ID']
    invoice = data['Invoice']
    fname = data['Fname']
    lname = data['Lname']
    driver =  data['Driver']
    vnumber = data['Vnumber']
    ltype = data['Ltype']
    vtype = data['Vtype']
    inout = data['InOut']
    date1 = data['Date1']
    date2 = data['Date2']

    now = datetime.datetime.now()
    shamsi=jdatetime.datetime.fromgregorian(datetime=now)
    shamsi = str(shamsi).split(' ')[0]
    shamsi = shamsi.replace('-','/')

    if len(date1)>0:
        date1_s = date1.split('-')
        if len(date1_s)==3 and len(date1_s[0])==4 and len(date1_s[1])==2 and len(date1_s[2])==2:
            date1 = date1 + ' 00:00:00'
        else:
            return JsonResponse({'status':'false','msg':'فرمت تاریخ صحیح نمی باشد'})
    else:
        date_s = ''
    if len(date2)>0:
        date2_s = date2.split('-')
        if len(date2_s)==3 and len(date2_s[0])==4 and len(date2_s[1])==2 and len(date2_s[2])==2:
            date2 = date2 + ' 23:59:59'
        else:
            return JsonResponse({'status':'false','msg':'فرمت تاریخ صحیح نمی باشد'})


    if inout == "بار ورودی":
        table = "InLoadings"
    elif inout == "بار خروجی":
        table = "OutLoadings"
        
    filter_string = ""
    if len(date1)>0 and len(date2)>0:
        filter_string += " (EnterDateShamsi between '{}' and '{}')".format(date1, date2)
    elif len(date1)>0:
        filter_string += " AND EnterDateShamsi='{}'".format(date1)
    elif len(date2)>0:
        filter_string += " AND EnterDateShamsi='{}'".format(date2)

    if len(invoice)>0:
        filter_string += " AND InvoiceNumber='{}'".format(invoice)

    if len(id)>0:
        filter_string += " AND CustomerID='{}'".format(invoice)

    if len(fname)>0:
        filter_string += " AND FirstName= N'{}'".format(fname)
    
    if len(lname)>0:
        filter_string += " AND LastName= N'{}'".format(lname)
        
    if len(driver)>0: 
        filter_string += " AND Driver= N'{}'".format(driver)

    if len(vnumber)>2:
        filter_string += " AND VehicleNumber= N'{}'".format(vnumber)

    if len(ltype)>0:
        loadtypeid, cartypeid = get_types_ids(conn, ltype, vtype)
        filter_string += " AND LoadType={}".format(loadtypeid)

    if len(vtype)>0:
        loadtypeid, cartypeid = get_types_ids(conn, ltype,vtype)
        filter_string += " AND VehicleType={} ".format(cartypeid)
        
    query=""
    if table=="InLoadings":
        query = """
        select CONCAT(FirstName,' ', LastName), InvoiceNumber, Driver,VehicleNumber,CustomerID,LoadedWeight,UnLoadedWeight,EnterDateShamsi, ExitDateShamsi, ExitDate 
        from InLoadings I join Suppliers S on I.CustomerID=S.NationalID 
        where {} and Deleted=0 order by ExitDate Desc
        """.format(filter_string)
        query = query.replace('where AND', 'where ')
        query = query.replace('where  AND', 'where ')

    if table=="OutLoadings":

        query = """
        select CONCAT(FirstName,' ', LastName), InvoiceNumber,Driver, VehicleNumber,O.CustomerID ,LoadedWeight,UnLoadedWeight,EnterDateShamsi, ExitDateShamsi, ExitDate 
        from OutLoadings O join Customers C on O.CustomerID=C.CustomerID 
        where {} and Deleted=0 order by ExitDate Desc
        """.format(filter_string)
        query = query.replace('where AND', 'where ')
        query = query.replace('where  AND', 'where ')

    cursor.execute(query)
    result = cursor.fetchall()

    data = []
    for row in result:
        d = {}
        d['name'] = str(row[0])
        d['reciept'] = str(row[1])
        d['driver'] = str(row[2])
        d['vnumber'] = str(row[3])
        d['customerid'] = str(row[4])
        d['loadedweight'] = str(row[5])
        d['unloadedweight'] = str(row[6])
        d['enterdate'] = str(row[7])
        d['exitdate'] = str(row[8])
        
        data.append(d)

    return JsonResponse(json.dumps(data),safe=False)

@csrf_exempt
def group_report_search(request):
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    cursor = conn.cursor()    

    data = json.loads(request.body)

    ltype = data['Ltype']
    inout = data['InOut']
    date1 = data['Date1']
    date2 = data['Date2']
    grouptype = data['Type']

    now = datetime.datetime.now()
    shamsi=jdatetime.datetime.fromgregorian(datetime=now)
    shamsi = str(shamsi).split(' ')[0]
    shamsi = shamsi.replace('-','/')

    if len(date1)>0:
        date1_s = date1.split('-')
        if len(date1_s)==3 and len(date1_s[0])==4 and len(date1_s[1])==2 and len(date1_s[2])==2:
            date1 = date1 + ' 00:00:00'
        else:
            return JsonResponse({'status':'false','msg':'فرمت تاریخ صحیح نمی باشد'})
    else:
        date_s = ''
    if len(date2)>0:
        date2_s = date2.split('-')
        if len(date2_s)==3 and len(date2_s[0])==4 and len(date2_s[1])==2 and len(date2_s[2])==2:
            date2 = date2 + ' 23:59:59'
        else:
            return JsonResponse({'status':'false','msg':'فرمت تاریخ صحیح نمی باشد'})


    if inout == "بار ورودی":
        table = "InLoadings"
    elif inout == "بار خروجی":
        table = "OutLoadings"
        
    filter_string = ""
    if len(date1)>0 and len(date2)>0:
        filter_string += " (EnterDateShamsi between '{}' and '{}')".format(date1, date2)
    elif len(date1)>0:
        filter_string += " AND EnterDateShamsi='{}'".format(date1)
    elif len(date2)>0:
        filter_string += " AND EnterDateShamsi='{}'".format(date2)

    if len(ltype)>0:
        loadtypeid, cartypeid = get_types_ids(conn, ltype, 'تراکتور')
        filter_string += " AND LoadType={}".format(loadtypeid)


    group_len = None

    if grouptype=="daily":
        group_len=10

    if grouptype=="monthly":
        group_len=7

    query=""
    if table=="InLoadings":
        query = """
        select SUBSTRING(EnterDateShamsi,1,{}) as _group, count(*), sum(LoadedWeight),sum(UnLoadedWeight),sum(LoadedWeight-UnloadedWeight) 
        from InLoadings 
        where {} and Deleted=0
        group by SUBSTRING(EnterDateShamsi,1,{})
        order by _group Desc
        """.format(group_len,filter_string,group_len)
        query = query.replace('where AND', 'where ')
        query = query.replace('where  AND', 'where ')

    if table=="OutLoadings":

        query = """
        select SUBSTRING(EnterDateShamsi,1,{}) as _group, count(*), sum(LoadedWeight),sum(UnLoadedWeight),sum(LoadedWeight-UnloadedWeight) 
        from OutLoadings 
        where {} and Deleted=0
        group by SUBSTRING(EnterDateShamsi,1,{})
        order by _group Desc
        """.format(group_len,filter_string,group_len)
        query = query.replace('where AND', 'where ')
        query = query.replace('where  AND', 'where ')

    cursor.execute(query)
    result = cursor.fetchall()

    data = []
    for row in result:
        d = {}
        d['group'] = str(row[0])
        d['count'] = str(row[1])
        d['sumin'] = str(row[2])
        d['sumout'] = str(row[3])
        d['sumpure'] = str(row[4])
        
        data.append(d)

    return JsonResponse(json.dumps(data),safe=False)

def read_recent_invoices(request):

    now = datetime.datetime.now()
    shamsi=jdatetime.datetime.fromgregorian(datetime=now)
    shamsi = str(shamsi).split(' ')[0]
    shamsi = shamsi.replace('-','/')
    

    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    cursor = conn.cursor()
    query = """ select * from (
    select top 50 InvoiceNumber,CONCAT(FirstName,' ', LastName) name,VehicleNumber,I.CustomerID, Location,LoadedWeight,UnLoadedWeight,EnterDateShamsi, ExitDateShamsi, ExitDate from (select * from InLoadings where SUBSTRING(EnterDateShamsi,1,10) = '{}' and Deleted=0) I join Suppliers S on I.CustomerID=S.NationalID   order by ExitDate Desc
    UNION
    select top 50 InvoiceNumber, CONCAT(FirstName,' ', LastName) name,VehicleNumber,O.CustomerID,Location,LoadedWeight,UnLoadedWeight,EnterDateShamsi, ExitDateShamsi, ExitDate from (select * from OutLoadings where SUBSTRING(EnterDateShamsi,1,10) = '{}' and Deleted=0) O join Customers C on O.CustomerID=C.CustomerID  order by ExitDate Desc ) a
    order by a.ExitDate DESC
    """.format(shamsi, shamsi)

    cursor.execute(query)
    result = cursor.fetchall()
    
    data = []
    for row in result:
        d = {}
        d['reciept'] = str(row[0])
        d['name'] = str(row[1])
        d['vnumber'] = str(row[2])
        d['customerid'] = str(row[3])
        d['location'] = str(row[4])
        d['loadedweight'] = str(row[5])
        d['unloadedweight'] = str(row[6])
        d['enterdate'] = str(row[7])
        d['exitdate'] = str(row[8])
        
        data.append(d)
        
    
    return JsonResponse(json.dumps(data),safe=False)

def print_temp_invoice(request,carid):

    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query_string =  "select * from dbo.temp_loadings where VehicleNumber = N'{}' ".format(carid)
    cursor.execute(query_string)
    data = {}
    for row in cursor.fetchall():
        for i,itm in enumerate(row):
            if itm == None: 
                row[i] = ''
        data['reciept'] = ''
        data['enterdate'] = str(row[3])
        data['exitdate'] = str(row[4])
        data['driver'] = str(row[5])
        data['vnumber'] = str(row[6])
        data['id'] = str(row[7])
        data['fname'] = str(row[8])
        data['lname'] = str(row[9])
        data['mobile'] = str(row[10])
        data['faname'] = str(row[11])
        data['bank'] = str(row[12])
        data['loadedweight'] = str(row[13])
        data['unloadedweight'] = str(row[14])
        data['pureweight'] = ''
        data['loadtype'] = str(row[15])
        data['vtype'] = str(row[16])
        data['location'] = str(row[17])
        
        
    
    return JsonResponse(data)

def print_other_invoice(request,carid):

    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query_string =  "select * from dbo.OtherLoadings where VehicleNumber = N'{}' ".format(carid)
    cursor.execute(query_string)
    print (query_string)
    data = {}
    for row in cursor.fetchall():
        print (row)
        for i,itm in enumerate(row):
            if itm == None: 
                row[i] = ''
        data['reciept'] = ''
        data['enterdate'] = str(row[3])
        data['exitdate'] = str(row[4])
        data['driver'] = str(row[5])
        data['vnumber'] = str(row[6])
        data['id'] = str(row[7])
        data['fname'] = str(row[8])
        data['lname'] = str(row[9])
        data['mobile'] = str(row[10])
        data['faname'] = str(row[11])
        data['bank'] = str(row[12])
        data['loadedweight'] = str(row[13])
        data['unloadedweight'] = str(row[14])
        data['pureweight'] = ''
        data['loadtype'] = str(row[15])
        data['vtype'] = str(row[16])
        data['location'] = str(row[17])
        
        
    
    return JsonResponse(data)

def print_full_invoice(request,reciept):

    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    if reciept.startswith('1'):
        query_string =  """select il.InvoiceNumber, il.EnterDateShamsi, il.ExitDateShamsi, il.Driver, il.VehicleNumber, il.CustomerID, il.LoadedWeight, il.unloadedweight,
                           il.PureWeight, s.FirstName, s.LastName, s.FathersName, s.BankAccount, s.Mobile, v.Type, l.Type, il.Location    
                           from dbo.InLoadings il inner join Suppliers s on il.CustomerID = s.NationalID 
                           inner join VehiclesTypes v on il.VehicleType = v.ID 
                           inner join LoadTypes l on il.LoadType = l.ID 
                           where InvoiceNumber = '{}' """.format(reciept)
    elif reciept.startswith('2'):
        query_string =  """select il.InvoiceNumber, il.EnterDateShamsi, il.ExitDateShamsi, il.Driver, il.VehicleNumber, il.CustomerID, il.LoadedWeight, il.unloadedweight,
                           il.PureWeight, s.FirstName, s.LastName, s.FathersName, s.BankAccount, s.Mobile, v.Type, l.Type, il.Location    
                           from dbo.OutLoadings il inner join Customers s on il.CustomerID = s.CustomerID 
                           inner join VehiclesTypes v on il.VehicleType = v.ID 
                           inner join LoadTypes l on il.LoadType = l.ID 
                           where InvoiceNumber = '{}' """.format(reciept)
    else:
        print("invalid reciept number")
        return JsonResponse({'msg':'invalid response'})
    cursor.execute(query_string)
    data = {}
    for row in cursor.fetchall():
        for i,itm in enumerate(row):
            if itm == None: 
                row[i] = ''
        data['reciept'] = str(row[0])
        data['enterdate'] = str(row[1])
        data['exitdate'] = str(row[2])
        data['driver'] = str(row[3])
        data['vnumber'] = str(row[4])
        data['id'] = str(row[5])
        data['loadedweight'] = str(row[6])
        data['unloadedweight'] = str(row[7])    
        data['pureweight'] = str(row[8])
        
        
        data['fname'] = str(row[9])
        data['lname'] = str(row[10])
        data['mobile'] = str(row[13])
        data['faname'] = str(row[11])
        data['bank'] = str(row[12])

        data['loadtype'] = str(row[15])
        data['vtype'] = str(row[14])
        data['location'] = str(row[16])
        
    return JsonResponse(data)

def edit_temp_invoice(request,carid):

    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])
    
    cursor = conn.cursor()
    query_string =  "select * from dbo.temp_loadings where VehicleNumber = N'{}' ".format(carid)
    cursor.execute(query_string)
    data = {}
    for row in cursor.fetchall():
        for i,itm in enumerate(row):
            if itm == None: 
                row[i] = ''
        data['reciept'] = ''
        data['enterdate'] = str(row[3])
        data['exitdate'] = str(row[4])
        data['driver'] = str(row[5])
        vnumber = str(row[6])
        data['id'] = str(row[7])
        data['fname'] = str(row[8])
        data['lname'] = str(row[9])
        data['mobile'] = str(row[10])
        data['faname'] = str(row[11])
        data['bank'] = str(row[12])
        data['loadedweight'] = str(row[13])
        data['unloadedweight'] = str(row[14])
        data['pureweight'] = ''
        data['loadtype'] = str(row[15])
        data['vtype'] = str(row[16])
        data['location'] = str(row[17])

        idx1 = vnumber.index('(')
        idx2 = vnumber.index(')')

        data['vletter'] = vnumber[idx2 + 4]
        data['vcode'] = vnumber[idx2+1:idx2+4]
        data['vid'] = vnumber[idx2+5:]
        data['vregion'] = vnumber[idx1+1:idx2]
    
    return JsonResponse(data)

def edit_full_invoice(request,reciept):

    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=localhost;DATABASE='+DATABASES['default']['NAME']+';UID='+DATABASES['default']['USER']+';PWD='+DATABASES['default']['PASSWORD'])

    cursor = conn.cursor()
    if reciept.startswith('1'):
        query_string =  """select il.InvoiceNumber, il.EnterDateShamsi, il.ExitDateShamsi, il.Driver, il.VehicleNumber, il.CustomerID, il.LoadedWeight, il.unloadedweight,
                           il.PureWeight, s.FirstName, s.LastName, s.FathersName, s.BankAccount, s.Mobile, v.Type, l.Type, il.Location    
                           from dbo.InLoadings il inner join Suppliers s on il.CustomerID = s.NationalID 
                           inner join VehiclesTypes v on il.VehicleType = v.ID 
                           inner join LoadTypes l on il.LoadType = l.ID 
                           where InvoiceNumber = '{}' """.format(reciept)
    elif reciept.startswith('2'):
        query_string =  """select il.InvoiceNumber, il.EnterDateShamsi, il.ExitDateShamsi, il.Driver, il.VehicleNumber, il.CustomerID, il.LoadedWeight, il.unloadedweight,
                           il.PureWeight, s.FirstName, s.LastName, s.FathersName, s.BankAccount, s.Mobile, v.Type, l.Type, il.Location    
                           from dbo.OutLoadings il inner join Customers s on il.CustomerID = s.CustomerID 
                           inner join VehiclesTypes v on il.VehicleType = v.ID 
                           inner join LoadTypes l on il.LoadType = l.ID 
                           where InvoiceNumber = '{}' """.format(reciept)
    else:
        print("invalid reciept number")
        return JsonResponse({'msg':'شماره فاکتور نامعتبر است. لطفا مجددا اقدام بفرمایید'})
    cursor.execute(query_string)
    data = {}
    for row in cursor.fetchall():
        for i,itm in enumerate(row):
            if itm == None: 
                row[i] = ''
        data['reciept'] = str(row[0])
        data['enterdate'] = str(row[1])
        data['exitdate'] = str(row[2])
        data['driver'] = str(row[3])
        
        data['id'] = str(row[5])
        data['loadedweight'] = str(row[6])
        data['unloadedweight'] = str(row[7])    
        data['pureweight'] = str(row[8])

        vnumber = str(row[4])
         
        idx1 = vnumber.index('(')
        idx2 = vnumber.index(')')
        data['vletter'] = vnumber[idx2 + 4]
        data['vcode'] = vnumber[idx2+1:idx2+4]
        data['vid'] = vnumber[idx2+5:]
        data['vregion'] = vnumber[idx1+1:idx2]
        
        data['fname'] = str(row[9])
        data['lname'] = str(row[10])
        data['mobile'] = str(row[13])
        data['faname'] = str(row[11])
        data['bank'] = str(row[12])

        data['loadtype'] = str(row[15])
        data['vtype'] = str(row[14])
        data['location'] = str(row[16])
      
    return JsonResponse(data)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request):
   
    if request.method == 'GET':
        return HttpResponse({'item': 1}, mimetype="application/json")
    else:
        return HttpResponse("Request method is not a GET")