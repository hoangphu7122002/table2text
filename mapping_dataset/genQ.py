import mapping_dataset as genA
import helperFunction
import random
import json
import pickle

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

lenRes = 5000

def scriptOneKPI():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingQuesOneKPI(date,view,company,kpi)
            # #answer = genA.mappingOneKPI(date,view,company,kpi)
                            
            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/oneKPI.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptGroupMonthOverall():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            
            question = genQ.mappingGroupKPIOverall(date,view,company,groupKPI)
            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/groupMonthOverall.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptGroupMonthDetail():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            index = random.choice([*range(3)])
            
            question = genQ.mappingGroupKPIDetail(date,view,company,groupKPI,index)
                        
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/groupMonthDetail.pkl','wb')
    pickle.dump(listQA,outfile)
    
def scriptChildInferenceMom():
    listQA = []
    for _ in range(lenRes):
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
            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/ChildInferenceMom.pkl','wb')
    pickle.dump(listQA,outfile)
    
def scriptCrossView():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = genQ.loadParentSet(genQ.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(genQ.listingGroupKPI(genQ.loaded_dict,company,groupKPI))
            
            question = genQ.mappingCrossView(date,company,kpi)
            #answer = genA.mappingCrossView(date,company,kpi)
            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/crossView.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptViewStat():
    listQA = []
    for _ in range(lenRes):
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
            #answer = genA.mappingViewStat(date,company,kpi,choice)
            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/viewStat.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptViewPredict():
    listQA = []
    for _ in range(lenRes):
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
            #answer = genA.mappingViewPredict(date,company,kpi,choice)
                            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/viewPredict.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptViewExplainResult():
    listQA = []
    for _ in range(lenRes):
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
            #answer = genA.mappingViewExplainResult(date,company,kpi)
            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/viewExplainResult.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptViewDetermineTrend():
    listQA = []
    for _ in range(lenRes):
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
            #answer = genA.mappingViewDetermineTrend(date,company,kpi)

            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/viewDetermineTrend.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptViewOneKPIStat():
    listQA = []
    for _ in range(lenRes):
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
            #answer = genA.mappingViewOneKPIStat(date,view,company,kpi,choice)
                            
            listQA.append(question)              
        # except:
        #     continue
    
    outfile = open('datasetQ/viewOneKPIStat.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptViewOneGroupKPIStat():
    listQA = []
    for _ in range(lenRes):
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
            #answer = genA.mappingViewOneGroupKPIStat(date,view,company,groupKPI,choice)
                            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/viewOneGroupKPIStat.pkl','wb')
    pickle.dump(listQA,outfile)

def scriptCtyDescribe():
    listQA = []
    for _ in range(lenRes):
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
            #answer = genA.mappingCtyDescribe(date,view,company)
            
            listQA.append(question)              
        except:
            continue
    
    outfile = open('datasetQ/viewCtyDescribe.pkl','wb')
    pickle.dump(listQA,outfile)
        
if __name__ == "__main__":
    scriptOneKPI()
    scriptGroupMonthOverall()
    scriptGroupMonthDetail()
    scriptChildInferenceMom()
    scriptCrossView()
    scriptViewStat()
    scriptViewPredict()
    scriptViewExplainResult()
    scriptViewDetermineTrend()
    scriptViewOneKPIStat()
    scriptViewOneGroupKPIStat()
    scriptCtyDescribe()