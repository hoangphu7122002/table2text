import NER_generate
import random
import json

listDate = NER_generate.helperFunction.generateListDate()

lenRes = 1000

def scriptOneKPI():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            
            dict_res = NER_generate.nerOneKPI(date,view,company,kpi)
            
            listQA.append(dict_res)
        except:
            continue   
    
    with open('datasetNER/oneKPI.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptGroupMonthOverall():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            
            dict_res = NER_generate.nerGroupKPIOverall(date,view,company,groupKPI)
            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    
    with open('datasetNER/groupMonthOverall.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptGroupMonthDetail():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(3)])
            
            dict_res = NER_generate.nerGroupKPIDetail(date,view,company,groupKPI,index)
            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/groupMonthDetail.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptChildInferenceMom():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerInferenceMom(date,company,groupKPI,kpi,index)
            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/ChildInferenceMom.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptCrossView():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerCrossView(date,company,kpi)
            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/crossView.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewStat():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['season','monthBefore'])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerTrendStat(date,company,kpi,choice)
            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/viewStat.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))
        
def scriptViewPredict():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['season','monthBefore'])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerTrendPredict(date,company,kpi,choice)
            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/viewPredict.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewExplainResult():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['season','monthBefore'])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerExplainResult(date,company,kpi)            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/viewExplainResult.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))
        
def scriptViewDetermineTrend():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['season','monthBefore'])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerDetermineTrend(date,company,kpi)            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/viewDetermineTrend.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))
        
def scriptViewOneKPIStat():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['min','max','mean'])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerStat1KPI(date,view,company,kpi,choice)            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/viewOneKPIStat.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptViewOneGroupKPIStat():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['min','max','mean'])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerStatGroupKPI(date,view,company,kpi,choice)            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/viewOneGroupKPIStat.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))

def scriptCtyDescribe():
    listQA = []
    for _ in range(lenRes):
        try:
            date = random.choice(listDate)
            view = random.choice(["month","quarter","year"])
            company = random.choice(["VTS","VTT","VDS","VTPOST"])
            choice = random.choice(['min','max','mean'])
            
            #get kpi
            parentSet = NER_generate.loadParentSet(NER_generate.loaded_dict,company)
            groupKPI = random.choice(list(parentSet))
            kpi = random.choice(NER_generate.listingGroupKPI(NER_generate.loaded_dict,company,groupKPI))
            index = random.choice([*range(2)])
            
            dict_res = NER_generate.nerQuesTongcongTy(date,view,company,kpi)            
            listQA.append(dict_res)
        except:
            continue
    # print(listQA)
    with open('datasetNER/viewCtyDescribe.json', 'w') as outfile:
        outfile.write(json.dumps(listQA))    


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