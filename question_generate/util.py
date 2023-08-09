import pickle

localHost = 'C://Users//Administrator//Desktop//largeProject//template_generate//'

import os, sys

def import_src():
    dir2 = os.path.abspath('')
    dir1 = os.path.dirname(dir2)
    if not dir1 in sys.path: sys.path.append(dir1)
    
    print(f'Append {dir1} to sys.path')

import_src()
from template_generate import helperFunction

meanDesc = ['mean','trung bình','bình quân','giá trị trung bình','trung bình cộng']
minDesc = ['giá trị nhỏ nhất','min','giá trị bé nhất','giá trị tối thiểu','giá trị thấp nhất']
maxDesc = ['giá trị lớn nhất','max','giá trị tối đa','giá trị bự nhất','giá trị to nhất']
datList = ['đạt','ổn','tốt','hoàn thành','như mong đợi']
koDatList = ['chưa đạt','không đạt','không ổn','chưa tốt','không hoàn thành','chưa hoàn thành','chưa ổn','không ổn','không như mong đợi','chưa như mong đợi']
allList = ['tất cả','toàn bộ','các','đầy đủ','bao gồm']
detailList = ["chi tiết","sâu hơn","tường tận","cặn kẽ","tỉ mỉ","đầy đủ","tường minh","rõ ràng"]
overallList = ["khái quát","tổng quan","tổng thể","cơ bản","tổng hợp","tóm tắt"]
nextMonthList = ["tháng tiếp theo","tháng kế tiếp","tháng sau","tháng <tháng+1>","vào tháng tới"]
seasonList = "2020 đến"

dictList = {
    "<mean>": meanDesc,
    "<min>": minDesc,
    "<max>": maxDesc,
    "<đạt>": datList,
    "<không đạt>": koDatList,
    "<tất cả>": allList,
    "<chi tiết>": detailList,
    "<tổng quan>":overallList,
    "<tháng tiếp theo>":nextMonthList,
    "<mùa>":seasonList
}

#==================Util function===================
with open('saved_dictionary.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)

def loadParentSet(loaded_dict,company='VTS'):
    groupKPISet = set()
    for oneKPI in loaded_dict['01/2020']['month'][company]:
        comp = loaded_dict['01/2020']['month'][company][oneKPI]['KPI MẸ']
        groupKPISet.add(comp)
    return groupKPISet

def listingGroupKPI(loaded_dict,company='VTPOST',kpi_mom='Tỷ lệ xử lý phản ánh của KH'):
    listOneKPI = []
    for oneKPI in loaded_dict['01/2020']['month'][company]:
        comp = loaded_dict['01/2020']['month'][company][oneKPI]['KPI MẸ']
        if comp == kpi_mom: 
            listOneKPI.append(oneKPI)
    return listOneKPI
#==================Util function===================