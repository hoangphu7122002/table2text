import pickle
import random
import helperFunction

import sys
localHost = 'C://Users//Administrator//Desktop//largeProject//template_generate//'

sys.path.append(f'{localHost}monthView')
sys.path.append(f'{localHost}quarterView')
sys.path.append(f'{localHost}yearView')

from monthView import a_monthView
from monthView import b_monthView
from quarterView import a_quaterView
from yearView import a_yearView

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
    template  = template.replace('<tên chỉ tiêu>',f'"{kpi}"') \
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
    
print(mappingGroupMonthDetail('01/2020',view="",company="",groupKPI="",index = 1))
# print(mappingOneKPI('01/2020','quarter') + '.')