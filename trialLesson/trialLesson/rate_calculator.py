#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 13:54:23 2018

@author: xaviervanegdom
"""
from datetime import date, timedelta

# If you provide a list it stores the items before it deletes them
def delete_records(dataset, indexes, tempdataset=None,):
    minus = 0
    for index in indexes:
        index -= minus
        minus += 1
        
        if tempdataset != None: tempdataset.append(dataset[index])
        del dataset[index]  

# functions for step 4

# if a set is found, this will check how many subsets can be found in the set based on the PersonId
def check_sets(sets, dataset):
    
    usedrows = [] # to know wich rows have been part of a set
    for row in sets:
        
        tempset = [] # temp list to put the set in to append it to the dataset
        if row['isMoved'] == None: # the last record of a set
            
            tempset.append(row)
            usedrows.append(row)
            
            for i in range(len(sets)): # the end of the set is unknow so whe go to all the rows to check if we find a new next record
                for extrarow in sets:
                    if tempset[-1]['dateRequestedTrialLesson'] == extrarow['isMoved']:  # check if column requestdate of the last know record of a set matches 
                                                       # a date at one the column IsMoved in one of the other records
                        tempset.append(extrarow)
                        usedrows.append(extrarow)
                        break
                    if extrarow['isMoved'] != None:
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
            if row['personId'] == rowextra['personId']: # if the same person if, then it goes in the set list
                sets.append(rowextra)
            
    if len(sets) > 1: # if there are more then one rows then it can contain multiple sets a function will check this
        check_sets(sets, newdataset)
    else :
        save_single_record(row, newdataset)
        
def save_set(setl, dataset):
    lastrecord = setl[0]
    
    count = 0
    for record in setl:
        count += int((record['verschil']))
    lastrecord['verschil'] = count  
    
    lastrecord['aantal verplaatsingen'] = len(setl)-1
                  
    dataset.append(lastrecord)
                    
def save_single_record(record, dataset):
    #record.insert(6, "NULL") 
    record['aantal verplaatsingen'] = 0
    dataset.append(record)

def check_one_minut_diffrence(temp, extrarow):
    timefirstpart = extrarow['isMoved'][:-1]
    timelastpart = str(int(extrarow['isMoved'][-1]) - 1)
    time = timefirstpart + timelastpart
    
    condition = False
    if temp[-1]['dateRequestedTrialLesson'] == time:
        condition = True
    return condition 

# functions step 8
    
# Calculate the rate of hit found according to the given column if column = 1
def rate_of_hit(dataset, column):
    rate_of_hit = []
    for i in range(0, 28, 7): # days of the weeks up to 4 weeks
        hit = 0 # 1++ if people fall in the day range and the column = 1
        amount_of_tl = 0 # amount of poeple found
        for row in dataset:
            if i == 0: # 0 falls in week 1 what effectifly makes week 1 8 days long
                if int(row['verschil']) >= i and int(row['verschil']) <= i + 7: 
                    if row[column] == 1:
                        hit += 1
                    amount_of_tl += 1
            else: # if i != 0 then its not week one and the weeks are 7 days long
                if int(row['verschil']) > i and int(row['verschil']) <= i + 7: 
                    if row[column] == 1:
                        hit += 1
                    amount_of_tl += 1
                
        rate_of_hit.append({'week' : f'{i} - {i + 7}', 'percentage' : hit / amount_of_tl * 100, 'aantal' : hit, 'aantal_mensen_totaal' : amount_of_tl })
        
    calculate_percentages(rate_of_hit)
    return rate_of_hit

# calculate how much lower the percentages is in an absolute number and relatively
def calculate_percentages(rate_of_hit):
    for i in range(len(rate_of_hit)):
        if i == 0:
            rate_of_hit[0]['minusA'] = 0
            rate_of_hit[0]['minusP'] = 0
        else :
            rate_of_hit[i]['minusA'] = rate_of_hit[i -1]['percentage'] - rate_of_hit[i]['percentage']
            rate_of_hit[i]['minusP'] = rate_of_hit[i]['minusA'] / rate_of_hit[i - 1]['percentage']


def calculate(dataset):
    # step 1
    # delete records with IsDeleted != NULL
    indexes = []
    for i in range(len(dataset)):
        if dataset[i]['isDeleted'] != None:
            indexes.append(i)
        row = dataset[i]
        del row['isDeleted']
            
    delete_records(dataset, indexes)
        
    # step 2
    # delete record if DateRequestedTrialLesson and IsMoved is the same 
    indexes = []
    for i in range(len(dataset)):
        if dataset[i]['dateRequestedTrialLesson'] == dataset[i]['isMoved']: # DateRequestedTrialLesson and IsMoved
            indexes.append(i)
    
    delete_records(dataset, indexes) 
    
    # step 3
    # calculate the days between the request and the show-up date
    for row in dataset:
        days = date(int(row['dateTrialLesson'][0:4]), int(row['dateTrialLesson'][5:7]), int(row['dateTrialLesson'][8:10])) - 
        date(int(row['dateRequestedTrialLesson'][0:4]), int(row['dateRequestedTrialLesson'][5:7]), int(row['dateRequestedTrialLesson'][8:10])) #showup - request
        row['verschil'] = days.days 
        
    # step 4
    # see explanation in documentation    
    newdataset = [] # to consturct a new list
    ids = [] # to make sure a person Id is never checked twice 
    for row in dataset:
        if row['personId'] not in ids:
            ids.append(row['personId']) # sets the id in the 
            check_for_sets(row, dataset, newdataset)
    
    # step 5 
    # delete records that still have IsMoved != NULL
    indexes = []
    errors = []
    for i in range(len(newdataset)):
        if newdataset[i]['isMoved'] != None:
            indexes.append(i)
            errors.append(newdataset[0])    
        
    delete_records(dataset, indexes)
    
    # step 6
    # make TrialLessontype binaire
    for row in newdataset:
        if int(row['trialLessonTypeId']) in [3,5]:
            row['aanwezig'] = 1
        else:
            row['aanwezig'] = 0
        
        if int(row['trialLessonTypeId']) == 5:
            row['member'] = 1
        else:
            row['member'] = 0
    
    # Save the dataset            
    # step 7
    # calculate rates
    return {'endresult' : newdataset,
            'rate_of_presence' : rate_of_hit(newdataset, 'aanwezig'), 
            'rate_of_membership' : rate_of_hit(newdataset, 'member')} # become a member