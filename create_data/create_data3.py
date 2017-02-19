#coding=utf-8
import datetime
import random
import math

def avg2xy(avg):
	if avg > 360:
		avg -= 360
	if avg < 0:
		avg += 360

	rad = avg / 180 * math.pi

	dist = (60+random.uniform(-5,5)) / 12

	dx = dist * math.cos(rad)
	dy = dist * math.sin(rad)

	dx = dx / 111
	dy = dy / (111*math.cos(math.pi/6))

	return dx,dy

driver_num = 80
car_num = 50

driver_pool = [i for i in range(0,driver_num)]
car_pool = [i for i in range(0,car_num)]

day_num = 30
oneday_carnum = 30

origin_time = datetime.datetime(2016,11,16,9,0,0)

begX = 105
endX = 112
begY = 27
endY = 33

car_info = []

for i in range(car_num):
	x = random.uniform(begX, endX)
	y = random.uniform(begY, endY)
	oil = random.uniform(100,200)
	car_info.append([x,y,oil])


with open("c.csv",'w') as f:
	for day in range(day_num):
		userd_driver = []
		userd_car = []
		for i in range(oneday_carnum):
			idriver = random.randint(0,len(driver_pool)-1)
			icar = random.randint(0,len(car_pool)-1)

			dirver_id = driver_pool[idriver]
			car_id = car_pool[icar]

			userd_driver.append(dirver_id)
			userd_car.append(car_id)

			driver_pool.pop(idriver)
			car_pool.pop(icar)

			begTime = origin_time + datetime.timedelta(days=day, minutes=random.randint(0,30))
			endTime = origin_time + datetime.timedelta(days=day, hours=8, minutes=random.randint(0,30))

			dst_avg = random.uniform(0,360)

			if car_info[car_id][2] < 100:
				car_info[car_id][2] += 100

			nowTime = begTime
			while nowTime < endTime:
				now_avg = dst_avg + random.uniform(-5,5)
				dx,dy = avg2xy(now_avg)
				car_info[car_id][0] += dx
				car_info[car_id][1] += dy
				car_info[car_id][2] -= 0.7 + random.uniform(-0.05,0.05)

				f.write("%d,%d,%f,%f,%f,%f,%s\n" % (dirver_id,car_id,car_info[car_id][0],car_info[car_id][1],car_info[car_id][2],random.uniform(16,26),str(nowTime)))

				nowTime += datetime.timedelta(minutes=5)

		driver_pool.extend(userd_driver)
		car_pool.extend(userd_car)