
#http://blog.csdn.net/gamer_gyt/article/details/51346159

#-*-coding:utf-8-*-  
''''' 
Created on 2016年5月2日 
 
@author: Gamer Think 
'''  
from math import sqrt  
  
fp = open("uid_score_bid","r")  
  
users = {}  
  
for line in open("uid_score_bid"):  
    lines = line.strip().split(",")  
    if lines[0] not in users:  
        users[lines[0]] = {}  
    users[lines[0]][lines[2]]=float(lines[1])  
  
  
#----------------新增代码段END----------------------  
  
  
  
class recommender:  
    #data：数据集，这里指users  
    #k：表示得出最相近的k的近邻  
    #metric：表示使用计算相似度的方法  
    #n：表示推荐book的个数  
    def __init__(self, data, k=3, metric='pearson', n=12):  
  
        self.k = k  
        self.n = n  
        self.username2id = {}  
        self.userid2name = {}  
        self.productid2name = {}  
  
        self.metric = metric  
        if self.metric == 'pearson':  
            self.fn = self.pearson  
        if type(data).__name__ == 'dict':  
            self.data = data  
        
    def convertProductID2name(self, id):  
  
        if id in self.productid2name:  
            return self.productid2name[id]  
        else:  
            return id  
  
    #定义的计算相似度的公式，用的是皮尔逊相关系数计算方法  
    def pearson(self, rating1, rating2):  
        sum_xy = 0  
        sum_x = 0  
        sum_y = 0  
        sum_x2 = 0  
        sum_y2 = 0  
        n = 0  
        for key in rating1:  
            if key in rating2:  
                n += 1  
                x = rating1[key]  
                y = rating2[key]  
                sum_xy += x * y  
                sum_x += x  
                sum_y += y  
                sum_x2 += pow(x, 2)  
                sum_y2 += pow(y, 2)  
        if n == 0:  
            return 0  
          
        #皮尔逊相关系数计算公式   
        denominator = sqrt(sum_x2 - pow(sum_x, 2) / n)  * sqrt(sum_y2 - pow(sum_y, 2) / n)  
        if denominator == 0:  
            return 0  
        else:  
            return (sum_xy - (sum_x * sum_y) / n) / denominator  
      
    def computeNearestNeighbor(self, username):  
        distances = []  
        for instance in self.data:  
            if instance != username:  
                distance = self.fn(self.data[username],self.data[instance])  
                distances.append((instance, distance))  
  
        distances.sort(key=lambda artistTuple: artistTuple[1],reverse=True)  
        return distances  
      
    #推荐算法的主体函数  
    def recommend(self, user):  
        #定义一个字典，用来存储推荐的书单和分数  
        recommendations = {}  
        #计算出user与所有其他用户的相似度，返回一个list  
        nearest = self.computeNearestNeighbor(user)  
        # print nearest  
          
        userRatings = self.data[user]  
#         print userRatings  
        totalDistance = 0.0  
        #得住最近的k个近邻的总距离  
        for i in range(self.k):  
            totalDistance += nearest[i][1]  
        if totalDistance==0.0:  
            totalDistance=1.0  
              
        #将与user最相近的k个人中user没有看过的书推荐给user，并且这里又做了一个分数的计算排名  
        for i in range(self.k):  
              
            #第i个人的与user的相似度，转换到[0,1]之间  
            weight = nearest[i][1] / totalDistance  
              
            #第i个人的name  
            name = nearest[i][0]  
  
            #第i个用户看过的书和相应的打分  
            neighborRatings = self.data[name]  
  
            for artist in neighborRatings:  
                if not artist in userRatings:  
                    if artist not in recommendations:  
                        recommendations[artist] = (neighborRatings[artist] * weight)  
                    else:  
                        recommendations[artist] = (recommendations[artist]+ neighborRatings[artist] * weight)  
  
        recommendations = list(recommendations.items())  
        recommendations = [(self.convertProductID2name(k), v)for (k, v) in recommendations]  
          
        #做了一个排序  
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)  
  
        return recommendations[:self.n],nearest  
   
def adjustrecommend(id):  
    bookid_list = []  
    r = recommender(users)  
    k,nearuser = r.recommend("%s" % id)  
    for i in range(len(k)):  
        bookid_list.append(k[i][0])  
    return bookid_list,nearuser[:15]        #bookid_list推荐书籍的id，nearuser[:15]最近邻的15个用户
   
      
   
#调用函数，输出结果
bookid_list,near_list = adjustrecommend("changanamei")
print ("bookid_list:",bookid_list) ##
'''('near_list:', [('122946019', 0.95478592449625332), ('56746289', 0.82807867121082335), ('yiminuansheng', 0.82368776758037365), ('4030281', 0.82090084975482847), ('46832091', 0.81666666666667098), ('111223566', 0.81242074845948797), ('4750931', 0.80178372573727841), ('65121529', 0.80064076902543724), ('57475649', 0.78835612279228862), ('budingsetlla', 0.77849894416152376), ('69874649', 0.76980035891950938), ('122191787', 0.76547790070314037), ('63589110', 0.75000000000000611), ('bshayna', 0.75000000000000611), ('94986189', 0.75000000000000611)])
'''

print ("near_list:",near_list) ##
'''('near_list:', [('122946019', 0.95478592449625332), ('56746289', 0.82807867121082335), ('yiminuansheng', 0.82368776758037365), ('4030281', 0.82090084975482847), ('46832091', 0.81666666666667098), ('111223566', 0.81242074845948797), ('4750931', 0.80178372573727841), ('65121529', 0.80064076902543724), ('57475649', 0.78835612279228862), ('budingsetlla', 0.77849894416152376), ('69874649', 0.76980035891950938), ('122191787', 0.76547790070314037), ('63589110', 0.75000000000000611), ('bshayna', 0.75000000000000611), ('94986189', 0.75000000000000611)])
'''



















########################################################
### http://python.jobbole.com/83938/

>>> import pandas as pd
>>> from pandas import Series,DataFrame
>>> rnames = ['user_id','movie_id','rating','timestamp']
>>> ratings = pd.read_table(r'ratings.dat',sep='::',header=None,names=rnames)
>>> ratings[:3]
   user_id  movie_id  rating  timestamp
0        1      1193       5  978300760
1        1       661       3  978302109
2        1       914       3  978301968

[3 rows x 4 columns]

####
>>> data = ratings.pivot(index='user_id',columns='movie_id',values='rating')
>>> data[:5]
movie_id  1   2   3   4   5   6  
user_id                                                                        
1          5 NaN NaN NaN NaN NaN ...
2        NaN NaN NaN NaN NaN NaN ...
3        NaN NaN NaN NaN NaN NaN ...
4        NaN NaN NaN NaN NaN NaN ...
5        NaN NaN NaN NaN NaN   2 ...

#
>>> foo = DataFrame(np.empty((len(data.index),len(data.index)),dtype=int),index=data.index,columns=data.index)
>>> for i in foo.index:
        for j in foo.columns:
            foo.ix[i,j] = data.ix[i][data.ix[j].notnull()].dropna().count()
    
#
>>> for i in foo.index:
        foo.ix[i,i]=0#先把对角线的值设为 0

>>> ser = Series(np.zeros(len(foo.index)))
>>> for i in foo.index:
        ser[i]=foo[i].max()#计算每行中的最大值

>>> ser.idxmax()#返回 ser 的最大值所在的行号
4169

>>> ser[4169]#取得最大值
998

>>> foo[foo==998][4169].dropna()#取得另一个 user_id
424     4169
Name: user_id, dtype: float64
  
#
>>> data.ix[4169].corr(data.ix[424])
0.45663851303413217
>>> test = data.reindex([424,4169],columns=data.ix[4169][data.ix[424].notnull()].dropna().index)
>>> test
movie_id  2   6   10  11  12  17 ...
424        4   4   4   4   1   5 ... 
4169       3   4   4   4   2   5 ...

>>> test.ix[424].value_counts(sort=False).plot(kind='bar')
>>> test.ix[4169].value_counts(sort=False).plot(kind='bar')

#
>>> periods_test = DataFrame(np.zeros((20,7)),columns=[10,20,50,100,200,500,998])
>>> for i in periods_test.index:
        for j in periods_test.columns:
            sample = test.reindex(columns=np.random.permutation(test.columns)[:j])
            periods_test.ix[i,j] = sample.iloc[0].corr(sample.iloc[1])

>>> periods_test[:5]
        10        20        50        100       200       500       998
0 -0.306719  0.709073  0.504374  0.376921  0.477140  0.426938  0.456639
1  0.386658  0.607569  0.434761  0.471930  0.437222  0.430765  0.456639
2  0.507415  0.585808  0.440619  0.634782  0.490574  0.436799  0.456639
3  0.628112  0.628281  0.452331  0.380073  0.472045  0.444222  0.456639
4  0.792533  0.641503  0.444989  0.499253  0.426420  0.441292  0.456639

[5 rows x 7 columns]
>>> periods_test.describe()
             10         20         50         100        200        500  #998略
count  20.000000  20.000000  20.000000  20.000000  20.000000  20.000000   
mean    0.346810   0.464726   0.458866   0.450155   0.467559   0.452448   
std     0.398553   0.181743   0.103820   0.093663   0.036439   0.029758   
min    -0.444302   0.087370   0.192391   0.242112   0.412291   0.399875   
25%     0.174531   0.320941   0.434744   0.375643   0.439228   0.435290   
50%     0.487157   0.525217   0.476653   0.468850   0.472562   0.443772   
75%     0.638685   0.616643   0.519827   0.500825   0.487389   0.465787   
max     0.850963   0.709073   0.592040   0.634782   0.546001   0.513486   

[8 rows x 7 columns]

#
>>> check_size = 1000
>>> check = {}
>>> check_data = data.copy()#复制一份 data 用于检验，以免篡改原数据
>>> check_data = check_data.ix[check_data.count(axis=1)>200]#滤除评价数小于200的用户
>>> for user in np.random.permutation(check_data.index):
        movie = np.random.permutation(check_data.ix[user].dropna().index)[0]
        check[(user,movie)] = check_data.ix[user,movie]
        check_data.ix[user,movie] = np.nan
        check_size -= 1
        if not check_size:
            break

>>> corr = check_data.T.corr(min_periods=200)
>>> corr_clean = corr.dropna(how='all')
>>> corr_clean = corr_clean.dropna(axis=1,how='all')#删除全空的行和列
>>> check_ser = Series(check)#这里是被提取出来的 1000 个真实评分
>>> check_ser[:5]
(15, 593)     4
(23, 555)     3
(33, 3363)    4
(36, 2355)    5
(53, 3605)    4
dtype: float64
 
 #
 >>> result = Series(np.nan,index=check_ser.index)
>>> for user,movie in result.index:#这个循环看着很乱，实际内容就是加权平均而已
        prediction = []
        if user in corr_clean.index:
            corr_set = corr_clean[user][corr_clean[user]>0.1].dropna()#仅限大于 0.1 的用户
        else:continue
        for other in corr_set.index:
            if  not np.isnan(data.ix[other,movie]) and other != user:#注意bool(np.nan)==True
                prediction.append((data.ix[other,movie],corr_set[other]))
        if prediction:
            result[(user,movie)] = sum([value*weight for value,weight in prediction])/sum([pair[1] for pair in prediction])

>>> result.dropna(inplace=True)
>>> len(result)#随机抽取的 1000 个用户中也有被 min_periods=200 刷掉的
862
>>> result[:5]
(23, 555)     3.967617
(33, 3363)    4.073205
(36, 2355)    3.903497
(53, 3605)    2.948003
(62, 1488)    2.606582
dtype: float64
>>> result.corr(check_ser.reindex(result.index))
0.436227437429696
>>> (result-check_ser.reindex(result.index)).abs().describe()#推荐期望与实际评价之差的绝对值
count    862.000000
mean       0.785337
std        0.605865
min        0.000000
25%        0.290384
50%        0.686033
75%        1.132256
max        3.629720
dtype: float64
 
 
 #
 >>> corr = data.T.corr(min_periods=200)
>>> corr_clean = corr.dropna(how='all')
>>> corr_clean = corr_clean.dropna(axis=1,how='all')

#
>>> lucky = np.random.permutation(corr_clean.index)[0]
>>> gift = data.ix[lucky]
>>> gift = gift[gift.isnull()]#现在 gift 是一个全空的序列


#
>>> corr_lucky = corr_clean[lucky].drop(lucky)#lucky 与其他用户的相关系数 Series，不包含 lucky 自身
>>> corr_lucky = corr_lucky[corr_lucky>0.1].dropna()#筛选相关系数大于 0.1 的用户
>>> for movie in gift.index:#遍历所有 lucky 没看过的电影
        prediction = []
        for other in corr_lucky.index:#遍历所有与 lucky 相关系数大于 0.1 的用户
            if not np.isnan(data.ix[other,movie]):
                prediction.append((data.ix[other,movie],corr_clean[lucky][other]))
        if prediction:
            gift[movie] = sum([value*weight for value,weight in prediction])/sum([pair[1] for pair in prediction])

>>> gift.dropna().order(ascending=False)#将 gift 的非空元素按降序排列
movie_id
3245        5.000000
2930        5.000000
2830        5.000000
2569        5.000000
1795        5.000000
981         5.000000
696         5.000000
682         5.000000
666         5.000000
572         5.000000
1420        5.000000
3338        4.845331
669         4.660464
214         4.655798
3410        4.624088
...
2833        1
2777        1
2039        1
1773        1
1720        1
1692        1
1538        1
1430        1
1311        1
1164        1
843         1
660         1
634         1
591         1
56          1
Name: 3945, Length: 2991, dtype: float64
   
   
####
