#!_*_coding:utf-8_*_
#__author__:"Alex Li"
import os
import sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database title summary
TITLE = ['id','name','age','phone','dept','enroll_date','expire_date','account','password','credit','balance','status','pay_day']

# Account database setting
DATABASE = {
    'engine': 'file_storage',  # support mysql, postgresql in the future
    'name':'accounts_table',
    'path': "%s/db/" % BASE_DIR
}

# Manager account database setting
MANAGE_DATABASE = {
    'engine': 'file_storage',  # support mysql, postgresql in the future
    'name':'managers_table',
    'path': "%s/db/" % BASE_DIR
}

# logger setting
LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': 'transactions.log',
    'access': 'access.log',
}

# Transaction setting
TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer':{'action':'minus', 'interest':0.05},
    'consume':{'action':'minus', 'interest':0},

}

ACCOUNT_DEFAULT = {
    'credit': 15000.0

}