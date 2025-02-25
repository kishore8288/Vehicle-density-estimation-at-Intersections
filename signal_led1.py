from ultralytics import YOLO
import RPi.GPIO as gpio
import time
import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt
gpio.cleanup()

# Taking the image data from files
r1,y1,g1,r2,y2,g2,r3,y3,g3,r4,y4,g4 = 2,3,4,14,15,18,17,27,22,10,9,11
images = os.path.join('/home/pi/Images')
model = YOLO('yolov8n.pt')
gpio.setmode(gpio.BCM)
gpio.setup(r1,gpio.OUT)
gpio.setup(r2,gpio.OUT)
gpio.setup(r3,gpio.OUT)
gpio.setup(r4,gpio.OUT)
gpio.setup(g1,gpio.OUT)
gpio.setup(g2,gpio.OUT)
gpio.setup(g3,gpio.OUT)
gpio.setup(g4,gpio.OUT)
gpio.setup(y1,gpio.OUT)
gpio.setup(y2,gpio.OUT)
gpio.setup(y3,gpio.OUT)
gpio.setup(y4,gpio.OUT)

gpio.output(r1,gpio.LOW)
gpio.output(r2,gpio.LOW)
gpio.output(r3,gpio.LOW)
gpio.output(r4,gpio.LOW)
gpio.output(g1,gpio.LOW)
gpio.output(g2,gpio.LOW)
gpio.output(g3,gpio.LOW)
gpio.output(g4,gpio.LOW)
gpio.output(y1,gpio.LOW)
gpio.output(y2,gpio.LOW)
gpio.output(y3,gpio.LOW)
gpio.output(y4,gpio.LOW)

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

def light(ind,count,ind1,support):
    if support == 0:
        if (ind == 0):
            gpio.output(y1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            print("Lane ",ind+1," ready to go ...")
            time.sleep(10)
            gpio.output(y1,gpio.LOW)
            print("Green For Lane ",(ind+1),".......")
            gpio.output(g1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            time.sleep(count-10)
            if (ind1 == 1):
                gpio.output(r2,gpio.LOW)
                gpio.output(g1,gpio.HIGH)
                gpio.output(y2,gpio.HIGH)
                gpio.output(r3,gpio.HIGH)
                gpio.output(r4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 2):
                gpio.output(r3,gpio.LOW)
                gpio.output(g1,gpio.HIGH)
                gpio.output(r2,gpio.HIGH)
                gpio.output(y3,gpio.HIGH)
                gpio.output(r4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 3):
                gpio.output(r4,gpio.LOW)
                gpio.output(g1,gpio.HIGH)
                gpio.output(r2,gpio.HIGH)
                gpio.output(r3,gpio.HIGH)
                gpio.output(y4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            gpio.output(g1,gpio.LOW)
            gpio.output(r2,gpio.LOW)
            gpio.output(r3,gpio.LOW)
            gpio.output(r4,gpio.LOW)
            gpio.output(y2,gpio.LOW)
            gpio.output(y3,gpio.LOW)
            gpio.output(y4,gpio.LOW)
            time.sleep(0.5)
        elif (ind == 1):
            gpio.output(r1,gpio.HIGH)
            gpio.output(y2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            print("Lane ",ind+1," ready to go ...")
            time.sleep(10)
            gpio.output(y2,gpio.LOW)
            print("Green For Lane ",(ind+1),".......")
            gpio.output(r1,gpio.HIGH)
            gpio.output(g2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            time.sleep(count-10)
            if (ind1 == 0):
                gpio.output(r1,gpio.LOW)
                gpio.output(y1,gpio.HIGH)
                gpio.output(g2,gpio.HIGH)
                gpio.output(r3,gpio.HIGH)
                gpio.output(r4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 2):
                gpio.output(r3,gpio.LOW)
                gpio.output(r1,gpio.HIGH)
                gpio.output(g2,gpio.HIGH)
                gpio.output(y3,gpio.HIGH)
                gpio.output(r4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 3):
                gpio.output(r4,gpio.LOW)
                gpio.output(r1,gpio.HIGH)
                gpio.output(g2,gpio.HIGH)
                gpio.output(r3,gpio.HIGH)
                gpio.output(y4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            gpio.output(r1,gpio.LOW)
            gpio.output(g2,gpio.LOW)
            gpio.output(r3,gpio.LOW)
            gpio.output(r4,gpio.LOW)
            gpio.output(y1.gpio.LOW)
            gpio.output(y3,gpio.LOW)
            gpio.output(y4,gpio.LOW)
            time.sleep(0.5)
        elif (ind == 2):
            gpio.output(r1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(y3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            print("Lane ",ind+1," ready to go ...")
            time.sleep(10)
            gpio.output(y3,gpio.LOW)
            print("Green For Lane ",(ind+1),".......")
            gpio.output(r1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(g3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            time.sleep(count-10)
            if (ind1 == 0):
                gpio.output(r1,gpio.LOW)
                gpio.output(y1,gpio.HIGH)
                gpio.output(r2,gpio.HIGH)
                gpio.output(g3,gpio.HIGH)
                gpio.output(r4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 1):
                gpio.output(r2,gpio.LOW)
                gpio.output(r1,gpio.HIGH)
                gpio.output(y2,gpio.HIGH)
                gpio.output(g3,gpio.HIGH)
                gpio.output(r4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 3):
                gpio.output(r4,gpio.LOW)
                gpio.output(r1,gpio.HIGH)
                gpio.output(r2,gpio.HIGH)
                gpio.output(g3,gpio.HIGH)
                gpio.output(y4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            gpio.output(r1,gpio.LOW)
            gpio.output(r2,gpio.LOW)
            gpio.output(g3,gpio.LOW)
            gpio.output(r4,gpio.LOW)
            gpio.output(y1,gpio.LOW)
            gpio.output(y2,gpio.LOW)
            gpio.output(y4,gpio.LOW)
            time.sleep(0.5)
        elif (ind == 3):
            gpio.output(r1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(y4,gpio.HIGH)
            print("Lane ",ind+1," ready to go ...")
            time.sleep(10)
            gpio.output(y4,gpio.LOW)
            print("Green For Lane ",(ind+1),".......")
            gpio.output(r1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(g4,gpio.HIGH)
            time.sleep(count-10)
            if (ind1 == 0):
                gpio.output(r1,gpio.LOW)
                gpio.output(y1,gpio.HIGH)
                gpio.output(r2,gpio.HIGH)
                gpio.output(r3,gpio.HIGH)
                gpio.output(g4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 1):
                gpio.output(r2,gpio.LOW)
                gpio.output(r1,gpio.HIGH)
                gpio.output(y2,gpio.HIGH)
                gpio.output(r3,gpio.HIGH)
                gpio.output(g4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 2):
                gpio.output(r3,gpio.LOW)
                gpio.output(r1,gpio.HIGH)
                gpio.output(r2,gpio.HIGH)
                gpio.output(y3,gpio.HIGH)
                gpio.output(g4,gpio.HIGH)
                print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            gpio.output(r1,gpio.LOW)
            gpio.output(r2,gpio.LOW)
            gpio.output(r3,gpio.LOW)
            gpio.output(g4,gpio.LOW)
            gpio.output(y1,gpio.LOW)
            gpio.output(y2,gpio.LOW)
            gpio.output(y3,gpio.LOW)
            time.sleep(0.5)
    elif support != 0:
        if (ind == 0):
            gpio.output(g1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            print("Green For Lane ",(ind+1),".......")
            time.sleep(count-10)
            if (ind1 == 1):
                if support != 3:
                    gpio.output(r2,gpio.LOW)
                    gpio.output(g1,gpio.HIGH)
                    gpio.output(y2,gpio.HIGH)
                    gpio.output(r3,gpio.HIGH)
                    gpio.output(r4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 2):
                if support != 3:
                    gpio.output(r3,gpio.LOW)
                    gpio.output(g1,gpio.HIGH)
                    gpio.output(r2,gpio.HIGH)
                    gpio.output(y3,gpio.HIGH)
                    gpio.output(r4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 3):
                if support != 3:
                    gpio.output(r4,gpio.LOW)
                    gpio.output(g1,gpio.HIGH)
                    gpio.output(r2,gpio.HIGH)
                    gpio.output(r3,gpio.HIGH)
                    gpio.output(y4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            gpio.output(g1,gpio.LOW)
            gpio.output(r2,gpio.LOW)
            gpio.output(r3,gpio.LOW)
            gpio.output(r4,gpio.LOW)
            gpio.output(y2,gpio.LOW)
            gpio.output(y3,gpio.LOW)
            gpio.output(y4,gpio.LOW)
            time.sleep(0.5)
        elif (ind == 1):
            gpio.output(r1,gpio.HIGH)
            gpio.output(g2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            print("Green For Lane ",(ind+1),".......")
            time.sleep(count-10)
            if (ind1 == 0):
                if support != 3:
                    gpio.output(r1,gpio.LOW)
                    gpio.output(y1,gpio.HIGH)
                    gpio.output(g2,gpio.HIGH)
                    gpio.output(r3,gpio.HIGH)
                    gpio.output(r4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 2):
                if support != 3:
                    gpio.output(r3,gpio.LOW)
                    gpio.output(r1,gpio.HIGH)
                    gpio.output(g2,gpio.HIGH)
                    gpio.output(y3,gpio.HIGH)
                    gpio.output(r4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 3):
                if support != 3:
                    gpio.output(r4,gpio.LOW)
                    gpio.output(r1,gpio.HIGH)
                    gpio.output(g2,gpio.HIGH)
                    gpio.output(r3,gpio.HIGH)
                    gpio.output(y4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            gpio.output(r1,gpio.LOW)
            gpio.output(g2,gpio.LOW)
            gpio.output(r3,gpio.LOW)
            gpio.output(r4,gpio.LOW)
            gpio.output(y1,gpio.LOW)
            gpio.output(y3,gpio.LOW)
            gpio.output(y4,gpio.LOW)
            time.sleep(0.5)
        elif (ind == 2):
            gpio.output(r1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(g3,gpio.HIGH)
            gpio.output(r4,gpio.HIGH)
            print("Green For Lane ",(ind+1),".......")
            time.sleep(count-10)
            if (ind1 == 0):
                if support != 3:
                    gpio.output(r1,gpio.LOW)
                    gpio.output(y1,gpio.HIGH)
                    gpio.output(r2,gpio.HIGH)
                    gpio.output(g3,gpio.HIGH)
                    gpio.output(r4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 1):
                if support != 3:
                    gpio.output(r2,gpio.LOW)
                    gpio.output(r1,gpio.HIGH)
                    gpio.output(y2,gpio.HIGH)
                    gpio.output(g3,gpio.HIGH)
                    gpio.output(r4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 3):
                if support != 3:
                    gpio.output(r4,gpio.LOW)
                    gpio.output(r1,gpio.HIGH)
                    gpio.output(r2,gpio.HIGH)
                    gpio.output(g3,gpio.HIGH)
                    gpio.output(y4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            gpio.output(r1,gpio.LOW)
            gpio.output(r2,gpio.LOW)
            gpio.output(g3,gpio.LOW)
            gpio.output(r4,gpio.LOW)
            gpio.output(y1,gpio.LOW)
            gpio.output(y2,gpio.LOW)
            gpio.output(y4,gpio.LOW)
            time.sleep(0.5)
        elif (ind == 3):
            gpio.output(r1,gpio.HIGH)
            gpio.output(r2,gpio.HIGH)
            gpio.output(r3,gpio.HIGH)
            gpio.output(g4,gpio.HIGH)
            print("Green For Lane ",(ind+1),".......")
            time.sleep(count-10)
            if (ind1 == 0):
                if support != 3:
                    gpio.output(r1,gpio.LOW)
                    gpio.output(y1,gpio.HIGH)
                    gpio.output(r2,gpio.HIGH)
                    gpio.output(r3,gpio.HIGH)
                    gpio.output(g4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 1):
                if support != 3:
                    gpio.output(r2,gpio.LOW)
                    gpio.output(r1,gpio.HIGH)
                    gpio.output(y2,gpio.HIGH)
                    gpio.output(r3,gpio.HIGH)
                    gpio.output(g4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            elif (ind1 == 2):
                if support != 3:
                    gpio.output(r3,gpio.LOW)
                    gpio.output(r1,gpio.HIGH)
                    gpio.output(r2,gpio.HIGH)
                    gpio.output(y3,gpio.HIGH)
                    gpio.output(g4,gpio.HIGH)
                    print("Lane ",ind1+1," ready to go ...")
                time.sleep(10)
            gpio.output(r1,gpio.LOW)
            gpio.output(r2,gpio.LOW)
            gpio.output(r3,gpio.LOW)
            gpio.output(g4,gpio.LOW)
            gpio.output(y1,gpio.LOW)
            gpio.output(y2,gpio.LOW)
            gpio.output(y3,gpio.LOW)
            time.sleep(0.5)

def ind_match(old_list,max_val):
    for i,value in enumerate(old_list):
        if(value == max_val):
            return i

"""
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
    while (s<=total+10):
        if (t[0]-s<0):
            print("Lane ",a[0]+1," : ",t1[3]-(s-(s-1)),"\t",end = '')
            t1[3] = t1[3]-1
        else:
            print("Lane ",a[0]+1," : ",t[0]-s,"\t",end = '')
        if (t[1]-s<0):
            print("Lane ",a[1]+1," : ",t2[3]-(s-(s-1)),"\t",end = '')
            t2[3] = t2[3]-1
        else:
            print("Lane ",a[1]+1," : ",t[1]-s,"\t",end = '')
        if (t[2]-s<0):
            print("Lane ",a[2]+1," : ",t3[3]-(s-(s-1)),"\t",end = '')
            t3[3] = t3[3]-1
        else:
            print("Lane ",a[2]+1," : ",t[2]-s,"\t",end = '')
        if (t[3]-s<0):
            print("Lane ",a[3]+1," : ",t4[3]-(s-(s-1)),"\t",end = '')
            t4[3] = t4[3]-1
        else:
            print("Lane ",a[3]+1," : ",t[3]-s,"\t")
        s = s+1
        time.sleep(1)
"""

def sort(arr):
    s = list()
    for l in range(len(arr)):
        a = list()
        for i in range(len(arr[l])):
            for j in range(len(arr[l])):
                if (arr[i][j] == max(arr[l])):
                    a.append(arr[i][j])
                    arr.remove(arr[i][j])
        s.append(a)
    return s

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

while True :
    key = list()
    timer = list()
    tempo = list()
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

    print(tempo,'\t',timer)
   # for x in timer:
   #     count(x)

    for l in range(len(tempo)):
        sort_arr = tempo[l][:]
        sort_arr.sort(reverse = True)
        support = 0
        for i in range(len(tempo[l])):
            max_value = max(timer[l])
            ind = ind_match(tempo[l],max_value)
            print('Maximum timer allocated is : ',max_value + 10 if support == 0 else max_value,'\t for lane ',(ind+1))
            if (i == len(tempo[l])-1):
                ind2 = 0
            elif (i <= len(tempo[l])-1):
                for j in range(len(sort_arr)):
                    if (max_value == sort_arr[j]):
                        ind2 = j+1
                        break
            ind1 = ind_match(tempo[l],sort_arr[ind2])
            light(ind,max_value,ind1,support)
            support += 1
            timer[l].remove(max_value)

    gpio.output(r1,gpio.LOW)
    gpio.output(r2,gpio.LOW)
    gpio.output(r3,gpio.LOW)
    gpio.output(r4,gpio.LOW)
    gpio.output(g1,gpio.LOW)
    gpio.output(g2,gpio.LOW)
    gpio.output(g3,gpio.LOW)
    gpio.output(g4,gpio.LOW)

gpio.cleanup()
