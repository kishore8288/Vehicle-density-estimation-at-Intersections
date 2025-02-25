from ultralytics import YOLO
import RPi.GPIO as gpio
import time
import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt
gpio.cleanup()

images = os.path.join('/home/pi/Images')
model = YOLO('yolov8n.pt')

classes = model.names
vehicles = ['person','car','bicycle','motorcycle','truck','bus']
dense_map = {0:'Extremely low',1:'Low',2:'Medium',3:'Close to high',
             4:'High',5:'Very high',6:'Extremely High'}

def img_counts(img_path):
    count = list()
    for i, img in enumerate(os.listdir(img_path)):
        img = cv.imread(os.path.join(img_path,img))
        re_img = img[int(img.shape[0]*0.25):,int(img.shape[1]*0.25):,:]
        res = model(re_img)
        v_counts = {cls:0 for cls in vehicles}
        for r in res:
            for box in r.boxes:
                ind = int(box.cls)
                match = classes[ind]
                if match in vehicles:
                    v_counts[match] += 1
            detect = r.plot()
            detect = cv.cvtColor(detect,cv.COLOR_BGR2RGB)
            plt.subplot(4,4,(i+1))
            plt.imshow(detect)
            plt.axis('off')
        count.append(v_counts)
    return count

def obj_counts(c):
    l_counts = list()
    s_counts = list()
    pedes = list()
    for i in c:
        count = i['truck'] + i['bus']
        l_counts.append(count)
        count = i['motorcycle'] + i['car'] + i['bicycle']
        s_counts.append(count)
        pedes.append(i['person'])
    return l_counts,s_counts,pedes

def selective(n_large,n_small,n_person):
    n_vehicles = n_large + n_small
    if n_vehicles>0 and n_vehicles<=10:
        if n_large == 0:
            return 0
        elif n_large >0 and n_large <=4:
            return 1
        else :
            return 2
    elif n_vehicles>10 and n_vehicles<=30:
        if n_large <= 4:
            return 2
        elif n_large > 4 and n_large <= 8:
            return 3
        else :
            return 4
    elif n_vehicles>30:
        if n_large <=8 :
            return 4
        elif n_large >8 and n_large <= 15:
            return 5
        else :
            return 6
    else :
        print('Invalid')

def max_time(max_val):
    for i in range(len(timer)):
        if (timer[i] == max_val):
            max_val = timer[i]
            return i,max

def ind_match(old_list,max_val):
    for i,value in enumerate(old_list):
        if(value == max_val):
            return i

def count(timer):
    coun = timer[:]
    a = list()
    while (len(coun)>0):
        m = max(coun)
        ind = ind_match(timer,m)
        if ind is not None:
            a.append(ind)
            coun.remove(m)
    t = list()
    print(len(a))
    print(len(timer))
    for i in range(len(a)):
        j = 0
        temp = 0
        while j<=i:
            temp = temp + timer[a[j]]
            j = j+1
        t.append(temp)
    total = sum(timer)
    s = 0
    t1 = t[:]
    t2 = t[:]
    t3 = t[:]
    t4 = t[:]
    print("Timings for Lanes : \n")
    while (s<=total+11):
        if (t[0]+10-s<0):
            print("Lane ",a[0]+1," :",t1[3]+10-(s-(s-1)),"\t",end = '')
            t1[3] = t1[3]-1
        else:
            print("Lane ",a[0]+1," :",t[0]+10-s,"\t",end = '')
        if (t[1]+10-s<0):
            print("Lane ",a[1]+1," :",t2[3]+10-(s-(s-1)),"\t",end = '')
            t2[3] = t2[3]-1
        else:
            print("Lane ",a[1]+1," :",t[1]+10-s,"\t",end = '')
        if (t[2]+10-s<0):
            print("Lane ",a[2]+1," :",t3[3]+10-(s-(s-1)),"\t",end = '')
            t3[3] = t3[3]-1
        else:
            print("Lane ",a[2]+1," :",t[2]+10-s,"\t",end = '')
        if (t[3]+10-s<0):
            print("Lane ",a[3]+1," :",t4[3]+10-(s-(s-1)),"\t",end = '')
            t4[3] = t4[3]-1
        else:
            print("Lane ",a[3]+1," :",t[3]+10-s,"\t")
        s = s+1
        time.sleep(1)

c = list()
for path in os.listdir(images):
    c.append(img_counts(os.path.join(images,path)))

large,small,ped = [],[],[]
for i,obj in enumerate(c):
    a = list()
    b = list()
    c = list()
    for j in range(len(obj)):
        a,b,c = obj_counts(obj)
    large.append(a)
    small.append(b)
    ped.append(c)

key = list()
timer = list()
tempo = list()

while True :
    for l in range(len(large)):
        tim = list()
        te = list()
        for i in range(len(large[l])):
            key.append(selective(large[l][i],small[l][i],ped[l][i]))
            t = (small[l][i]*2 + large[l][i]*3)//2
            tim.append(t)
            te.append(t)
            print(dense_map[key[i]])
        timer.append(tim)
        tempo.append(te)

    print("Timings for each lane : ",tempo)
    for x in timer:
        count(x)
