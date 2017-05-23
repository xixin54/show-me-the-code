#https://my.oschina.net/lionets/blog/284479

import pandas as pd  
 from pandas import Series,DataFrame

 rnames = ['user_id','movie_id','rating','timestamp']
 ratings = pd.read_table(r'ratings.dat',sep='::',header=None,names=rnames)
# ratings[:3]

data = ratings.pivot(index='user_id',columns='movie_id',values='rating')

foo = DataFrame(np.empty((len(data.index),len(data.index)),dtype=int),index=data.index,columns=data.index)
for i in foo.index:
        for j in foo.columns:
            foo.ix[i,j] = data.ix[i][data.ix[j].notnull()].dropna().count()
        
for i in foo.index:
     foo.ix[i,i]=0#先把对角线的值设为 0
    
ser = Series(np.zeros(len(foo.index)))
for i in foo.index:
     ser[i]=foo[i].max()#计算每行中的最大值
    
ser.idxmax()#返回 ser 的最大值所在的行号

ser[4169]#取得最大值

foo[foo==998][4169].dropna()#取得另一个 user_id


data.ix[4169].corr(data.ix[424])
test = data.reindex([424,4169],columns=data.ix[4169][data.ix[424].notnull()].dropna().index)
>>> test

>>> test.ix[424].value_counts(sort=False).plot(kind='bar')
>>> test.ix[4169].value_counts(sort=False).plot(kind='bar')



>>> periods_test = DataFrame(np.zeros((20,7)),columns=[10,20,50,100,200,500,998])
>>> for i in periods_test.index:
        for j in periods_test.columns:
            sample = test.reindex(columns=np.random.permutation(test.columns)[:j])
            periods_test.ix[i,j] = sample.iloc[0].corr(sample.iloc[1])
          
          
          
