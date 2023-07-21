import random

def genMonthDesc():
    listMonthDesc = [
        'trong quý <tháng> năm <năm>'
        'T<tháng>/<năm>'
    ]
    
    return random.choice(listMonthDesc)

def genQuarterDesc():
    listQuarterDesc = [
        'trong quý <quý> năm <năm>'
        'Q<quý>/<năm>'
    ]
    
    return random.choice(listQuarterDesc)

def genYearDesc():
    listYearDesc = [
        'trong năm <năm>'
        'N<năm>'
    ]
    
    return random.choice(listYearDesc)

def genCtyDescribe(dat=1,all=2,choice=1):
    A = ""
    B = ""
    if dat != all:
        B = ", có số chỉ tiêu không đạt là <số KPIs không đạt>/<tổng số> KPIs"
    if dat != 0:
        A = "có số chỉ tiêu KPI đạt là <số đạt>/<tổng số> KPIs"
    return f"<tổng công ty> {A} {B}".replace("  "," ")

print(genCtyDescribe())