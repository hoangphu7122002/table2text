import pickle
import random
import helperFunction
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

from template_generate.monthView import a_monthView
from template_generate.monthView import b_monthView
from template_generate.quarterView import a_quaterView
from template_generate.quarterView import b_linkQMView
from template_generate.kpiView import trend_kpiView
from template_generate.yearView import a_yearView
from template_generate.kpiView import stat_kpiView
from template_generate.tongCtyView import a_tongCtyView

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

def convertKeyToIndexDict(dictRes):
    keyList = list(dictRes.keys())
    dictKey = dict()
    for index,ele in enumerate(keyList):
        dictKey[index] = ele
    return dictKey

def convertIndex(idx,len_):
    return len_ + idx

templateOneKPI = {
    "month" : a_monthView,
    "quarter" :  a_quaterView,
    "year" : a_yearView
}

def sign(a):
    return bool(a > 0) - bool(a < 0)

def getSign(kpiNow,kpiTarget=None):
    if kpiTarget is None: signVal = sign(kpiNow)
    else: signVal = sign(kpiNow - kpiTarget)
    
    if random.random() > 0.1:
        return signVal
    else:
        return 0

def getRatio(kpiNow,kpiTarget):
    return kpiNow / kpiTarget
    

def mappingOneKPI(timeFind, view = "", company="", kpi = "",dict_index={"indexNow":None,
                                                                       "indexBefore":None,
                                                                       "indexYearBefore":None,
                                                                       "index":None}):
    ##for test:
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    dataset = loaded_dict[timeFind][view][company][kpi]
    #############
    
    dictKey = convertKeyToIndexDict(dataset)
    
    #get data
    unit = dataset[dictKey[3]].lower()
    condition = dataset[dictKey[4]]
    target = dataset[dictKey[5]]
    kpiNow = dataset[dictKey[6]]
    evaluation = dataset[dictKey[7]].lower()
    
    monthBefore = dataset[dictKey[8]]
    compareMonthBefore = dataset[dictKey[9]]
    yearBefore = dataset[dictKey[convertIndex(-4,len(dictKey))]]
    compareYearBefore = dataset[dictKey[convertIndex(-3,len(dictKey))]]
    groupKPI = dataset[dictKey[convertIndex(-1,len(dictKey))]]
    ##############
    
    ###Describe###
    describeNow = dictKey[6]
    describeMonthBefore = dictKey[8]
    describeYearBefore = dictKey[convertIndex(-4,len(dictKey))]
    
    templateGen = templateOneKPI[view]
    sign = []
    ratio = []
    
    sign.append(getSign(kpiNow,target))
    sign.append(getSign(compareMonthBefore))
    sign.append(getSign(compareYearBefore))
    
    ratio.append(getRatio(kpiNow,target))
    ratio.append(getRatio(kpiNow,monthBefore))
    ratio.append(getRatio(kpiNow,yearBefore))
        
    # print(sign)
    # print(ratio)
    ##############
    
    timeView = describeNow.split(' ')[1].split('.')[0]
    yearView = describeNow.split(' ')[1].split('.')[1]
    
    monthBeforeView = describeMonthBefore.split('.')[0][1:]
    
    if view != "year":
        yearBeforeView = describeYearBefore.split('.')[1]
    else:
        yearBeforeView = describeYearBefore[1:]
    ##getTemplate
    if view != "year":
        postProcess = templateGen.genFullView(sign,ratio,dict_index["indexNow"],dict_index["indexBefore"],dict_index["indexYearBefore"],dict_index["index"])
    else:
        postProcess = templateGen.genFullView(sign,ratio,dict_index["indexNow"],dict_index["indexBefore"],dict_index["index"])
    if dict_index["index"] == None:
        prefixGen = templateGen.genPrefixAdv() + ' ' + templateGen.genPrefixDesc()  + ' '
    else: 
        prefixGen = 'chỉ tiêu <tên chỉ tiêu> '
    template = prefixGen + postProcess

    template = helperFunction.postProcessOutput(template)
    ##############
    
    ratio_res = round(kpiNow / target,2)
    diff_res = round(kpiNow - target,2)
    ratio_year_res = round(kpiNow / yearBefore,2)
    ratio_month_res = round(kpiNow / monthBefore,2)
    
    if unit != "%":
        unit = ' ' + unit
    template  = template.replace('<tên chỉ tiêu>',f'{kpi}') \
                        .replace('<tên tổng công ty>',f"{company}").replace('<tổng công ty>',f"{company}") \
                        .replace('<đạt/không đạt>',f"{evaluation}") \
                        .replace('<hiện trạng kpi>',f"{kpiNow}") \
                        .replace('<đơn vị>',f"{unit}") \
                        .replace('<mục tiêu kpi>',f"{target}") \
                        .replace('<tháng>',timeView).replace('<quý>',timeView).replace('<năm>',yearView) \
                        .replace('<tháng-1>',monthBeforeView).replace('<năm-1>',yearBeforeView)\
                        .replace('<quý-1>',monthBeforeView)\
                        .replace('<độ tăng giảm so với kpis mục tiêu>',f"{abs(diff_res)}") \
                        .replace('<độ tăng giảm so với kpi tháng trước>',str(abs(compareMonthBefore))) \
                        .replace('<độ tăng giảm so với kpi năm trước>',str(abs(compareYearBefore))) \
                        .replace('<độ tăng giảm so với kpi cùng kỳ năm trước>',str(abs(compareYearBefore))) \
                        .replace('<độ tăng giảm so với kpi quý trước>',str(abs(compareMonthBefore))) \
                        .replace('<kpi tháng trước>',str(monthBefore)).replace('<kpi quý trước>',str(monthBefore)).replace('<kpi năm trước>',str(yearBefore)) \
                        .replace('<kpi cùng kỳ năm trước>',str(yearBefore))\
                        .replace('<tỉ lệ so với kpis mục tiêu>',f"{ratio_res}") \
                        .replace('<tỉ lệ so với kpi cùng kỳ năm trước>',str(ratio_year_res))\
                        .replace('<tỉ lệ so với kpi tháng trước>',str(ratio_month_res))\
                        .replace('<tỉ lệ so với kpi năm trước>',str(ratio_year_res))\
                        .replace('<tỉ lệ so với kpi quý trước>',str(ratio_month_res))
                    
    return template
    
def mappingGroupMonthOverall(timeFind,view="",company="",groupKPI="",index = None):
    ##for test:
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if groupKPI == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpiList = listingGroupKPI(loaded_dict,company,groupKPI)
    #đưa về trường hợp đặc biệt
    if len(kpiList) == 1:
        dataset = loaded_dict[timeFind][view][company][kpiList[0]]
        if dataset['KPI MẸ'] == groupKPI:
            return f'cụm chỉ tiêu "{groupKPI}" này được coi là 1 chỉ tiêu (vì nó không có chỉ tiêu con). ' +  mappingOneKPI(timeFind, view, company, kpiList[0])
        else:
            return f'cụm chỉ tiêu "{groupKPI}" này chỉ có 1 chỉ tiêu con duy nhất là "{kpiList[0]}. "' + mappingOneKPI(timeFind, view, company, kpiList[0])
    #trường hợp bình thường
    evaluationList = [loaded_dict[timeFind][view][company][kpi]['Đánh giá'] for kpi in kpiList]
    
    #get data
    datList = [ele for ele in evaluationList if ele == "Đạt"]
    koDatList = [ele for ele in evaluationList if ele == "Không đạt"]
    dataset = loaded_dict[timeFind][view][company][kpiList[0]]
    
    dictKey = convertKeyToIndexDict(dataset)
    
    #get data
    timeMonth = dataset[dictKey[1]] 
    unit = dataset[dictKey[3]].lower()
    condition = dataset[dictKey[4]]
    describeNow = dictKey[6]
    
    month = timeMonth.split('/')[0][1:]
    year = timeMonth.split('/')[1]
    timeView = describeNow.split(' ')[1].split('.')[0]
    
    #get template
    template = helperFunction.postProcessOutput(b_monthView.genGroupMonthOverall(kpiList,evaluationList,view,index))
    
    if unit != "%":
        unit = ' ' + unit
    #mapping
    template =  template.replace('<số chỉ tiêu không đạt>',str(len(koDatList))) \
                        .replace('<số chỉ tiêu đạt>',str(len(datList))) \
                        .replace('<tổng số chỉ tiêu con>',str(len(evaluationList))) \
                        .replace('<năm>',year).replace('<tháng>',month).replace('<quý>',timeView) \
                        .replace('<đơn vị>',unit).replace('<điều kiện>',condition) \
                        .replace('<tên cụm chỉ tiêu>',f'"{groupKPI}"')
    
    #loại bỏ trường hợp có số chỉ tiêu là 0
    template = template.replace(', số chỉ tiêu đạt là 0 chỉ tiêu','.') \
                       .replace('có số chỉ tiêu không đạt là 0 chỉ tiêu, ','.')
    
    return template
    
def mappingGroupMonthDetail(timeFind,view="",company="",groupKPI="",index = None):
    ##for test:
    if view == "":
        view = random.choice(["month","quarter","year"])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if groupKPI == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpiList = listingGroupKPI(loaded_dict,company,groupKPI)
    #đưa về trường hợp đặc biệt
    if len(kpiList) == 1:
        dataset = loaded_dict[timeFind][view][company][kpiList[0]]
        if dataset['KPI MẸ'] == groupKPI:
            return f'cụm chỉ tiêu "{groupKPI}" này được coi là 1 chỉ tiêu (vì nó không có chỉ tiêu con). ' +  mappingOneKPI(timeFind, view, company, kpiList[0])
        else:
            return f'cụm chỉ tiêu "{groupKPI}" này chỉ có 1 chỉ tiêu con duy nhất là "{kpiList[0]}. "' + mappingOneKPI(timeFind, view, company, kpiList[0])
        
    evaluationList = [loaded_dict[timeFind][view][company][kpi]['Đánh giá'] for kpi in kpiList]
    #get data
    datList = [ele for ele in evaluationList if ele == "Đạt"]
    kpiDatList = [kpi for kpi in kpiList if loaded_dict[timeFind][view][company][kpi]['Đánh giá'] == "Đạt"]
    kpiKoDatList = [kpi for kpi in kpiList if loaded_dict[timeFind][view][company][kpi]['Đánh giá'] == "Không đạt"]
    koDatList = [ele for ele in evaluationList if ele == "Không đạt"]
    
    dataset = loaded_dict[timeFind][view][company][kpiList[0]]
    
    dictKey = convertKeyToIndexDict(dataset)
    
    timeMonth = dataset[dictKey[1]] 
    unit = dataset[dictKey[3]].lower()
    condition = dataset[dictKey[4]]
    describeNow = dictKey[6]
    
    month = timeMonth.split('/')[0][1:]
    year = timeMonth.split('/')[1]
    timeView = describeNow.split(' ')[1].split('.')[0]
    
    #get template
    template = b_monthView.genGroupMonthDetail1(view,index,len(datList),len(koDatList))
    
    template =  template.replace('<số chỉ tiêu không đạt>',str(len(koDatList))) \
                        .replace('<số chỉ tiêu đạt>',str(len(datList))) \
                        .replace('<tổng số chỉ tiêu con>',str(len(evaluationList))) \
                        .replace('<năm>',year).replace('<tháng>',month).replace('<quý>',timeView) \
                        .replace('<đơn vị>',unit).replace('<điều kiện>',condition) \
                        .replace('<tên cụm chỉ tiêu>',f'"{groupKPI}"')
    
    #loại bỏ trường hợp có số chỉ tiêu là 0
    template = template.replace(', số chỉ tiêu đạt là 0 chỉ tiêu','') \
                       .replace('có số chỉ tiêu không đạt là 0 chỉ tiêu, ','')
    
    #detail part generate
    index_detail = random.choice([*range(4)])
    indexMonthNow = random.choice([*range(4)])
    indexMonthBefore = random.choice([*range(3)])
    indexYearBefore = random.choice([*range(2)])
    
    if index == 0: listIter = kpiList
    elif index == 1: listIter = kpiDatList
    else: listIter = kpiKoDatList
    sente = ""
    for kpi in listIter:
        sente += f"""\n+ {mappingOneKPI(timeFind, view, company, kpi,dict_index={"indexNow":indexMonthNow,
                                                                    "indexBefore":indexMonthBefore,
                                                                       "indexYearBefore":indexYearBefore,
                                                                       "index":index_detail}):}"""
    return template + sente
    
def mappingChildInferenceMom(timeFind="",company="",kpi="",index=None):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    dataset = loaded_dict[timeFind]["month"][company][kpi]
    dictKey = convertKeyToIndexDict(dataset)
    
    #get data
    unit = dataset[dictKey[3]].lower()
    condition = dataset[dictKey[4]]
    target = dataset[dictKey[5]]
    kpiNow = dataset[dictKey[6]]
    evaluation = dataset[dictKey[7]].lower()
    
    monthBefore = dataset[dictKey[8]]
    compareMonthBefore = dataset[dictKey[9]]
    yearBefore = dataset[dictKey[convertIndex(-4,len(dictKey))]]
    compareYearBefore = dataset[dictKey[convertIndex(-3,len(dictKey))]]
    groupKPI = dataset[dictKey[convertIndex(-1,len(dictKey))]]
    ############## 
    
    month = timeFind.split('/')[0][1:]
    print(month)
    year = timeFind.split('/')[1]
    print(year)
    
    if unit != "%":
        unit = ' ' + unit
    
    if index is None:
        index = random.choice([0,1])
    
    if index == 0:
        kpiList = listingGroupKPI(loaded_dict,company,groupKPI)
        evaluationList = [loaded_dict[timeFind]["month"][company][kpi]['Đánh giá'] for kpi in kpiList]
        template = b_monthView.genChildInferenceMom(kpiList,evaluationList,index)
    else:
        template = b_monthView.genChildInferenceMom(index=index)
    template =  template.replace('<tên chỉ tiêu con>',f'{kpi}')\
                        .replace('<hiện trạng KPI>',str(kpiNow))\
                        .replace('<tên cụm chỉ tiêu>',f'{groupKPI}')\
                        .replace('<đơn vị>',unit)\
                        .replace('<tên tổng công ty>',company)\
                        .replace('<tháng>',month)\
                        .replace('<năm>',year)
    if index == 1:
        if month == "1":
            template = template.replace(' Trong cùng năm, chỉ tiêu này có số lần không đạt là len([D]), số KPI lần là len([C]) và dự đoán tháng tiếp theo có thể <dự đoán đạt/không đạt>.','')
            return template
        else:
            listDate = helperFunction.generatePrevMonthList(timeFind)
            listKPIKoDat = []
            listKPIDat = []
            
            for i,date in enumerate(listDate):
                eval = loaded_dict[date]["month"][company][kpi]['Đánh giá']
                res = loaded_dict[date]["month"][company][kpi][list(loaded_dict[date]["month"][company][kpi].keys())[6]]
                
                if eval == "Đạt": 
                    listKPIDat.append((i,res))
                else: listKPIKoDat.append((i,res))
            # print(listKPIDat)
            # print(listKPIKoDat)
            
            #==================can improve better==================
            res,eval = helperFunction.predictNextMonth(listKPIDat,listKPIKoDat)
            template =  template.replace('len([D])',str(len(listKPIKoDat))) \
                                .replace('len([C])',str(len(listKPIDat))) \
                                .replace('<dự đoán đạt/không đạt>',eval)\
                                .replace('<dự đoán KPI>',str(res))

    return template            

def retrieveData(dataset):
    dictKey = convertKeyToIndexDict(dataset)
    
    #retrivie data
    unit = dataset[dictKey[3]].lower()
    condition = dataset[dictKey[4]]
    target = dataset[dictKey[5]]
    kpiNow = dataset[dictKey[6]]
    evaluation = dataset[dictKey[7]].lower()
    monthBefore = dataset[dictKey[8]]
    compareMonthBefore = dataset[dictKey[9]]
    yearBefore = dataset[dictKey[convertIndex(-4,len(dictKey))]]
    compareYearBefore = dataset[dictKey[convertIndex(-3,len(dictKey))]]
    groupKPI = dataset[dictKey[convertIndex(-1,len(dictKey))]]
    describeNow = dictKey[6]
    describeMonthBefore = dictKey[8]
    describeYearBefore = dictKey[convertIndex(-4,len(dictKey))]    

    return {
        "unit" : unit,
        "condition" : condition,
        "target" : target,
        "kpiNow" : kpiNow,
        "evaluation" : evaluation,
        "monthBefore" : monthBefore,
        "compareMonthBefore" : compareMonthBefore,
        "yearBefore" : yearBefore,
        "compareYearBefore": compareYearBefore,
        "groupKPI" : groupKPI,
        "describeNow" : describeNow,
        "describeMonthBefore" : describeMonthBefore,
        "describeYearBefore" : describeYearBefore
    }

def mappingCrossView(timeFind,company="",kpi=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    
    #=======================#
    monthDataset = loaded_dict[timeFind]["month"][company][kpi]
    monthDict = retrieveData(monthDataset)
    
    quarterDataset = loaded_dict[timeFind]["quarter"][company][kpi]
    quarterDict = retrieveData(quarterDataset)
    
    yearDataset = loaded_dict[timeFind]["year"][company][kpi]
    yearDict = retrieveData(yearDataset)
    #=======================#
    if yearDict["evaluation"] == "đạt": yearFlag = 0
    else: yearFlag = 1
    templateGen = ""
    if monthDict["evaluation"] == "đạt" and quarterDict["evaluation"] == "đạt":
        templateGen = random.choice([
            b_linkQMView.genMonthViewDatOverview(),
            b_linkQMView.genMonthViewDatDetail(year = yearFlag),
        ])

    if monthDict["evaluation"] == "không đạt" and quarterDict["evaluation"] == "không đạt":
        templateGen = random.choice([
            b_linkQMView.genMonthViewKoDatOverall(),
            b_linkQMView.genMonthViewKoDatDetail(year = yearFlag),
        ])

    if monthDict["evaluation"] == "đạt" and quarterDict["evaluation"] == "không đạt":
        templateGen = b_linkQMView.genTKoDatQDat(year = yearFlag)
    
    if monthDict["evaluation"] == "không đạt" and quarterDict["evaluation"] == "đạt":
        templateGen = b_linkQMView.genTDatQKoDat(year = yearFlag)
    
    month = monthDict["describeNow"].split(' ')[1].split('.')[0]
    quarter = quarterDict["describeNow"].split(' ')[1].split('.')[0]
    year = monthDict["describeNow"].split(' ')[1].split('.')[1]
    unit = monthDict["unit"]
    
    monthKPI = monthDict["kpiNow"]
    quarterKPI = quarterDict["kpiNow"]
    yearKPI = yearDict["kpiNow"]
    
    monthTarget = monthDict["target"]
    quarterTarget = quarterDict["target"]
    yearTarget = yearDict["target"]
    
    if unit == "%":
        unit = ' ' + unit
    
    monthRatio = round(monthKPI / monthTarget,2)
    quarterRatio = round(quarterKPI / quarterTarget,2)
    yearRatio = round(yearKPI / yearTarget,2)
    
    monthDiff = abs(round(monthKPI - monthTarget,2))
    quarterDiff = abs(round(quarterKPI - quarterTarget,2))
    yearDiff = abs(round(yearKPI - yearTarget,2))
    
    templateGen =    templateGen.replace('<tên chỉ tiêu>',kpi) \
                                .replace('<tháng>',month) \
                                .replace('<quý>',quarter) \
                                .replace('<năm>',year) \
                                .replace('<đơn vị>',unit) \
                                .replace('<tổng công ty>',company) \
                                .replace('<hiện trạng KPI tháng>',str(monthKPI)) \
                                .replace('<hiện trạng KPI quý>',str(quarterKPI)) \
                                .replace('<hiện trạng KPI năm>',str(yearKPI)) \
                                .replace('<mục tiêu KPI tháng>',str(monthTarget)) \
                                .replace('<mục tiêu KPI quý>',str(quarterTarget)) \
                                .replace('<mục tiêu KPI năm>',str(yearTarget)) \
                                .replace('<độ chênh lệch tháng>',str(monthDiff)) \
                                .replace('<độ chênh lệch quý>',str(quarterDiff)) \
                                .replace('<độ chênh lệch năm>',str(yearDiff)) \
                                .replace('<tỉ lệ tháng>',str(monthRatio)) \
                                .replace('<tỉ lệ quý>',str(quarterRatio)) \
                                .replace('<tỉ lệ năm>',str(yearRatio)) \
                                .replace('  ',' ')
    return templateGen
    #get data

def mappingViewStat(timeFind,company="",kpi="",choice=""):
    if choice == "":
        choice = random.choice(['season','monthBefore'])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    #=======================#
    
    unit = ""
    groupKPIVal = []
    groupEval = []
    groupTime = []
    if choice == 'season':
        timeList = helperFunction.genPreviousSeason(timeFind)
    else:
        timeList = helperFunction.generatePrevMonthList(timeFind)
        
    for timeEle in timeList:
        dataset = loaded_dict[timeEle]['month'][company][kpi]
        if unit == "":
            unit = dataset['ĐƠN VỊ']
        groupKPIVal.append(dataset[list(dataset.keys())[6]])
        groupTime.append(dataset['Time'])
        groupEval.append(dataset['Đánh giá'])
    
    if choice =='season':
        template = trend_kpiView.genViewStatSeason(groupKPIVal,groupEval,groupTime)
    else:
        template = trend_kpiView.genViewStatMonthBefore(groupKPIVal,groupEval,groupTime)
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    if unit != '%':
        unit = ' ' + unit.lower()
    template =  template.replace('<tên chỉ tiêu>',kpi)\
                        .replace('<tên tổng công ty>',company)\
                        .replace('<tháng>',str(month))\
                        .replace('<năm>',str(year))\
                        .replace('<đơn vị>',unit)
    return template
    
def mappingViewPredict(timeFind,company="",kpi="",choice=""):
    if choice == "":
        choice = random.choice(['season','monthBefore'])
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    #=======================#
    
    unit = ""
    groupKPIVal = []
    if choice == 'season':
        timeList = helperFunction.genPreviousSeason(timeFind)
    else:
        timeList = helperFunction.generatePrevMonthList(timeFind)
        
    for timeEle in timeList:
        dataset = loaded_dict[timeEle]['month'][company][kpi]
        if unit == "":
            unit = dataset['ĐƠN VỊ']
        groupKPIVal.append(dataset[list(dataset.keys())[6]])
        # groupEval.append(dataset['Đánh giá'])
    
    if choice == 'season':
        template = trend_kpiView.genViewPredictYearSeasonBefore()
    else:
        template = trend_kpiView.genViewPredictMonthBefore()
    
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    lenD = year - 2020 + 1
    quarter = helperFunction.getQuarter(month)
    
    resPredict = round(helperFunction.predictView(groupKPIVal),2)
    quarterDataset = loaded_dict[timeEle]['quarter'][company][kpi]
    yearDataset = loaded_dict[timeEle]['year'][company][kpi]
    
    targetQuarter = quarterDataset[list(quarterDataset.keys())[5]]
    targetYear = yearDataset[list(yearDataset.keys())[5]]
    
    evalQuarter = "không đạt"
    evalYear = "không đạt"
    if resPredict >= targetQuarter:
        evalQuarter = "đạt"
    if resPredict >= targetYear:
        evalYear = "đạt"
    
    if unit != '%':
        unit = ' ' + unit.lower()
    template =  template.replace('<tên chỉ tiêu>',kpi)\
                        .replace('<tên tổng công ty>',company)\
                        .replace('<tháng>',str(month))\
                        .replace('<quý>',str(quarter)) \
                        .replace('<năm>',str(year))\
                        .replace('<đơn vị>',unit)\
                        .replace('<kết quả dự báo>',str(resPredict)) \
                        .replace('<mục tiêu KPI quý>',str(targetQuarter)) \
                        .replace('<mục tiêu KPI năm>',str(targetYear)) \
                        .replace('<đạt/không đạt quý>',evalQuarter) \
                        .replace('<đạt/không đạt năm>',evalYear) \
                        .replace('len([D])',str(lenD))
                        
    return template

def mappingViewDetermineTrend(timeFind,company="",kpi=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    #=======================#
    groupKPIVal = []
    timeList = helperFunction.generatePrevMonthList(timeFind)
    unit = ""
    if len(timeList) == 0:
        return f"chỉ tiêu {kpi} tính đến {timeFind} chưa đủ dữ kiện để dự đoán trend của cả năm."
    timeList.append(timeFind)
    for timeEle in timeList:
        dataset = loaded_dict[timeEle]['month'][company][kpi]
        if unit == "":
            unit = dataset['ĐƠN VỊ']
        groupKPIVal.append(dataset[list(dataset.keys())[6]])
    
    angle,res = helperFunction.determineTrend(groupKPIVal)
    indexLevel = 1
    indexDesc = 1
    
    if angle >= -10 and angle <= 10: 
        indexDesc = 2
        indexLevel = 2
    elif angle <= 30 or angle >= -30: 
        if angle >= 0:
            indexDesc = 0
        indexLevel = 1
    else: 
        if angle >= 0:
            indexDesc = 0
        indexLevel = 0
    res = round(res,2)
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    
    if unit != '%':
        unit = ' ' + unit.lower()
    
    template = trend_kpiView.genViewDetermineTrend(indexDesc,indexLevel)
    template =  template.replace('<tên chỉ tiêu>',kpi) \
                        .replace('<tên tổng công ty>',company) \
                        .replace('<tháng>',str(month))\
                        .replace('<năm>',str(year))\
                        .replace('<đơn vị>',unit)\
                        .replace('<kết quả dự báo>',str(res))
    return template
                        
def mappingViewExplainResult(timeFind,company="",kpi=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    #============#
    timeList = helperFunction.generatePrevMonthList(timeFind)
    if len(timeList) <= 1:
        return f"chỉ tiêu {kpi} tính đến {timeFind} chưa đủ dữ kiện để giải trình, điều kiện cần là tháng hiện tại >= 3"
    groupKPIVal = []
    timeList = helperFunction.generatePrevMonthList(timeFind)
    
    unit = ""
    for timeEle in timeList:
        dataset = loaded_dict[timeEle]['month'][company][kpi]
        if unit == "":
            unit = dataset['ĐƠN VỊ']
        groupKPIVal.append(dataset[list(dataset.keys())[6]])
        
    angle,res = helperFunction.determineTrend(groupKPIVal)
    dataset = loaded_dict[timeEle]['month'][company][kpi]
    
    res = round(res,2)
    kpiNow = round(dataset[list(dataset.keys())[6]],2)
    evaluation = dataset[list(dataset.keys())[7]]
    
    abs_distance = abs(res - kpiNow)
    if evaluation == "Đạt":
        if abs_distance <= 10: index = 0
        else: index = 1
    else:
        if abs_distance <= 10: index = 2
        else: index = 3
    
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    if unit != '%':
        unit = ' ' + unit.lower()
    
    template = trend_kpiView.genViewExplainResult(index)
    template =  template.replace('<tháng>',str(month)) \
                        .replace('<năm>',str(year)) \
                        .replace('<tên chỉ tiêu>',kpi) \
                        .replace('<hiện trạng KPI tháng>',str(kpiNow)) \
                        .replace('<đơn vị>',unit) \
                        .replace('len([A])',str(len(timeList))) \
                        .replace('<kết quả dự báo>',str(res))
    return template
    
dict_map_view = {
    "month" : 0,
    "quarter" : 1,
    "year" : 2
}
    
def mappingViewOneKPIStat(timeFind,view = "",company="",kpi="",choose=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if view == "":
        view = random.choice(["month","month","month","quarter","year"])
    if kpi == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpi = random.choice(listingGroupKPI(loaded_dict,company,groupKPI))
    if choose == "":
        choose = random.choice(["mean","max","min"])

    month = int(timeFind.split('/')[0])
    quarter = helperFunction.getQuarter(month)
    year = int(timeFind.split('/')[1])
    
    flagMeanMM = 0
    flagMinMax = 0
    if choose != "mean":
        flagMeanMM = 1
        if choose == "min": flagMinMax = 1
    timeList = helperFunction.generatePrevMonthList(timeFind)
    if len(timeList) <= 1:
        return f"chỉ tiêu {kpi} tính đến {timeFind} chưa đủ dữ kiện để giải trình, điều kiện cần là tháng hiện tại >= 2 để xài chức năng này"
    timeList = helperFunction.generatePrevMonthList(timeFind)
    unit=""
    condition=""
    groupKPIVal = []
    for timeEle in timeList:
        dataset = loaded_dict[timeEle][view][company][kpi]
        if unit == "": unit = dataset['ĐƠN VỊ']
        if condition == "": condition = dataset['ĐIỀU KIỆN']
        groupKPIVal.append(dataset[list(dataset.keys())[6]])
    
    template = stat_kpiView.genViewOneKpiStat(flagMeanMM,dict_map_view[view],flagMeanMM,flagMinMax)
    monthFind = ""
    quarterFind = ""
    if choose == "mean": 
        resCompute = np.mean(groupKPIVal)
    elif choose == "min": 
        resCompute = min(groupKPIVal)
        index = np.argmin(resCompute)
        monthFind =  int(timeList[index].split('/')[0])
    elif choose == "max": 
        resCompute = max(groupKPIVal)
        index = np.argmax(groupKPIVal)
        monthFind =  int(timeList[index].split('/')[0])
    if monthFind != "":
        quarterFind = helperFunction.getQuarter(monthFind)
    
    resCompute = round(resCompute,2)
    if unit != "%":
        unit = ' ' + unit
        
    template =  template.replace('<tên chỉ tiêu>',kpi) \
                        .replace('<tổng công ty>',company) \
                        .replace('len([A])',str(len(timeList))) \
                        .replace('<đơn vị>',unit) \
                        .replace('<tháng>',str(month)) \
                        .replace('<quý>',str(quarter)) \
                        .replace('<năm>',str(year)) \
                        .replace('<tháng-m>',str(monthFind)) \
                        .replace('<quý-m>',str(quarterFind)) \
                        .replace('<năm-m>',str(year)) \
                        .replace('<hiện trạng KPI-m>',str(resCompute)) \
                        .replace('<kết quả KPI trung bình>',str(resCompute)) \
                        .replace('<điều kiện>',condition)
    
    return template
  
def mappingViewOneGroupKPIStat(timeFind,view="",company="",groupKPI="",choose=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if view == "":
        view = random.choice(["month","month","month","quarter","year"])
    if groupKPI == "":
        parentSet = loadParentSet(loaded_dict,company)
        groupKPI = random.choice(list(parentSet))
        kpiList = listingGroupKPI(loaded_dict,company,groupKPI)
    if choose == "":
        choose = random.choice(["mean","max","min"])
    
    month = int(timeFind.split('/')[0])
    quarter = helperFunction.getQuarter(month)
    year = int(timeFind.split('/')[1])
    
    flagMeanMM = 0
    flagMinMax = 0
    if choose != "mean":
        flagMeanMM = 1
        if choose == "min": flagMinMax = 1
    
    unit=""
    condition=""
    groupKPIVal = []
    kpiFind=""
    
    for kpi in kpiList:
        dataset = loaded_dict[timeFind][view][company][kpi]
        if unit == "": unit = dataset['ĐƠN VỊ']
        if condition == "": condition = dataset['ĐIỀU KIỆN']
        groupKPIVal.append(dataset[list(dataset.keys())[6]])
    
    if choose == "mean": 
        resCompute = np.mean(groupKPIVal)
    elif choose == "min": 
        resCompute = min(groupKPIVal)
        index = np.argmin(resCompute)    
        kpiFind = kpiList[index]
    elif choose == "max": 
        resCompute = max(groupKPIVal)
        index = np.argmax(groupKPIVal)
        kpiFind = kpiList[index]
    
    resCompute = round(resCompute,2)
    
    template = stat_kpiView.genViewOneGroupKPIStat(None,dict_map_view[view],flagMeanMM,flagMinMax)
    if unit != "%":    
        unit = " " + unit
    template =  template.replace('<tên chỉ tiêu-m>',kpiFind) \
                        .replace('<tên chỉ tiêu>',kpiFind) \
                        .replace('<tổng công ty>',company) \
                        .replace('<tên tổng công ty>',company) \
                        .replace('<tên cụm chỉ tiêu>',groupKPI) \
                        .replace('<đơn vị>',unit) \
                        .replace('<tháng>',str(month)) \
                        .replace('<quý>',str(quarter)) \
                        .replace('<năm>',str(year)) \
                        .replace('<KPI-m>',str(resCompute)) \
                        .replace('<KPI trung bình>',str(resCompute)) \
                        .replace('<điều kiện>',condition)

    return template

def mappingCtyDescribe(timeFind,view="",company=""):
    if company == "":
        company = random.choice(["VTS","VTT","VDS","VTPOST"])
    if view == "":
        view = random.choice(["month","quarter","year"])
    
    groupKPI = []
    groupEval = []
    for kpi in loaded_dict[timeFind][view][company].keys():
        groupKPI.append(kpi)
        groupEval.append(loaded_dict[timeFind][view][company][kpi]['Đánh giá'])
            
    template = a_tongCtyView.genCtyDescribe(groupKPI,groupEval,dict_map_view[view])
    
    month = int(timeFind.split('/')[0])
    year = int(timeFind.split('/')[1])
    quarter = helperFunction.getQuarter(month)
    
    template =  template.replace('<tổng công ty>',company) \
                        .replace('<tháng>',str(month)) \
                        .replace('<quý>',str(quarter)) \
                        .replace('<năm>',str(year))
    
    return template

# print(mappingCtyDescribe('01/2023'))      
# mappingViewExplainResult('06/2023')
# print(mappingCrossView('01/2020'))
# print(mappingChildInferenceMom('02/2020'))
# print(mappingGroupMonthDetail('01/2020',view="",company="",groupKPI="",index = 1))
# print(mappingOneKPI('01/2020') + '.')