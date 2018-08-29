#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 13:54:23 2018

@author: xaviervanegdom
"""

import xlsxwriter
from datetime import date, timedelta

# make a nice list of the dataset
def get_dataset_list(name):
    # load the datasets
    with open(name, 'r') as f:
        dataset = f.read()
    
    tempset, temprow, temp = [], [], ''
    
    for i in dataset:
        
        if i is ';':
            temprow.append(temp)
            temp = ''
            
        elif i is "\n":
            temprow.append(temp)
            tempset.append(temprow)
            temprow, temp = [], ''
        
        else:      
            temp += i
    
    temprow.append(temp)
    tempset.append(temprow)
    return tempset

def rotate_list(data, head):

    rotateSet = []
    for i in range(len(data[0])):
        temprow = []
        temprow.append(head[i])
        for row in data:
            temprow.append(row[i])
        rotateSet.append(temprow)
    return rotateSet

# create excelsheet
def create_excel(name, data, head):
    
    data = rotate_list(data, head)
    
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    
    row = 0
    
    for col, data in enumerate(data):
        worksheet.write_column(row, col, data)
        
    workbook.close()

# If you provide a list it stores the items before it deletes them
def delete_records(dataset, indexes, tempdataset=None,):
    minus = 0
    for index in indexes:
        index -= minus
        minus += 1
        
        if tempdataset != None: tempdataset.append(dataset[index])
        del dataset[index]  

# functions for step 5

# if a set is found, this will check how many subsets can be found in the set based on the PersonId
def check_sets(sets, dataset):
    
    usedrows = [] # to know wich rows have been part of a set
    for row in sets:
        
        tempset = [] # temp list to put the set in to append it to the dataset
        if row[6] == "NULL": # the last record of a set
            
            tempset.append(row)
            usedrows.append(row)
            
            for i in range(len(sets)): # the end of the set is unknow so whe go to all the rows to check if we find a new next record
                for extrarow in sets:
                    if tempset[-1][5] == extrarow[6]:  # check if column requestdate of the last know record of a set matches 
                                                       # a date at one the column IsMoved in one of the other records
                        tempset.append(extrarow)
                        usedrows.append(extrarow)
                        break
                    if extrarow[6] != 'NULL':
                        if check_one_minut_diffrence(tempset, extrarow):
                            tempset.append(extrarow)
                            usedrows.append(extrarow)
                            break
            
            save_set(tempset, dataset)
            
    for row in sets:
        if row not in usedrows:
            save_single_record(row, dataset)
        


# check if ther are sets based on the PersonID
def check_for_sets(row, dataset, newdataset):
    sets = [row] # to put all the rows in with the same ID to check for sets if len() = 1 then ther are no sets
    for rowextra in dataset:        
        if row != rowextra: # already has this row ofcours
            if row[2] == rowextra[2]: # if the same person if, then it goes in the set list
                sets.append(rowextra)
            
    if len(sets) > 1: # if there are more then one rows then it can contain multiple sets a function will check this
        check_sets(sets, newdataset)
    else :
        save_single_record(row, newdataset)
        
def save_set(setl, dataset):
    lastrecord = setl[0]
    
    count = 0
    for record in setl:
        count += int((record[7]))
    lastrecord[7] = count  
    
    #lastrecord.insert(6, setl[-1][5])
    lastrecord.append(len(setl)-1)
                  
    dataset.append(lastrecord)
                    
def save_single_record(record, dataset):
    #record.insert(6, "NULL") 
    record.append(0)
    dataset.append(record)

def check_one_minut_diffrence(temp, extrarow):
    timefirstpart = extrarow[6][:-1]
    timelastpart = str(int(extrarow[6][-1]) - 1)
    time = timefirstpart + timelastpart
    
    condition = False
    if temp[-1][5] == time:
        condition = True
    return condition 

# functions step 8
    
# Calculate the rate of hit found according to the given column if column = 1
def rate_of_hit(dataset, column, name, head):
    rate_of_hit = []
    for i in range(0, 28, 7): # days of the weeks up to 4 weeks
        hit = 0 # 1++ if people fall in the day range and the column = 1
        amount_of_tl = 0 # amount of poeple found
        for row in dataset:
            if i == 0: # 0 falls in week 1 what effectifly makes week 1 8 days long
                if int(row[9]) >= i and int(row[9]) <= i + 7: 
                    if row[column] == 1:
                        hit += 1
                    amount_of_tl += 1
            else: # if i != 0 then its not week one and the weeks are 7 days long
                if int(row[9]) > i and int(row[9]) <= i + 7: 
                    if row[column] == 1:
                        hit += 1
                    amount_of_tl += 1
                
        rate_of_hit.append((i, hit / amount_of_tl * 100, hit, amount_of_tl ))
    
    create_excel(name, rate_of_hit, head) 


# get the dataset
dataset = get_dataset_list('TrialLesson(orgineel).csv')
head = dataset[0]
del dataset[0]

# step 1
# delete records with IsDeleted != NULL
del head[6]
indexes = []
for i in range(len(dataset)):
    if dataset[i][6] != 'NULL':
        indexes.append(i)
    row = dataset[i]
    del row[6]
        
delete_records(dataset, indexes)

# step 2
# delete all records before a date
beforedate = date(2017, 4, 2)
indexes = []
for i in range(len(dataset)):
    if date(2000 + int(dataset[i][4][6:8]), int(dataset[i][4][3:5]), int(dataset[i][4][0:2])) < beforedate:
        indexes.append(i)

delete_records(dataset, indexes)

# step 3
# delete record if DateRequestedTrialLesson and IsMoved is the same 
indexes = []
for i in range(len(dataset)):
    if dataset[i][5] == dataset[i][6]: # DateRequestedTrialLesson and IsMoved
        indexes.append(i)

delete_records(dataset, indexes) 

# step 4
# calculate the days between the request and the show-up date
head.append("Aantal dagen")
for row in dataset:
    days = date(int(row[4][6:8]), int(row[4][3:5]), int(row[4][0:2])) - date(int(row[5][6:8]), int(row[5][3:5]), int(row[5][0:2])) #showup - request
    row.append(days.days)

# step 5 
# see explanation in documentation
head.append("aantal verplaatsingen")

newdataset = [] # to consturct a new list
ids = [] # to make sure a person Id is never checked twice 
for row in dataset:
    if row[2] not in ids:
        ids.append(row[2]) # sets the id in the 
        check_for_sets(row, dataset, newdataset)

# step 6 
# delete records that still have IsMoved != NULL
indexes = []
errors = []
for i in range(len(newdataset)):
    if newdataset[7] != 'NULL':
        indexes.append(i)
        errors.append(newdataset[0])    
    
delete_records(dataset, indexes)

# step 7
# delete make TrialLessontype binaire
head.insert(4, 'Aanwezig')
head.insert(5, 'Member')
for row in newdataset:
    if int(row[3]) in [3,5]:
        row.insert(4,1)
    else:
       row.insert(4,0)
    
    if int(row[3]) == 5:
        row.insert(5,1)
    else:
        row.insert(5,0)

# Save the dataset
create_excel('Dataset_PPD.csv', newdataset, head)
        
# step 8
# calculate rates
rate_of_hit(newdataset, 4, "rate of presence(1).csv", ["week", "rate of presence", "presence", "amout of people"]) # present
rate_of_hit(newdataset, 5, "rate of membership(1).csv", ["week", "rate of membership", "presence", "amout of people"]) # become a member       
