#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2023 Wael Hojak

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

###########################################################

Created on Sat Nov 26 20:29:30 2022
@author: Wael Hojak

"""

import requests
import json
import pandas as pd
import os

folder = os.path.realpath(os.path.dirname(__file__)) + '/'

# load dict with error data extracted from the manual (txt file)
with open(folder+'fanuc_alarm_codes_manual.json') as file:
    DIC_ERROR_MANUAL = json.load(file)

# load dict with error data fetched from the API (online)
with open(folder+'fanuc_alarm_codes_api.json') as file:
    DIC_ERROR_API = json.load(file)

# load dict with facility code-name matrix extracted from the manual (txt file)
with open(folder+'table_facility_codes_by_number.json') as file:
    FACIL_CODE_BY_NUM = json.load(file)
    
# like the latter, but with category names as keys
with open(folder+'table_facility_codes_by_name.json') as file:
    FACIL_CODE_BY_NAME = json.load(file)


# import data from csv file 'table_error_facility_codes'
DF_FACILITY_CODES = pd.read_csv(folder+'table_facility_codes.csv', delimiter=',', header=9)


def get_alarm_code(status) -> (str, str, str):
    """
    get alarm code, category name and description of the given status.
    Parameters
    ----------
    status : int or str
        int: error status received from FANUC, e.g: 12311
        str: alarm code as displayed on TP, e.g.:'INTP-311'.
    Returns
    -------
    (str, str, str)
        alarm code, category name and description of category.
    """
    if type(status) == int:
        print(f"Fetching details about status: '{status}' ...")
        cat_num = str(status)[:-3]   # '12' in case status = 12311
        err_num = str(status)[-3:]
        assert cat_num in FACIL_CODE_BY_NUM, f'unknown facility code: {cat_num}.'
        category = FACIL_CODE_BY_NUM[cat_num]['Facility Name']
        disc = FACIL_CODE_BY_NUM[cat_num]['Description']
        alarm_code = f'{category}-{err_num}'    # INTP-311 for status = 12311
        
    else: # input is an alarm code like 'INTP-311'.
        alarm_code = status.upper()
        print(f"Fetching details about alarm code: '{alarm_code}' ...")
        category = alarm_code.split('-')[0]
        disc = FACIL_CODE_BY_NAME[category]['Description']
    
    return alarm_code, category, disc


def error_detail(status) -> str:
    """
    Fetching details about the status from FANUC Manual:
        "OPERATOR'S MANUAL (Alarm Code List)
         R-30+B CONTROLLER / B-83284EN-1/02"
    Parameters
    ----------
    status : int or str
        int: error status received from FANUC, e.g: 12311
        str: alarm code as displayed on TP, e.g.:'INTP-311'.
    Returns
    -------
    (str)
        message with the details about the error.
    """
    alarm_code, category, disc = get_alarm_code(status)
    print(f"Facility Name: '{category}'\nDescription: '{disc}'")
    
    if category in DIC_ERROR_MANUAL:
        if alarm_code in DIC_ERROR_MANUAL[category]:
            msg = DIC_ERROR_MANUAL[category][alarm_code]
        else:
            msg = f"unknown alarm code: {alarm_code}"
    else:
        msg = f"unknown error category: {category}"
    
    print('########################################################')
    print("######     OPERATOR'S MANUAL (Alarm Code List)    ######")
    print("######     R-30+B CONTROLLER / B-83284EN-1/02     ######")
    print('########################################################')
    print(msg)
    print('########################################################')
    return msg


def error_detail_api(status) -> str:
    """
    Fetching details about the status from the dictionary that was fed with data
    using the API available on: http://linuxsand.info/fanuc/. It provides details
    to Alarm codes of FANUC Robotics, supports R-30iB controller (8.0 series).
    Parameters
    ----------
    status : int or str
        int: error status received from FANUC, e.g: 12311
        str: alarm code as displayed on TP, e.g.:'INTP-311'.
    Returns
    -------
    (str)
        message with the details about the error.
    """
    alarm_code, category, disc = get_alarm_code(status)
    print(f"Facility Name: '{category}'\nDescription: '{disc}'")
    
    if category in DIC_ERROR_API:
        if alarm_code in DIC_ERROR_API[category]:
            msg = DIC_ERROR_API[category][alarm_code]
        else:
            msg = f"unknown alarm code: {alarm_code}"
    else:
        msg = f"unknown error category: {category}"
    
    print('########################################################')
    print('######       These details were previously        ######')
    print('######              retrieved from:               ######')
    print('######        http://linuxsand.info/fanuc/        ######')
    print('########################################################')
    print(msg)
    print('########################################################')
    return msg


def error_detail_online(status) -> dict:
    """
    Fetching details about status or alarm code from the API available on:
    http://linuxsand.info/fanuc/. It provides details to Alarm codes of FANUC 
    Robotics, supports R-30iB controller (8.0 series).
    Parameters
    ----------
    status : int or str
        int: error status received from FANUC, e.g: 12311
        str: alarm code as displayed on TP, e.g.:'INTP-311'.
    Raises
    ------
    SystemExit
        e.g. when you pc is offline.
    Returns
    -------
    (str)
        received dictionary with the details about the error.
    """
    alarm_code, category, disc = get_alarm_code(status)
    print(f"Facility Name: '{category}'\nDescription: '{disc}'")
    
    url_call = f'http://linuxsand.info/fanuc/code-api/{alarm_code}?type=json'
    try:
        r = requests.get(url_call)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e) 
        
    dic = json.loads(r.content)
    print('########################################################')
    print('######        http://linuxsand.info/fanuc/        ######')
    print('########################################################')
    for k, v in dic.items():
        print(f'{k}: {v}')
    print('########################################################')
    return dic

