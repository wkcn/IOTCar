import random

numberOfCar=80

f=open("xing.txt",'rb')
u = f.read().decode('utf-8')#.encode('GBK')
xing=u.split(',')

f=open("ming.txt",'rb')
u = f.read().decode('utf-8')#.encode('GBK')
ming=u.split(',')

f=open('driver.txt','w')

tel=15900000000

for i in range(numberOfCar):
    j=random.randint(0,len(xing)-1)
    f.write(xing[j])
    j=random.randint(0,len(ming)-1)
    f.write(ming[j]+',')
    tel+=random.randint(0,90000000/numberOfCar)
    f.write(str(tel)+'\n')

