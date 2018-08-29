#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 00:35:02 2018

@author: Ivo
"""

import requests
import requests.auth

def get_token():
	post_data = {"grant_type": "password",
				 "username": 'Xavier',
				 "password": 'Xavier3153'}
	response = requests.post("https://defensemonkees.nl/api/token",
							 data=post_data)
	token_json = response.json()
	return token_json["access_token"]

def get_trialLessons(access_token, startTime, endTime):
    headers = {"Authorization": "bearer " + access_token}
    url = (f'https://defensemonkees.nl/api/v1/TrialLesson/Filter?startTime={startTime}&endDate={endTime}&removeDeleted=true')
    response = requests.get(url, headers=headers)
    me_json = response.json()
    return me_json