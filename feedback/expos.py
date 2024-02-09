# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 15:40:02 2019

@author: Rohith
"""

#%%
import csv
import numpy as np
import matplotlib.pyplot as plt
#%%
def load_csv(file):
    data=[]
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

#%%
col = "iitpkd23"
data = load_csv("iitpkd23.csv")
del data[0]
num_samples = np.shape(data)[0]
data = np.array(data)
data = data[data[:,2]>"2"] #eliminating samples below phase 2
num_samples = np.shape(data)[0]
phase5 = data[data[:,2]>="5"]
num_samples5 = np.shape(phase5)[0]
#%%
#colors=['brown', 'g', 'b', 'y', 'magenta', 'c', 'grey', 'r']
colors=['yellowgreen','orchid', 'crimson', 'royalblue','cyan' , 'red', 'grey', 'burlywood', 'salmon']
#%%
#Q1
#labels = ["Phase "+str(i) for i in range(0,8)]
labels = [str(i) for i in range(0,8)]
labels.reverse()
count=[]
labels1=[]
for label in labels:
    num = sum(data[:,2]==label)
    if num!=0:
        count.append(num)
        labels1.append(label)


fig1, ax1 = plt.subplots()
ax1.pie(count, autopct='%.0f%%', colors=colors)
ax1.axis('equal')
ax1.legend(labels1, loc='upper right', bbox_to_anchor=(1.1, 0.8))
plt.title("Number of phases completed by all students.", y=-0.05)
plt.savefig(col+"q1.png", bbox_inches='tight', transparent=True)
plt.close(fig1)
#%%
#Q2
labels = ["< 5 Hours", "5-10 Hours", "10-15 Hours", "> 15 Hours"]
count=[]
for label in labels:
    count.append(sum(data[:,3]==label))

count5=[]
for label in labels:
    count5.append(sum(phase5[:,3]==label))

plt.figure(1, figsize=(10,5))
ax1 = plt.subplot(121)
ax1.pie(count, autopct='%.0f%%', colors=colors)
ax1.axis('equal')
plt.title("All Students", y=-0.01)

ax2 = plt.subplot(122)
ax2.pie(count5, autopct='%.0f%%', colors=colors)
ax2.axis('equal')
plt.title("Students who completed Phase 5 and above", y=-0.01)
plt.legend(labels, loc='lower left', bbox_to_anchor=(0.8, 0.8))
plt.savefig(col+"q2.png", bbox_inches='tight', transparent=True)
plt.close()

#%%
#Q3
labels=["100% Sufficient", ">90% Sufficient", ">75% Sufficient", ">50% Sufficient"]
count=[]
for label in labels:
    count.append(sum(data[:,4]==label))

count5=[]
for label in labels:
    count5.append(sum(phase5[:,4]==label))

plt.figure(1, figsize=(10,5))
ax1 = plt.subplot(121)
ax1.pie(count, autopct='%.0f%%', colors=colors)
ax1.axis('equal')
plt.title("All Students", y=-0.01)

ax2 = plt.subplot(122)
ax2.pie(count5, autopct='%.0f%%', colors=colors)
ax2.axis('equal')
plt.title("Students who completed Phase 5 and above", y=-0.01)
plt.legend(labels, loc='lower left', bbox_to_anchor=(0.8, 0.8))
plt.savefig(col+"q3.png", bbox_inches='tight', transparent=True)
plt.close()

#%%
#Q4
labels = ["Those who have done the lab have a clear advantage in understanding the theory", "Those who have done the lab have a minor advantage in understanding the theory"]
count=[]
for label in labels:
    count.append(sum(data[:,5]==label))

count5=[]
for label in labels:
    count5.append(sum(phase5[:,5]==label))

plt.figure(1, figsize=(10,5))
ax1 = plt.subplot(121)
ax1.pie(count, autopct='%.0f%%', colors=colors)
ax1.axis('equal')
plt.title("All Students", y=-0.01)
plt.legend(labels, loc='lower left', bbox_to_anchor=(0, 1))

ax2 = plt.subplot(122)
ax2.pie(count5, autopct='%.0f%%', colors=colors)
ax2.axis('equal')
plt.title("Students who completed Phase 5 and above", y=-0.01)
#plt.legend(labels, loc='lower left', bbox_to_anchor=(0, 0))
plt.savefig(col+"q4.png", bbox_inches='tight', transparent=True)
plt.close()

#%%
#Q5
labels = ["The lab brought a considerable improvement", "The lab brought about moderate improvement", "This lab did not bring about a serious improvement"]
count=[]
for label in labels:
    count.append(sum(data[:,6]==label))

count5=[]
for label in labels:
    count5.append(sum(phase5[:,6]==label))

plt.figure(1, figsize=(10,5))
ax1 = plt.subplot(121)
ax1.pie(count, autopct='%.0f%%', colors=colors)
ax1.axis('equal')
plt.title("All Students", y=-0.01)
plt.legend(labels, loc='lower left', bbox_to_anchor=(0, 1))

ax2 = plt.subplot(122)
ax2.pie(count5, autopct='%.0f%%', colors=colors)
ax2.axis('equal')
plt.title("Students who completed Phase 5 and above", y=-0.01)
#plt.legend(labels, loc='lower left', bbox_to_anchor=(0, 0))
plt.savefig(col+"q5.png", bbox_inches='tight', transparent=True)
plt.close()

#%%
#Q6
labels=["Sufficient", "Computer Organization/Hardware", "Compilers", "Datastructures", "Programming"]
count=[]
for label in labels:
    count.append(sum([label in val for val in data[:,7]]))

count5=[]
for label in labels:
    count5.append(sum([label in val for val in phase5[:,7]]))

labels[1]="Computer Organization/\nHardware"
x=np.arange(5)
plt.figure(1, figsize=(10,5))
ax1 = plt.subplot(121)
rects1=ax1.bar(x, count)
for rect in rects1:
    height = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2., 1*height,
            '%.2f' % ((height*100)/num_samples) + "%", ha='center', va='bottom')
plt.xticks(x,labels)
plt.setp(ax1.get_xticklabels(), rotation=90, horizontalalignment='center')
plt.title("All Students")

ax2 = plt.subplot(122)
rects2=ax2.bar(x, count5)
for rect in rects2:
    height = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2., 1*height,
            '%.2f' % ((height*100)/num_samples5) + "%", ha='center', va='bottom')
plt.xticks(x,labels)
plt.setp(ax2.get_xticklabels(), rotation=90, horizontalalignment='center')
plt.title("Students who completed Phase 5 and above")
plt.savefig(col+"q6.png", bbox_inches='tight', transparent=True)
plt.close()

#%%
