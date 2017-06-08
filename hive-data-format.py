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

