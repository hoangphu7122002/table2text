try:
    import question_template
except:
    from question_generate import question_template
import pickle
import random
import numpy as np
localHost = 'C://Users//Administrator//Desktop//largeProject//template_generate//'

import os, sys

def import_src():
    dir2 = os.path.abspath('')
    dir1 = os.path.dirname(dir2)
    if not dir1 in sys.path: sys.path.append(dir1)
    
    print(f'Append {dir1} to sys.path')
    

sys.path.append(f'{localHost}monthView')
sys.path.append(f'{localHost}quarterView')
sys.path.append(f'{localHost}yearView')
sys.path.append(f'{localHost}kpiView')
sys.path.append(f'{localHost}tongCtyView')

import_src()

from template_generate import helperFunction

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

def mappingQuesOneKPI(timeFind,view="",company="",kpi=""):
    ##for test:
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    #############
    #get template
    templateGen = question_template.genQuesOneKPI(view)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên chỉ tiêu>',str(kpi)) 

    return templateGen

def mappingGroupKPIOverall(timeFind,view="",company="",groupKPI=""):
    ##for test:
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if groupKPI == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        
    #############
    #get template
    templateGen = question_template.genQuesGroupKPIOverall(view)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên cụm chỉ tiêu>',str(groupKPI))

    return templateGen

def mappingGroupKPIDetail(timeFind,view="",company="",groupKPI="",index=None):
    ##for test:
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if groupKPI == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
    if index == None:
        index = random.choice([*range(3)])
    #############
    #get template
    templateGen = question_template.genGroupKPIDetail(view,index)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên cụm chỉ tiêu>',str(groupKPI))\
                                .replace('<cụm chỉ tiêu>',str(groupKPI))\

    return templateGen

def mappingInferenceMom(timeFind,company="",groupKPI="",kpi="",index=None):
    ##for test:
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if groupKPI == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    if index == None:
        index = random.choice([*range(2)])
    
    #############
    #get template
    templateGen = question_template.genInferenceMom(index)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên cụm chỉ tiêu>',str(groupKPI)) \
                                .replace('<tên chỉ tiêu>',str(kpi))

    return templateGen

def mappingCrossView(timeFind,company="",kpi=""):
    ##for test:
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    
    #############
    #get template
    templateGen = question_template.genQuesCrossView()
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên chỉ tiêu>',str(kpi))

    return templateGen

def mappingQuesTongcongTy(timeFind,view="",company="",kpi=""):
    ##for test:
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    #############
    #get template
    templateGen = question_template.genQuesTongCongTy(view)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên chỉ tiêu>',str(kpi)) 

    return templateGen

def mappingTrendStat(timeFind,company="",kpi="",choice=""):
    ##for test:
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    if choice == "":
        choice = random.choice(['season','monthBefore'])
    #############
    #get template
    templateGen = question_template.genQuesTrendStat()
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    distance = year - 2020 + 1
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên chỉ tiêu>',str(kpi)) \
                                .replace('<năm-m>',str(distance))

    return templateGen
    
def mappingTrendPredict(timeFind,company="",kpi="",choice=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    if choice == "":
        choice = random.choice(['season','monthBefore'])
    #############
    dataset = loaded_dict[timeFind]['month'][company][kpi]
    unit = dataset["ĐƠN VỊ"]
    
    #get template
    templateGen = question_template.genQuesTrendPredict(choice)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    distance = year - 2020 + 1
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên chỉ tiêu>',str(kpi)) \
                                .replace('<đơn vị>',unit) \
                                .replace('<năm-m>',str(distance)) \
                                .replace('<tháng+1>',str(month+1))

    return templateGen
    
def mappingExplainResult(timeFind,company="",kpi=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    #############
    
    #get template
    templateGen = question_template.genQuesExplainResult()
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên chỉ tiêu>',str(kpi)) 

    return templateGen

def mappingDetermineTrend(timeFind,company="",kpi=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    #############
    
    #get template
    templateGen = question_template.genQuesDetermineTrend()
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên chỉ tiêu>',str(kpi)) 

    return templateGen

def mappingStat1KPI(timeFind,view="",company="",kpi="",choice=""):
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    if choice == "":
        choice = random.choice(["min","max","mean"])
    #############
    
    #get template
    templateGen = question_template.genQuesStat1KPI(view,choice)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên chỉ tiêu>',str(kpi)) 

    return templateGen

def mappingStatGroupKPI(timeFind,view="",company="",groupKPI="",choice=""):
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if groupKPI == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
    if choice == "":
        choice = random.choice(["min","max","mean"])    

    templateGen = question_template.genQuesStatGroupKPI(view,choice)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    #mapping data
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    quarter = helperFunction.getQuarter(month)
    
    templateGen =    templateGen.replace('<tháng>',str(month)) \
                                .replace('<quý>',str(quarter)) \
                                .replace('<năm>',str(year)) \
                                .replace('<tên tổng công ty>',str(company)).replace('<tổng công ty>',str(company)) \
                                .replace('<tên cụm chỉ tiêu>',str(groupKPI)) 

    return templateGen


if __name__ == "__main__":
    print(mappingStatGroupKPI('01/2020'))