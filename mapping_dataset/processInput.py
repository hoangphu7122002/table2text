def getListFind(findName):
    with open(findName,'r',encoding='utf-8') as f:
        res = f.read()
        listRes = res.split('.\n###############################\n')
    return listRes
        
print(len(getListFind('dataset/crossView.txt')))