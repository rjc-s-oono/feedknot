# -*- coding: utf-8 -*-
import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta

def get_first_day(date):
    """月初を返す"""
    return date.replace(day=1)

def get_last_day(date):
    """月末を返す"""
    return date.replace(day=get_days_of_month(date.year, date.month))

def get_days_ago(date, number_of_days):
    """数日前の日付を返す"""
    return date - datetime.timedelta(days=number_of_days)

def get_months_ago(date, number_of_months):
    """数月前の日付を返す"""
    return date - relativedelta(months=number_of_months)

def get_years_ago(date, number_of_years):
    """数年前の日付を返す"""
    return date - relativedelta(years=number_of_years)

def get_days_later(date, number_of_days):
    """数日後の日付を返す"""
    return date + datetime.timedelta(days=number_of_days)

def get_months_later(date, number_of_months):
    """数月後の日付を返す"""
    return date + relativedelta(months=number_of_months)

def get_years_later(date, number_of_years):
    """数年後の日付を返す"""
    return date + relativedelta(years=number_of_years)

def get_days_of_month(year,month):
    """年,月の日数を返す"""
    return monthrange(year, month)[1]

def is_last_day(date):
    """月末日付ならTrueを返す"""
    return get_days_of_month(date.year, date.month) == date.day

def get_manths_list(year):
    """指定月の1年の日付配列を返す"""
    manths_list = []
    for manths in range(1, 13):
        manths_list.append(datetime.date(year, manths, 1))
    return manths_list

def get_years_list(from_year, to_year):
    """指定年の間の年日付配列を返す"""
    years_list = []
    for year in range(int(from_year), int(to_year)+1):
        years_list.append(datetime.date(year, 1, 1))
    return years_list
