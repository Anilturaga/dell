from django.shortcuts import render
from django.shortcuts import render, redirect
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from dell.models import Dell,accessories,BackendAnalytics
from django import forms 
from dell.forms import CustomerForm  
from django.views.decorators.csrf import csrf_exempt

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 18:06:55 2019

@author: mogal
"""

import pandas as pd
import math
def countX(lst, x): 
    count = 0
    for ele in lst: 
        if (ele == x): 
            count = count + 1
    return count
        
def cosine_similarity(v1,v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def rampriority(df):
    ramcount=[]
    RAM1=df['RAM']
    RAM1=RAM1.tolist()
    ram_values=df.RAM.unique()
    ram_values=ram_values.tolist()
    for i in ram_values:
        ramcount.append(countX(RAM1,i))
    n = len(ramcount)
    for i in range(n):
        for j in range(0, n-i-1):
            if ramcount[j] < ramcount[j+1] :
                ramcount[j], ramcount[j+1] = ramcount[j+1], ramcount[j]
                ram_values[j], ram_values[j+1] = ram_values[j+1], ram_values[j] 
    return ram_values

def graphicpriority(df):
    graphiccount=[]
    graphic1=df['GraphicCard']
    graphic1=graphic1.tolist()
    graphic_values=df.GraphicCard.unique()
    graphic_values=graphic_values.tolist()
    for i in graphic_values:
        graphiccount.append(countX(graphic1,i))
    n = len(graphiccount)
    for i in range(n):
        for j in range(0, n-i-1):
            if graphiccount[j] < graphiccount[j+1] :
                graphiccount[j], graphiccount[j+1] = graphiccount[j+1], graphiccount[j]
                graphic_values[j], graphic_values[j+1] = graphic_values[j+1], graphic_values[j] 
    return graphic_values

def costpriority(df):
    cost_values=df.Cost.unique()
    cost_values=cost_values.tolist()
    for i in range(0, len(cost_values)): 
         cost_values[i] = int(cost_values[i]) 
    cost_max=max(cost_values)
    cost_min=min(cost_values)
    return cost_max,cost_min

def colorpriority(df):
    colorcount=[]
    color1=df['Color']
    color1=color1.tolist()
    color_values=df.Color.unique()
    color_values=color_values.tolist()
    for i in color_values:
        colorcount.append(countX(color1,i))
    n = len(colorcount)
    for i in range(n):
        for j in range(0, n-i-1):
            if colorcount[j] < colorcount[j+1] :
                colorcount[j], colorcount[j+1] = colorcount[j+1], colorcount[j]
                color_values[j], color_values[j+1] = color_values[j+1], color_values[j] 
    return color_values

def screenpriority(df):
    screencount=[]
    screen1=df['ScreenSize']
    screen1=screen1.tolist()
    screen_values=df.ScreenSize.unique()
    screen_values=screen_values.tolist()
    for i in screen_values:
        screencount.append(countX(screen1,i))
    n = len(screencount)
    for i in range(n):
        for j in range(0, n-i-1):
            if screencount[j] < screencount[j+1] :
                screencount[j], screencount[j+1] = screencount[j+1], screencount[j]
                screen_values[j], screen_values[j+1] = screen_values[j+1], screen_values[j] 
    return screen_values

def memorypriority(df):
    memorycount=[]
    memory1=df['Memory']
    memory1=memory1.tolist()
    memory_values=df.Memory.unique()
    memory_values=memory_values.tolist()
    for i in memory_values:
        memorycount.append(countX(memory1,i))
    n = len(memorycount)
    for i in range(n):
        for j in range(0, n-i-1):
            if memorycount[j] < memorycount[j+1] :
                memorycount[j], memorycount[j+1] = memorycount[j+1], memorycount[j]
                memory_values[j], memory_values[j+1] = memory_values[j+1], memory_values[j] 
    return memory_values

def processorpriority(df):
    processorcount=[]
    processor1=df['Processor']
    processor1=processor1.tolist()
    processor_values=df.Processor.unique()
    processor_values=processor_values.tolist()
    for i in processor_values:
        processorcount.append(countX(processor1,i))
    n = len(processorcount)
    for i in range(n):
        for j in range(0, n-i-1):
            if processorcount[j] < processorcount[j+1] :
                processorcount[j], processorcount[j+1] = processorcount[j+1], processorcount[j]
                processor_values[j], processor_values[j+1] = processor_values[j+1], processor_values[j] 
    return processor_values

def gcompanypriority(df):
    gcompanycount=[]
    gcompany1=df['Gcompany']
    gcompany1=gcompany1.tolist()
    gcompany_values=df.Gcompany.unique()
    gcompany_values=gcompany_values.tolist()
    for i in gcompany_values:
        gcompanycount.append(countX(gcompany1,i))
    n = len(gcompanycount)
    for i in range(n):
        for j in range(0, n-i-1):
            if gcompanycount[j] < gcompanycount[j+1] :
                gcompanycount[j], gcompanycount[j+1] = gcompanycount[j+1], gcompanycount[j]
                gcompany_values[j], gcompany_values[j+1] = gcompany_values[j+1], gcompany_values[j] 
    return gcompany_values

def change(df,df1):
    ram=rampriority(df)
    n=len(ram)
    df1['RAM'] = df1['RAM'].apply({8:n, 16:n-1,4:n-2,64:n-3,6:n-4}.get)
    
    screen=screenpriority(df)
    m=len(screen)
    df1['ScreenSize'] = df1['ScreenSize'].apply({17.3:m,15.6:m-1}.get)
    
    color=colorpriority(df)
    a=len(color)
    df1['Color']=df1['Color'].apply({'Black':a,'Shadow Black':a-1,'Stealth Black':a-2,'Obsidian Black':a-3,'Scar Gunmetal':a-4,'Peacock Blue':a-5}.get)
    
    grap=graphicpriority(df)
    b=len(grap)
    df1['GraphicCard']=df1['GraphicCard'].apply({'4GB':b,'6GB':b-1,'8GB':b-2,'3GB':b-3}.get)
    
    gcom=gcompanypriority(df)
    c=len(gcom)
    df1['Gcompany']=df1['Gcompany'].apply({'NVDIA GTX 1050':c,'NVDIA GTX 1650':c-1,'NVDIA GTX 1660':c-2,'NVDIA RTX 2060':c-3,'NVDIA RTX 2080':c-4,'Radeon RX 560X':c-5,'NVIDIA GTX 1050':c-6,'NVDIA  GTX 1650':c-7,'NVDIA GTX 1070':c-8,'NVDIA GTX 1060':c-9}.get)
    
    mem=memorypriority(df)
    d=len(mem)
    df1['Memory']=df1['Memory'].apply({'1TB':d, '512GB':d-1, '2TB':d-2}.get)
    
    proc=processorpriority(df)
    e=len(proc)
    df1['Processor']=df1['Processor'].apply({'Intel Core i7':e,'Intel Core i5':e-1,'Intel Core i9':e-2,'AMD Ryzen 5-3550H':e-3,'Intel core i5':e-4}.get);
    return

def cossimilarity(df,df1):
    Row_list =[] 
    for index, rows in df1.iterrows(): 
        my_list =[rows.ScreenSize, rows.RAM,rows.Color,rows.GraphicCard,rows.Gcompany,rows.Memory,rows.Processor]  
        Row_list.append(my_list)
    ram=rampriority(df)
    screen=screenpriority(df)
    color=colorpriority(df)
    grap=graphicpriority(df)
    gcom=gcompanypriority(df)
    mem=memorypriority(df)
    proc=processorpriority(df)
    base=[len(screen),len(ram),len(color),len(grap),len(gcom),len(mem),len(proc)]
    comp=[]
    for i in Row_list:
        p=cosine_similarity(i,base)
        comp.append(p)
    return comp

def finaloutput(df,df1):
    comp=cossimilarity(df,df1)
    df2=df1
    Row_list1 =[] 
    for index, rows in df2.iterrows(): 
        my_list =[rows.ID,rows.LaptopName,rows.ScreenSize, rows.RAM,rows.Cost,rows.Color,rows.GraphicCard,rows.Gcompany,rows.Memory,rows.Processor,rows.Rating]  
        Row_list1.append(my_list)
    n = len(comp)
    for i in range(n):
        for j in range(0, n-i-1):
            if comp[j] < comp[j+1] :
                comp[j], comp[j+1] = comp[j+1], comp[j]
                Row_list1[j], Row_list1[j+1] = Row_list1[j+1], Row_list1[j] 
    new_df = pd.DataFrame(columns=['ID','LaptopName','ScreenSize','RAM','Cost','Color','GraphicCard','Gcompany','Memory','Processor','Rating'], data=Row_list1)
    i,j=costpriority(df)
    new_df['Cost']=new_df['Cost'].astype(int)
    for i in range(len(new_df)):
        if(new_df['Cost'][i] >j & new_df['Cost'][i] <i):
            new_df[new_df.LaptopName != new_df['LaptopName'][i]]
    final_df=new_df.drop(['LaptopName','ScreenSize','RAM','Cost','Color','GraphicCard','Gcompany','Memory','Processor','Rating'],axis=1)
    return final_df

        
def main():
    df=pd.read_csv("/home/anil/Desktop/dellProject/dell/laptop - Sheet1.csv")
    df=df.drop(df.index[1])
    df1=pd.read_csv("/home/anil/Desktop/dellProject/dell/dell1 - Sheet1.csv")  
    rampriority(df)
    screenpriority(df)
    colorpriority(df)
    costpriority(df)
    screenpriority(df)
    graphicpriority(df)
    gcompanypriority(df)
    processorpriority(df)
    memorypriority(df)
    change(df,df1)
    cossimilarity(df,df1)
    return finaloutput(df,df1)['ID'].tolist()
    

def index(request):
    form = CustomerForm()  
    return render(request, "index.html", {'form':form})
@csrf_exempt
def foryou(request,):
    array=[8,11,2,3,4,7,6,10,9,5,1]
    array = main()
    data = Dell.objects.all()
    files = []
    for index in range(0,11):
        files.append({'name':data.get(ID = array[index]).LaptopName,
        'id' : array[index],
         'photo' : data.get(ID = array[index]).photo,
         'screen' : data.get(ID = array[index]).ScreenSize,
         'cost' : data.get(ID = array[index]).Cost,
         'ram' : data.get(ID = array[index]).RAM,
         'gcard' : data.get(ID = array[index]).GraphicCard,
         'gcompany' : data.get(ID = array[index]).Gcompany,
         'memory' : data.get(ID = array[index]).Memory,
         'processor' : data.get(ID = array[index]).Processor,
         'rating' : data.get(ID = array[index]).Rating,})
    
    template = loader.get_template('foryou.html')
    context = {
        'data' : files
        
    }
    return HttpResponse(template.render(context, request))
@csrf_exempt
def formHandler(request):
     if request.method == "POST":
        form = CustomerForm(request.POST)
        ans = request.POST['submit']
        print("!!!!!!!!!!!!!")
        print(ans)
        template = loader.get_template('foryou.html')
        context ={}  
        return redirect("foryou/")

@csrf_exempt
def single(request,index):
    data = Dell.objects.all()
    files = []
    files.append({'name':data.get(ID = index).LaptopName,
        'id' : index,
         'photo' : data.get(ID = index).photo,
         'screen' : data.get(ID = index).ScreenSize,
         'cost' : data.get(ID = index).Cost,
         'ram' : data.get(ID = index).RAM,
         'gcard' : data.get(ID = index).GraphicCard,
         'gcompany' : data.get(ID = index).Gcompany,
         'memory' : data.get(ID = index).Memory,
         'processor' : data.get(ID = index).Processor,
         'rating' : data.get(ID = index).Rating})
    access = []
    a = accessories.objects.all()
    string = data.get(ID = index).Accessories
    temp = []
    temp.append(int(string[0]))
    temp.append(int(string[1]))
    temp.append(int(string[2]))
    for index in range(0,3):
        access.append({'name':a.get(ID = temp[index]).Name,
        'id' : temp[index],
         'photo' : a.get(ID = temp[index]).photo,
         'cost' : a.get(ID = temp[index]).Cost,})
    
    template = loader.get_template('single.html')
    context = {
        'data' : files,
        'access' : access
    }
    return HttpResponse(template.render(context, request))
@csrf_exempt
def cart(request):
    try:
        tutorial  = request.COOKIES['id']
        ids = tutorial.split('/')
        ids = ids[1:]
        laptops = []
        temp =[]
        total = 0
        for iterater in range(len(ids)):
            if int(ids[iterater]) > 11:
                temp.append(int(ids[iterater])-11)
            else:
                laptops.append( int(ids[iterater]))
        data = Dell.objects.all()
        a = accessories.objects.all()
        files = []
        for index in laptops:
            files.append({'name':data.get(ID = index).LaptopName,
            'id' : index,
            'photo' : data.get(ID = index).photo,
            'cost' : data.get(ID = index).Cost,})
            total = total + data.get(ID = index).Cost
        for index in temp:
            files.append({'name':a.get(ID = index).Name,
            'id' : index,
            'photo' : a.get(ID = index).photo,
            'cost' : a.get(ID = index).Cost,})
            total = total + a.get(ID = index).Cost
        template = loader.get_template('cart.html')
        context = {
            'valid' : 1,
            'data' : files,
            'total' : total
        }
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('cart.html')
        context = {
            'valid' : 0,
            'error' : "Add items to the cart or enable cookies to view items"
        }
        return HttpResponse(template.render(context, request))
        
    
    
        
