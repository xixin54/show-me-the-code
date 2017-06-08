import math
import platform

import numpy as np
import scipy.spatial.distance as distance

'''
a = np.array([0.1, 0.2])
b = np.array([0.3, 0.4])
c = 1 - distance.cosine(a, b)
print(c)
'''

## load data
srcfile = r"C:\Users\siege\Desktop\crd2.txt" if platform.system() == "Windows" else "/home/zkpk/Desktop/wfsiege/clnt_merch_count.txt"
fp = open(srcfile, "r")
users = {}
# txndt = {}

'''
for line in fp:
    lines = line.strip().split()
    if lines[0] not in users:
        users[lines[0]] = {}
    users[lines[0]][lines[1]] = float(lines[2])
    # print(lines)
print("data loaded")
'''

# print(users['100000005'])
# c = type(users)
# print(c)




def readFile(filename: object) -> object:
    contents = []
    f = open(filename, "r")
    contents = f.readlines()
    f.close()
    return contents


us2 = readFile(srcfile)
# print(us2)

def getRatingInfo(ratings):
    rates = []
    for line in ratings:
        rate = line.split("\t")
        rates.append([int(rate[0]), int(rate[1]), int(rate[2])])
    return rates


ratg1 = getRatingInfo(us2)
#print(ratg1)

# 生成用户评分数据结构
userDict = {}
itemUser = {}


def getUserScoreDataStructure(rates: object) -> object:
    # userDict[2]=[(1,5),(4,2)].... 表示用户2对Item1的评分是5，对Item4的评分是2
    userDict = {}
    itemUser = {}
    for k in rates:
        user_rank = (k[1], k[2])
        if k[0] in userDict:
            userDict[k[0]].append(user_rank)
        else:
            userDict[k[0]] = [user_rank]

        if k[1] in itemUser:
            itemUser[k[1]].append(k[0])
        else:
            itemUser[k[1]] = [k[0]]
    return userDict, itemUser


userDict1, itemUser1 = getUserScoreDataStructure(ratg1)


#print(userDict1,itemUser1)


def getCosDist(user1, user2):
    sum_x = 0.0
    sum_y = 0.0
    sum_x1 = 0.0
    sum_y1 = 0.0
    sum_xy = 0.0
    # print( user2)
    for key1 in user1:
        # print(11111)
        #sum_x1 += key1[1] * key1[1]
        #print(sum_x1)
        for key2 in user2:
            #print(key2)
            #sum_y1 += key2[1] * key2[1]
            #print(sum_y1)
            if key1[0] == key2[0]:
                sum_xy += key1[1] * key2[1]
                #### sum_xy += 1
                '''now is used value to multiply, instead we could use  1 to effect as distinct or other rank value
                test case found that , no distinct 用户相似度 离散程度更大
                '''
    #print(sum_xy)
    if sum_xy == 0.0:
        print("user item cross got a zero")
        print(sum_xy)
        return 0
    else:
        for key1 in user1:
            sum_x += key1[1] * key1[1]
            #### sum_x += 1
        for key2 in user2:
            #print(key2[0], key2[1])
            sum_y += key2[1] * key2[1]
            #### sum_y += 1
    #print(sum_x)
    #print(sum_y)

            #print(key2[1]*key2[1])
    demo = math.sqrt(sum_x * sum_y)
    #print(sum_xy / demo)
    return sum_xy / demo


def getNearestNeighbor(userId, userDict, itemUser):
    neighbors = []
    for item in userDict[userId]:
        #print(item)
        for neighbor in itemUser[item[0]]:  ## 待优化
            #print(itemUser)
            #print(item[0])
            #print(itemUser[item[0]])
            if neighbor != userId and neighbor not in neighbors:
                neighbors.append(neighbor)
                #print(neighbors)

    neighbors_dist = []
    for neighbor in neighbors:
        dist = getCosDist(userDict[userId], userDict[neighbor])
        #print(userDict[userId], userDict[neighbor])
        neighbors_dist.append([dist, neighbor])
        #print(neighbors_dist)
    neighbors_dist.sort(reverse=True)
    print("\n Nearest Neighbors order by distance")
    #print(neighbors_dist)
    return neighbors_dist


#gnn1 = getNearestNeighbor(100000004,userDict1,itemUser1)  ## test case over
#print(gnn1)

def recommendByUserFC(filename: object, userId: object, k: object = 50) -> object:
    contents = readFile(filename)  # 读取文件
    rates = getRatingInfo(contents)  # 文件格式数据转化为二维数组
    userDict, itemUser = getUserScoreDataStructure(rates)  # 格式化成字典数据
    neighbors = getNearestNeighbor(userId, userDict, itemUser)[:k]  # 找邻居
    #print(neighbors)
    #print(userDict[userId])

    '''
    Itemd = {}
    Itemd1 = []
    for itemd in userDict[userId]:
        #print(itemd[0])
        Itemd[itemd[0]]=itemd[1]
        Itemd1.append(itemd[0])
        #if item[0] not in itemd
    #print(Itemd1)
    '''

    recommand_dict = {}  # 建立推荐字典
    recommand_dict1 = {}
    for neighbor in neighbors:
        neighbor_user_id = neighbor[1]
        #print(neighbor[1])
        items = userDict[neighbor_user_id]
        #print(items)
        #print(userDict[userId])
        for item in items:
            if item not in userDict[userId]:
                if item[0] not in recommand_dict:# and item[0] not in Itemd:
                    #print(type(userDict[userId]))
                    #print(type(userDict[userId]))
                    recommand_dict[item[0]] = neighbor[0]  # need to be updated for rate
                    #### below for + rank value -- not distinct
                    recommand_dict1[item[0]] = neighbor[0]*item[1]
                    # print(111)
                    # print(recommand_dict[item[0]],item[0])
                else:
                    recommand_dict[item[0]] += neighbor[0]  ## together with above
                    #### below for + rank value -- not distinct
                    recommand_dict1[item[0]] += neighbor[0] * item[1]
                    # print(222)
                    # print(recommand_dict[item[0]], item[0])



                # 建立推荐列表
    recommand_list = []
    for key in recommand_dict:
        recommand_list.append([recommand_dict[key], key])
    recommand_list.sort(reverse=True)
    #print(recommand_list)

    recommand_list1 = []
    for key in recommand_dict1:
        recommand_list1.append([recommand_dict1[key], key])
    recommand_list1.sort(reverse=True)
    #print(recommand_list1)

    user_items = [k[0] for k in userDict[userId]]
    # print(user_items)
    rec_items = [k[1] for k in recommand_list]
    # print(rec_items)

    #recommend_list1 = [k if k in rec_items and k not in user_items]
    #print(recommend_list1)

    ####
    return [k[1] for k in recommand_list1], user_items, itemUser, neighbors
    #return [k[1] for k in recommand_list], user_items, itemUser, neighbors



recommend_list, user_items, itemUser, neighbors = recommendByUserFC(srcfile,100000004, 50)


print(recommend_list[:20])

rec_out = {}
for i in range(100000001,100000011):
    recommend_list, user_items, itemUser, neighbors = recommendByUserFC(srcfile,i , 50)
    rec_out[i]=recommend_list[:20]
with open('output.txt','w') as fp:
    fp.write((str(rec_out)))
    #fp.write(str(user_items)+'\n')
    #fp.write(itemUser+'\n')
    #fp.write(neighbors+'\n')
    fp.close()
# 获取产品的列表
def getItemList(filename):
    contents = readFile(filename)
    Item_info = {}
    for item in contents:
        single_info = item.split("|")
        Item_info[int(single_info[0])] = single_info[1:]
    return items_info


# gml = getItemList(srcfile)

'''
def computeNearestNeighbor(self, username):
    dist = []
    for instance in self.data:
        if dist != username:
            dist = self.fn(self.data[username], self.data[instance])
            dist.append((instance, dist))
            dist.sort(key=lambda artistTuple: artistTuple[1], reverse=True)


print("\nnow waht")
list1 = []
print(list1)
# list = computeNearestNeighbor('100000004')

'''