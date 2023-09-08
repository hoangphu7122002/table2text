import question_template
from util import *
import random
from collections import defaultdict
import string

punctuation = string.punctuation

def labelNer(templateGen,data):
    
    def find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]
    #handle tag
    for punc in punctuation:
        if punc in ['<','>','_']:
            continue
        templateGen = templateGen.replace(punc,' ')
    
    templateGen = templateGen.replace('  ',' ')
    lowerDigit = find(templateGen,'<')
    greaterDigit = find(templateGen,'>')
    lenDigit = [g + 1 - l for l,g in zip(lowerDigit,greaterDigit)]
    
    tag_L = 0
    ner = defaultdict(list)
    save = ""
    list_replace = []

    
    
    for l,g in zip(lowerDigit,lenDigit):
        tag = templateGen[l:l+g]
    
        begin = l+tag_L
        
        save = data.get(tag,"")
        end = len(save)
        
        tag_L = tag_L + end - len(tag)
        
        # if tag not in ner.keys():
        ner[tag].append((begin,begin+end,save))
        list_replace.append((tag,save))
    
    #replace process
    for ele in list_replace:
        tag,save = ele
        templateGen = templateGen.replace(tag,save,1)

    #find text in templateGen
    # for key in dictList.keys():
    #     list_ele = dictList[key]
    #     for ele in list_ele:
    #         idx = templateGen.rfind(ele)
    #         if idx != -1:
    #             ner[key] = (idx,idx+len(ele),ele)
    #             break
    
    return ner,templateGen

def nerOneKPI(timeFind,view="",company="",kpi=""):
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    
    templateGen = question_template.genQuesOneKPI(view)
    templateGen = helperFunction.postProcessOutput(templateGen)
    
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])    
    quarter = helperFunction.getQuarter(month)
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),
        '<tên chỉ tiêu>' : str(kpi)
    }
    
    ner,res = labelNer(templateGen,data)
    return {"sentence":res,"ner":ner}

def nerGroupKPIOverall(timeFind,view="",company="",groupKPI=""):
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
     
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),
        '<tên cụm chỉ tiêu>' : str(groupKPI)
    }
    
    ner,res = labelNer(templateGen,data)
    return {"sentence":res,"ner":ner}

def nerGroupKPIDetail(timeFind,view="",company="",groupKPI="",index=None):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),
        '<tên cụm chỉ tiêu>' : str(groupKPI),      
    }
    
    ner,res = labelNer(templateGen,data)
    return {"sentence":res,"ner":ner}

def nerInferenceMom(timeFind,company="",groupKPI="",kpi="",index=None):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),
        '<tên cụm chỉ tiêu>' : str(groupKPI),  
        '<tên chỉ tiêu>' : str(kpi)    
    }    
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}

def nerCrossView(timeFind,company="",kpi=""):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),  
        '<tên chỉ tiêu>' : str(kpi)    
    }    
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}      

def nerQuesTongcongTy(timeFind,view="",company="",kpi=""):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),  
        '<tên chỉ tiêu>' : str(kpi)    
    }    
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}      

def nerTrendStat(timeFind,company="",kpi="",choice=""):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),  
        '<tên chỉ tiêu>' : str(kpi),
        '<năm-m>' : str(distance)
    }
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}

def nerTrendPredict(timeFind,company="",kpi="",choice=""):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),  
        '<tên chỉ tiêu>' : str(kpi),
        '<đơn vị>':unit,
        '<năm-m>':str(distance),
        '<tháng+1>':str(month+1)
    }
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}

def nerExplainResult(timeFind,company="",kpi=""):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),  
        '<tên chỉ tiêu>' : str(kpi)
    }
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}

def nerDetermineTrend(timeFind,company="",kpi=""):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),  
        '<tên chỉ tiêu>' : str(kpi)
    }
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}
    
def nerStat1KPI(timeFind,view="",company="",kpi="",choice=""):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),  
        '<tên chỉ tiêu>' : str(kpi)
    }
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}

def nerStatGroupKPI(timeFind,view="",company="",groupKPI="",choice=""):
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
    
    data = {
        '<tháng>' : str(month),
        '<quý>' : str(quarter),
        '<năm>' : str(year),
        '<tên tổng công ty>' : str(company),  
        '<tên cụm chỉ tiêu>' : str(groupKPI)
    }
    
    ner,res = labelNer(templateGen,data)
    
    return {"sentence":res,"ner":ner}

if __name__ == "__main__":
    print(nerStatGroupKPI("02/2022"))