import helperFunction
import mapping_dataset
import random
import sys

listDate = helperFunction.generateListDate()
date = random.choice(listDate)

listView = {
    "View 1 chỉ tiêu" : mapping_dataset.mappingOneKPI(date),
    "View cụm chỉ tiêu - tổng quan" : mapping_dataset.mappingGroupMonthOverall(date),
    "View cụm chỉ tiêu - chi tiết" : mapping_dataset.mappingGroupMonthDetail(date),
    "View cụm chỉ tiêu - infer mẹ" : mapping_dataset.mappingChildInferenceMom(date),
    "View Cross" : mapping_dataset.mappingCrossView(date),
    "View thống kê" : mapping_dataset.mappingViewStat(date),
    "View dự báo" : mapping_dataset.mappingViewPredict(date),
    "View giải trình với kết quả hiện có" : mapping_dataset.mappingViewExplainResult(date),
    "View xem xét xu hướng" : mapping_dataset.mappingViewDetermineTrend(date),
    "View stat 1 chỉ tiêu" : mapping_dataset.mappingViewOneKPIStat(date),
    "View stat 1 cụm chỉ tiêu" : mapping_dataset.mappingViewOneGroupKPIStat(date),
    "View tổng công ty" : mapping_dataset.mappingCtyDescribe(date),
}

def convertKeyToIndexDict(dictRes):
    keyList = list(dictRes.keys())
    dictKey = dict()
    for index,ele in enumerate(keyList):
        dictKey[index] = ele
    return dictKey

if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise "error"
    key = int(sys.argv[1])
    dictKey = convertKeyToIndexDict(listView)
    
    print(dictKey[key])
    print("=====================")
    print(listView[dictKey[key]])        
    