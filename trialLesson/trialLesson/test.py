#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 17:34:00 2018

@author: xaviervanegdom
"""

import rest_request
from rate_calculator import calculate
from datetime import date

context = calculate(rest_request.get_trialLessons(rest_request.get_token(), date(2017, 4, 2), date(2018, 7, 24)))