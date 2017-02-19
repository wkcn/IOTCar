import random

numberOfCar=50
cnPreFix='粤A'

f=open("carType.txt",'rb')
u = f.read().decode('utf-8')#.encode('GBK')
cartype=u.split(',')

f=open('table car.txt','w',encoding='utf-8')

number=10000
for i in range(50):
    j=random.randint(0,len(cartype)-1)
    f.write(cartype[j]+',')
    number+=random.randint(0,80000/numberOfCar)
    f.write(cnPreFix+str(number)+'\n')

print(cnPreFix)