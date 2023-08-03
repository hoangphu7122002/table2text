import mapping_dataset as genA
import helperFunction
import random
import json


localHost = 'C://Users//Administrator//Desktop//largeProject//question_generation'

import os, sys

def import_src():
    dir2 = os.path.abspath('')
    dir1 = os.path.dirname(dir2)
    if not dir1 in sys.path: sys.path.append(dir1)
    
    print(f'Append {dir1} to sys.path')
    
import_src()
import question_generate.mapping_question as genQ

listDate = helperFunction.generateListDate()

def scriptOneKPI():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingQuesOneKPI(date,view,company,kpi)
            answer = genA.mappingOneKPI(date,view,company,kpi)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/oneKPI.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptGroupMonthOverall():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            
            question = genQ.mappingGroupKPIOverall(date,view,company,groupKPI)
            answer = genA.mappingGroupMonthOverall(date,view,company,groupKPI)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/groupMonthOverall.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptGroupMonthDetail():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            index = random.choice([*range(3)])
            
            question = genQ.mappingGroupKPIDetail(date,view,company,groupKPI,index)
            answer = genA.mappingGroupMonthDetail(date,view,company,groupKPI,index)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/groupMonthDetail.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))
    
def scriptChildInferenceMom():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            question = genQ.mappingInferenceMom(date,company,groupKPI,kpi,index)
            answer = genA.mappingChildInferenceMom(date,company,kpi,index)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/ChildInferenceMom.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))
    
def scriptCrossView():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingCrossView(date,company,kpi)
            answer = genA.mappingCrossView(date,company,kpi)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/crossView.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewStat():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['season','monthBefore'])
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingTrendStat(date,company,kpi,choice)
            answer = genA.mappingViewStat(date,company,kpi,choice)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/viewStat.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewPredict():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['season','monthBefore'])
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingTrendPredict(date,company,kpi,choice)
            answer = genA.mappingViewPredict(date,company,kpi,choice)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/viewPredict.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewExplainResult():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['season','monthBefore'])
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingExplainResult(date,company,kpi)
            answer = genA.mappingViewExplainResult(date,company,kpi)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/viewExplainResult.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewDetermineTrend():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['season','monthBefore'])
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingDetermineTrend(date,company,kpi)
            answer = genA.mappingViewDetermineTrend(date,company,kpi)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/viewDetermineTrend.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewOneKPIStat():
    listQA = []
    for _ in range(1000):
        # try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['min','max','mean'])
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingStat1KPI(date,view,company,kpi,choice)
            answer = genA.mappingViewOneKPIStat(date,view,company,kpi,choice)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        # except:
        #     continue
    
    with open('datasetQA/viewOneKPIStat.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewOneGroupKPIStat():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['min','max','mean'])
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingStatGroupKPI(date,view,company,groupKPI,choice)
            answer = genA.mappingViewOneGroupKPIStat(date,view,company,groupKPI,choice)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/viewOneGroupKPIStat.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptCtyDescribe():
    listQA = []
    for _ in range(1000):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['min','max','mean'])
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingQuesTongcongTy(date,view,company,kpi)
            answer = genA.mappingCtyDescribe(date,view,company)
                            
            dict_res = {
                "question" : question,
                "answer" : answer
            }  
            
            listQA.append(dict_res)              
        except:
            continue
    
    with open('datasetQA/viewCtyDescribe.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

scriptCtyDescribe()
# scriptViewOneGroupKPIStat()
# scriptViewOneKPIStat()
# scriptViewDetermineTrend()
# scriptViewExplainResult()
# scriptViewPredict()
# scriptViewStat()
# scriptCrossView()
# scriptGroupMonthDetail()
# with open('datasetQA/groupMonthDetail.json', 'r') as outfile:
#     data = json.loads(outfile.read())
# print(data)