#spider for Miss Slonae

#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import beautifulsoup fro bs4
#import lxml

cookie =''

def generator_URL():
  for i in range(4000):
    url = 'https://movie.douban.com/subject/26703158/comments?start='+str(20*i+1)+'&limit=20&sort=new_score&status=P'
    #print url
    yield url

for url in generator_URL():
  print url      # test generator
    
def Slonae(url):
  for i in url:
    res = resquest(i,cookie,time=100)
    
    
    
