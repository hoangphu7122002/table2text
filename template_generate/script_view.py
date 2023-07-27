import helperFunction
import mapping_dataset
import random

listDate = helperFunction.generateListDate()
##View oneKPI

def scriptOneKPI():
    with open('oneKPI.txt','w',encoding="utf-8") as f:
        for _ in range(10000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingOneKPI(date) + '.')
                f.write('\n###############################\n')
            except:
                continue

def scriptGroupMonthOverall():
    with open('GroupMonthOverall.txt','w',encoding="utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingGroupMonthOverall(date))
                f.write('\n###############################\n')
            except:
                continue

def scriptGroupMonthDetail():
    with open('GroupMonthDetail.txt','w',encoding = "utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingGroupMonthDetail(date))
            except:
                continue

def scriptChildInferenceMom():
    with open('ChildInferenceMom.txt','w',encoding = "utf-8") as f:
        for _ in range(2000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingChildInferenceMom(date))
            except:
                continue

def scriptCrossView():
    with open('crossView.txt','w',encoding="utf-8") as f:
        for _ in range(4000):
            try:
                date = random.choice(listDate)
                f.write(mapping_dataset.mappingCrossView(date))
            except:
                continue