#!/usr/bin
# -*-coding:utf-8-*-


from math import sqrt
import codecs
import platform

## 元数据
srcfile = r"C:\Users\siege\Desktop\crd2.txt" if platform.system()=="Windows" else "/home/zkpk/Desktop/wfsiege/clnt_merch_count.txt"

'''
fp = open("/tmp/siege2/python/test_data.txt","r")  
users = {}  
for line in fp:  
    lines = line.strip().split(",")  
    if lines[0] not in users:  
        users[lines[0]] = {}  
    users[lines[0]][lines[2]]=float(lines[1])  
'''

fp = open(srcfile, "r")
users = {}
users_txndt = {}


for line in fp:
    lines = line.strip().split()
    if lines[0] not in users:
        users[lines[0]] = {}
        #users_txndt[lines[0]] = {}
    users[lines[0]][lines[1]] = float(lines[2])
    #users_txndt[lines[0]][lines[1]] = float(lines[3])

    # print lines
    # print users


class recommender:
    # data：data of users
    # k：nearest K
    # metric：calculations
    # n：recommend books
    def __init__(self, data, k=3, metric='cosine', n=10):

        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.f = {}

        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        elif self.metric == 'cosine':
            self.fn = self.cosine
        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):

        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    # similarity calculation
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

            # specific steps
        denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def cosine(self, rating1, rating2):
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

        # specific steps
        denominator = sqrt(sum_x2) * sqrt(sum_y2)
        if denominator == 0:
            return 0
        else:
            return (sum_xy) / denominator

    def computeNearestNeighbor(self, username):
        dist= []
        for instance in self.data:
            if dist != username:
                dist = self.fn(self.data[username], self.data[instance])
                dist.append((instance, dist))

                dist.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return dist

        # reconmend main

    def recommend(self, user):
        # dictionary to store data
        recommendations = {}
        # similiar user list
        nearest = self.computeNearestNeighbor(user)
        #print（nearest）

        userRatings = self.data[user]
        #print userRatings
        totalDistance = 0.0
        # nearest K similiar user
        for i in range(self.k):
            totalDistance += nearest[i][1]
        if totalDistance == 0.0:
            totalDistance = 1.0

        # recommend book for similiar user sort by R
        for i in range(self.k):
            # similiar in [0,0]
            weight = nearest[i][1] / totalDistance

            # name of i (user)
            name = nearest[i][0]

            # user i data
            neighborRatings = self.data[name]

            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist] * weight)
                    else:
                        recommendations[artist] = (recommendations[artist] + neighborRatings[artist] * weight)

        recommendations = list(recommendations.items())
        recommendations = [(self.convertProductID2name(k), v) for (k, v) in recommendations]

        # sort
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)

        return recommendations[:self.n], nearest


def adjustrecommend(id):
    bookid_list = []
    r = recommender(users)
    k, nearuser = r.recommend("%s" % id)
    for i in range(len(k)):
        bookid_list.append(k[i][0])
    return bookid_list, nearuser[:15]  # bookid_list include id，nearuser[:15] from 15 nearest users


'''
bookid_list,near_list =MRE2.adjustrecommend("100000004")  
print ("near_list:",near_list)
print ("bookid_list:",bookid_list)

'''
