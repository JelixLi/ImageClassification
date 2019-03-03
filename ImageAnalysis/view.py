from django.http import HttpResponse
from django.shortcuts import render
import json
import pymysql.cursors
import pymysql
from . import image_process
import os
import shutil
import datetime


# def hello(request):
#     return HttpResponse("Hello world ! ")


def hello(request):
    return render(request,'index.html')

def process_database(class_name,img_src):
    db = pymysql.Connect(
    host='localhost',
    user='root',
    passwd='lj1512510237',
    db='mysql',
    charset='utf8')

    cursor = db.cursor()
    sql = "select count(*) from ImageData where image_class="+"\'"+class_name+"\'"
    cursor.execute(sql)
    results = cursor.fetchall()

    img_hash = image_process.pHash(img_src)

    if results[0][0] == 0 :
        sql = "INSERT INTO ImageData (image_class,image_class_id,image_hash) VALUES("+"\'"+class_name+"\'"+","+"1"+","+"\'"+img_hash+"\'"+")"
        cursor.execute(sql)
        db.commit()
        db.close()
    else:
        sql = "INSERT INTO ImageData (image_class,image_class_id,image_hash) VALUES("+"\'"+class_name+"\'"+","+str(results[0][0]+1)+","+"\'"+img_hash+"\'"+")"
        cursor.execute(sql)
        db.commit()
        db.close()



def get_max_id(class_name):
    db = pymysql.Connect(
    host='localhost',
    user='root',
    passwd='lj1512510237',
    db='mysql',
    charset='utf8')

    cursor = db.cursor()

    sql = "select max(image_class_id) from ImageData where image_class="+"\'"+class_name+"\'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if results[0][0]==None:
        return "0"
    else:
        return str(results[0][0])


def upload_file(request):  
    if request.POST:
        class_name = request.POST['class_name']
        if class_name=='':
            return HttpResponse("File upload Error") 
        else:
            myFile =request.FILES.get("myfile")
            str_name = "C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\"+class_name+"\\"+str(int(get_max_id(class_name))+1)+".jpg"
            if not os.path.exists("C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\"+class_name):
                os.mkdir( "C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\"+class_name)
            destination = open(str_name,'wb')   
            for chunk in myFile.chunks():      
                destination.write(chunk)  
            destination.close()  

            process_database(class_name,str_name)
            return HttpResponse("upload over!") 




def page_1(request):
    return render(request,'page_1.html')

def page_2(request):
    return render(request,'page_2.html')

def page_3(request):
    return render(request,'page_3.html')


def img_num(request):
    now_class = request.POST['args']
    ret_id = get_max_id(now_class)
    a = {"re":ret_id}
    return HttpResponse(json.dumps(a), content_type='application/json')

def img_class(request):
    db = pymysql.Connect(
    host='localhost',
    user='root',
    passwd='lj1512510237',
    db='mysql',
    charset='utf8')

    cursor = db.cursor()

    sql = "select image_class from ImageData group by image_class"

    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()

    json_results = {}
    count = 0

    for v in results:
        ret_str="args"+str(count)
        json_results[ret_str]=v    
        count=count+1

    return HttpResponse(json.dumps(json_results), content_type='application/json')


class get_list:
      def __init__(self):
          self.res_list=[]
    
      def push(self,image_id,res_map):
          count = 0 
          for item in self.res_list:
              if(res_map[item]<res_map[image_id]):
                  break
              count = count + 1 
              if count >= 6:
                  break

          self.res_list.insert(count,image_id)
          if len(self.res_list) > 6:
              self.res_list=self.res_list[:6]

      def get_res(self):
          return self.res_list

def search_file(request):
    if request.POST:
        myFile =request.FILES.get("myfile")
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        src = "C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\temp\\"+now+".jpg"
        if os.path.exists('C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\temp'):
            shutil.rmtree('C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\temp')
        os.mkdir('C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\temp')
        
        destination = open(src,'wb')   
        for chunk in myFile.chunks():      
            destination.write(chunk)  
        destination.close()  
        img_hash =  image_process.pHash(src)

        db = pymysql.Connect(
        host='localhost',
        user='root',
        passwd='lj1512510237',
        db='mysql',
        charset='utf8')

        cursor = db.cursor()

        sql = "select image_id,image_class,image_class_id,image_hash from ImageData;"
        cursor.execute(sql)
        results = cursor.fetchall()

        res_map={}
        store_map = {}
        gt = get_list()
        for v in results:
            image_id=int(v[0])
            res_map[image_id]=image_process.get_similarity(v[3],img_hash)
            store_map[image_id]=str(v[1])+"/"+str(v[2])+".jpg"
            gt.push(image_id,res_map)

        res_list = gt.get_res()

        count = 0
        json_results={}
        json_results['file_src']=now+".jpg"
        for v in res_list:
            ret_str="args"+str(count)
            json_results[ret_str]=store_map[v]
            count = count + 1

        return HttpResponse(json.dumps(json_results), content_type='application/json')


def recognize(request):
    if request.POST:
        myFile =request.FILES.get("myfile")
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        src = "C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\temp\\"+now+".jpg"
        if os.path.exists('C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\temp'):
            shutil.rmtree('C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\temp')
        os.mkdir('C:\\Users\\Administrator\\Desktop\\pyData\\ImageAnalysis\\static\\images\\temp')
        destination = open(src,'wb')   
        for chunk in myFile.chunks():      
            destination.write(chunk)  
        destination.close()  
        img_hash =  image_process.pHash(src)
        
        destination = open(src,'wb')   
        for chunk in myFile.chunks():      
            destination.write(chunk)  
        destination.close()  
        img_hash =  image_process.pHash(src)

        db = pymysql.Connect(
        host='localhost',
        user='root',
        passwd='lj1512510237',
        db='mysql',
        charset='utf8')

        cursor = db.cursor()

        sql = "select image_id,image_class,image_class_id,image_hash from ImageData;"
        cursor.execute(sql)
        results = cursor.fetchall()

        store_map = {}
        cur_max_id = -1
        cur_max_similarity = -1
        for v in results:
            image_id=int(v[0])
            res = image_process.get_similarity(v[3],img_hash)
            if res > cur_max_similarity:
                cur_max_similarity=res
                cur_max_id=image_id
            
            store_map[image_id]=str(v[1])

        json_results={}
        json_results['file_src']=now+".jpg"
        json_results["args"]=store_map[cur_max_id]

        return HttpResponse(json.dumps(json_results), content_type='application/json')