import re
import random
import numpy as np
import calendar
from datetime import datetime
from datetime import datetime, timedelta
from scipy import stats
import math

#===========================================================================
#post process output:
##Viết hoa đầu câu hoặc sau dấu chấm
##Bỏ đi một số dấu bị dư (kiểu như hai dấu liên tiếp như: ",,", ", ", ". ")
##Đưa dạng "abc ," về dạng "abc,"
##Strip,Replace("  "," ").

def replace_commas_and_dots(input_string):
    # Thay thế ",," thành ","
    replaced_string = re.sub(r',+', ',', input_string)
    # Thay thế ".." thành "."
    replaced_string = re.sub(r'\.+', '.', replaced_string)
    return replaced_string

def postProcessOutput(sent):
    sent = sent.lower().strip().replace('  ',' ').replace(' ,',',').replace(' .','.')
    sent = replace_commas_and_dots(sent)
    sents = sent.split('.')
    newSent = []
    for text in sents:
        if len(text) == 0: continue
        text = text.strip()
        firstDigit = text[0]
        parital = text[1:]
        newSent.append(firstDigit.upper()+parital)
    
    return ". ".join(newSent)
#==========================================================================
##Implement sau
def predictNextMonth(listDat, listKoDat):
    resDat = None
    resKoDat = None
    if len(listDat) != 0:
        resDat = np.mean([ele[1] for ele in listDat])
    if len(listKoDat) != 0:
        resKoDat = np.mean([ele[1] for ele in listKoDat])
    #định nghĩa sau
    eval = random.choice(['đạt','không đạt'])
    if resDat is None: return resKoDat, eval
    if resKoDat is None: return resDat, eval
    return (resDat + resKoDat)/2, eval

def predictView(listKPI):
    return np.mean(listKPI)

def determineTrend(listKPI):
    assert(len(listKPI) > 1)
    x = [*range(len(listKPI))]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,listKPI)
    
    return (math.atan(slope) / math.pi) * 180, slope * len(listKPI) + intercept
    
#=========================================================================
def next_month(date_str):
    date = datetime.strptime(date_str, '%m/%Y').date()
    year = date.year
    month = date.month
    days_in_month = calendar.monthrange(year, month)[1]
    if date.month == 12:
        next_date = date.replace(year=year+1, month=1)
    else:
        next_date = date.replace(day=1, month=month+1)
    next_date = next_date.replace(day=min(date.day, days_in_month))
    return datetime.strftime(next_date, '%m/%Y')

def generateListDate(beginDate='01/2020',endDate='07/2023'):
    listDate = []
    while beginDate != endDate:
        listDate.append(beginDate)
        beginDate = next_month(beginDate)
    return listDate

def genPreviousSeason(date_str):
    month = date_str.split('/')[0]
    year = int(date_str.split('/')[1])
    listDateStr = []
    
    while year != 2019:
        listDateStr.append(f'{month}/{year}')
        year -= 1
    
    return listDateStr

def generatePrevMonthList(date_str):
    month = int(date_str.split('/')[0])
    year = int(date_str.split('/')[1])
    
    if month == 1: 
        return []
    
    list_date = []
    for i in range(1,int(month)):
        if i == 11: list_date.append(f'11/{year}')
        elif i == 10: list_date.append(f'10/{year}')
        else: list_date.append(f'0{i}/{year}')
    return list_date

def getQuarter(current_month):
    current_quarter = ''
    for i in range(0,4):
        if current_month in [1 + 3*i,2 + 3*i,3 + 3*i]:
            current_quarter = i+1
    return current_quarter