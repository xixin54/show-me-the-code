import numpy as np
import pandas as pd
from pandas import Series, DataFrame

#rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
rnames = ['user_id', 'movie_id', 'rating']
ratings = pd.read_table(r'C:\Users\siege\Desktop\crd2.txt', sep='\t', header=None, names=rnames)
print(ratings[:3])

data = ratings.pivot(index='user_id', columns='movie_id', valu








es='rating')
#print(data[:5])



''''''
foo = DataFrame(np.empty((len(data.index), len(data.index)), dtype=int), index=data.index, columns=data.index)
#print(foo)
for i in foo.index:
    for j in foo.columns:
        foo.ix[i, j] = data.ix[i][data.ix[j].notnull()].dropna().count()

for i in foo.index:
    foo.ix[i, i] = 0  # 先把对角线的值设为 0

ser = Series(np.zeros(len(foo.index)))

for i in foo.index:
    ser[i] = foo[i].max()  # 计算每行中的最大值 ===========error

print(ser.idxmax())  # 返回 ser 的最大值所在的行号
# 4169  --100000001

print(ser[100000001])  # 取得最大值
# 998  ---31.0


# get errors below
#foo[foo == 100000001][31].dropna()  # 取得另一个 user_id

'''
424     4169
Name: user_id, dtype: float64
'''

#print(data.ix[4169].corr(data.ix[424]))
# 0.45663851303413217

'''
test = data.reindex([424, 4169], columns=data.ix[4169][data.ix[424].notnull()].dropna().index)
#print（test）

test.ix[424].value_counts(sort=False).plot(kind='bar')
test.ix[4169].value_counts(sort=False).plot(kind='bar')

periods_test = DataFrame(np.zeros((20, 7)), columns=[10, 20, 50, 100, 200, 500, 998])
for i in periods_test.index:
    for j in periods_test.columns:
        sample = test.reindex(columns=np.random.permutation(test.columns)[:j])
        periods_test.ix[i, j] = sample.iloc[0].corr(sample.iloc[1])

print(periods_test[:5])

print(1)
periods_test.describe()


'''

check_size = 40
check = {}
check_data = data.copy()  # 复制一份 data 用于检验，以免篡改原数据

check_data = check_data.ix[check_data.count(axis=1) > 20]  # 滤除评价数小于200的用户
#print(check_data)
for user in np.random.permutation(check_data.index):
    movie = np.random.permutation(check_data.ix[user].dropna().index)[0]
    check[(user, movie)] = check_data.ix[user, movie]
    check_data.ix[user, movie] = np.nan
    check_size -= 1
    if not check_size:
        break

#print(3333)
corr = check_data.T.corr(min_periods=20)
corr_clean = corr.dropna(how='all')
corr_clean = corr_clean.dropna(axis=1, how='all')  # 删除全空的行和列
check_ser = Series(check)  # 这里是被提取出来的 1000 个真实评分
print(check_ser[:5])

result = Series(np.nan, index=check_ser.index)
for user, movie in result.index:  # 这个循环看着很乱，实际内容就是加权平均而已
    prediction = []
    if user in corr_clean.index:
        corr_set = corr_clean[user][corr_clean[user] > 0.1].dropna()  # 仅限大于 0.1 的用户
    else:
        continue
    for other in corr_set.index:
        if not np.isnan(data.ix[other, movie]) and other != user:  # 注意bool(np.nan)==True
            prediction.append((data.ix[other, movie], corr_set[other]))
    if prediction:
        result[(user, movie)] = sum([value * weight for value, weight in prediction]) / sum(
            [pair[1] for pair in prediction])

result.dropna(inplace=True)

print(len(result))  # 随机抽取的 1000 个用户中也有被 min_periods=200 刷掉的
# 862
print(result[:5])

'''
(23, 555)     3.967617
(33, 3363)    4.073205
(36, 2355)    3.903497
(53, 3605)    2.948003
(62, 1488)    2.606582
dtype: float64
'''
print(result.corr(check_ser.reindex(result.index)))
# 0.436227437429696
print((result - check_ser.reindex(result.index)).abs().describe())  # 推荐期望与实际评价之差的绝对值
'''
count    862.000000
mean       0.785337
std        0.605865
min        0.000000
25%        0.290384
50%        0.686033
75%        1.132256
max        3.629720
dtype: float64
'''


# do Rec
'''
corr = data.T.corr(min_periods=50)
corr_clean = corr.dropna(how='all')
corr_clean = corr_clean.dropna(axis=1, how='all')

lucky = np.random.permutation(corr_clean.index)[0]
print(lucky)

gift = data.ix[lucky]
gift = gift[gift.isnull()]  # 现在 gift 是一个全空的序列

corr_lucky = corr_clean[lucky].drop(lucky)  # lucky 与其他用户的相关系数 Series，不包含 lucky 自身
corr_lucky = corr_lucky[corr_lucky > 0.1].dropna()  # 筛选相关系数大于 0.1 的用户
for movie in gift.index:  # 遍历所有 lucky 没看过的电影
    prediction = []
    for other in corr_lucky.index:  # 遍历所有与 lucky 相关系数大于 0.1 的用户
        if not np.isnan(data.ix[other, movie]):
            prediction.append((data.ix[other, movie], corr_clean[lucky][other]))
    if prediction:
        gift[movie] = sum([value * weight for value, weight in prediction]) / sum([pair[1] for pair in prediction])

print(gift.dropna().order(ascending=False))  # 将 gift 的非空元素按降序排列

'''
