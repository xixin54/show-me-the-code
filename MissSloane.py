#spider for Miss Slonae

#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import BeautifulSoup fro bs4
import re
#import lxml
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


cookie =''

def generator_URL():
  for i in range(4000):
    url = 'https://movie.douban.com/subject/26703158/comments?start='+str(20*i+1)+'&limit=20&sort=new_score&status=P'
    #print url
    yield url

for url in generator_URL():
  print url      # test generator
    
def Slonae(url):
  dict1 = {}
  for i in url:
    res = resquest(i,cookie,timeout=100)
    soup = BeautifulSoup(res)
    comture = soup.findAll(class='comment')
    
    #dict1 = {}
    for i in comture:
      name = i.find(class='comment-info').a.string
      comtext = i.p.string
      dict1[name]=comtext
      
  return dict1
      
    
    
    
