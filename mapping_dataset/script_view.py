import helperFunction
import mapping_dataset
import random

listDate = helperFunction.generateListDate()
##View oneKPI

def scriptOneKPI():
    with open('dataset/oneKPI.txt','w',encoding="utf-8") as f:
        for _ in range(20000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingOneKPI(date) + '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptGroupMonthOverall():
    with open('dataset/GroupMonthOverall.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingGroupMonthOverall(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptGroupMonthDetail():
    with open('dataset/GroupMonthDetail.txt','w',encoding = "utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingGroupMonthDetail(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptChildInferenceMom():
    with open('dataset/ChildInferenceMom.txt','w',encoding = "utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingChildInferenceMom(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptCrossView():
    with open('dataset/crossView.txt','w',encoding="utf-8") as f:
        for _ in range(4000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingCrossView(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue
            
def scriptViewStat():
    with open('dataset/viewStat.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingViewStat(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptViewPredict():
    with open('dataset/viewPredict.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingViewPredict(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptViewDetermineTrend():
    with open('dataset/viewDetermineTrend.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingViewDetermineTrend(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptViewExplainResult():
    with open('dataset/viewExplainResult.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingViewExplainResult(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptViewOneKPIStat():
    with open('dataset/viewOneKPIStat.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingViewOneKPIStat(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptViewOneGroupKPIStat():
    with open('dataset/viewOneGroupKPIStat.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingViewOneGroupKPIStat(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptCtyDescribe():
    with open('dataset/viewCtyDescribe.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingViewOneGroupKPIStat(date)+ '.')
                f.write('\n###############################\n')
            except:
                continue

if __name__ == "__main__":
    # scriptOneKPI()
    # scriptGroupMonthOverall()
    # scriptGroupMonthDetail()
    # scriptChildInferenceMom()
    # scriptViewStat()
    # scriptViewPredict()
    # scriptViewDetermineTrend()
    scriptCrossView()
    scriptViewExplainResult()
    # scriptViewOneKPIStat()
    # scriptViewOneGroupKPIStat()
    # scriptCtyDescribe()