'''

# 源文件空格分割，训练集、测试集80：20

from sklearn import cross_validation

c = []
filename = r"C:\Users\siege\Desktop\crd2.txt"
out_train = open(r'C:\Users\siege\Desktop\train.txt', 'w')
out_test = open(r'C:\Users\siege\Desktop\test.txt', 'w')
for line in open(filename):
    items = line.strip().split()
    c.append(items)

c_train, c_test = cross_validation.train_test_split(c, test_size=0.2)
for i in c_train:
    out_train.write(' '.join(i) + '\n')
assert isinstance(c_test, object)
for i in c_test:
    out_test.write(' '.join(i) + '\n')

'''


from impala.dbapi import connect
conn = connect(host='localhost', port=10000) # ?
cursor = conn.cursor()
cursor.execute('SELECT clnt_nbr,merch_cde,count(*) fiew , max(Txnt_dt) FROM INT_CRD_TXN')
#print(cursor.description)  # prints the result set's schema
print(1)
results1 = cursor.fetchall()


##
cursor.execute('select merch_cde,max(fiew) from SELECT clnt_nbr,merch_cde,count(*) fiew , max(Txnt_dt) FROM INT_CRD_TXN')
results2 = cursor.fetchall()
for row in results2:
    process(row)


def transDate(date):
    date_view = 1
    if date in range(20161201,20161230):
        date_view = 4
    elif date in range(20161001,20161130):
        date_view = 3
    elif date in range(20160601,201610930):
        date_view = 2
    elif date in range(20160101,20160630):
        date_view = 1
    return date_view

def transCount(review_count,new_view_count):
    #print(1)
    fiew = 0
    if review_count > 5:
        for new_view_count_count in range(0,round(review_count/11)):
            fiew = 1
        for new_view_count in range(round(review_count/11),round(3*review_count/11)):
            fiew = 2
        for new_view_count in range( round(3 *review_count / 11), round(6 * review_count / 11)):
            fiew = 3
        for new_view_count in range(round(6* review_count / 11), round(review_count)):
            fiew = 4
    return fiew

cursor.execute('SELECT clnt_nbr,merch_cde,count(*) fiew , max(Txnt_dt) date_ve FROM INT_CRD_TXN')

f = open("crd2.txt",'w')

for row in results1:  # need to modify probably
    #print(transDate(row[3]))
    #f.write(row[0],'\t'row[1],transDate(transDate(row[3])))
    #f.write(row[0],'\t'row[1],'\t'transDate(transDate(row[3]*transCount(2))))


#print(f)
