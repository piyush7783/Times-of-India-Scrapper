import re
from datetime import date
from bs4 import BeautifulSoup
import pymysql
from urllib.request import Request, urlopen
import requests

conn= pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='toi',
)
cursor= conn.cursor()

date1 = str(input("Enter your date in yyyy/mm/dd:"))
reason1= str(input("Enter your query:"))

year1,month1,day1 =map(int, date1.split('/'))

a= date(2001,1,1)
b=date(year1,month1,day1)
var=b-a
result=var.days + 36892
link="https://timesofindia.indiatimes.com/"+str(date1)+"/archivelist/year-"+str(year1)+",month-"+str(month1)+",starttime-"+str(result)+".cms"

req= requests.get(link,headers={'User-Agent': 'Mozilla/5.0'})

bsObj= BeautifulSoup(req.text,'lxml')

reason1=reason1.lower()
tags=bsObj.find_all('a')
lst=[]
for tag in tags:
    var1=tag.get('href')
    var2=tag.text
    var2=var2.lower()
    x=re.findall(reason1,var2)
    if(len(x)!=0):
        if("http://timesofindia.indiatimes.com/" or "https://timesofindia.indiatimes.com/" not in var1):
            var1="http://timesofindia.indiatimes.com/"+str(var1)
            lst.append(var1)
        else:
            lst.append(var1)
if(len(lst)==0):
    print("No news found")
else:
    for i in lst:
        html1= requests.get(i,headers={'User-Agent': 'Mozilla/5.0'})
        bsobj1= BeautifulSoup(html1.text,'lxml')
        var4= bsobj1.findAll("div",{"class":"Normal"})
        str1=""
        try:
            for j in var4:
                str1=str1+str(j.text)
        except:
            pass
        # database
        sql = "INSERT INTO scraping (`link`, `data`) VALUES (%s, %s)"
        cursor.execute(sql, (i, str1))
        print("Task added successfully")
        conn.commit()
conn.close()
