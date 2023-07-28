import random

def genMonthDesc():
    listMonthDesc = [
        'trong quý <tháng> năm <năm>',
        'vào T<tháng>/<năm>'
    ]
    
    return random.choice(listMonthDesc)

def genQuarterDesc():
    listQuarterDesc = [
        'trong quý <quý> năm <năm> (cụ thể tháng <tháng> năm <năm>)',
        'vào Q<quý>/<năm> (cụ thể T<tháng>/<năm>)'
    ]
    
    return random.choice(listQuarterDesc)

def genYearDesc():
    listYearDesc = [
        'trong năm <năm> (cụ thể tháng <tháng> năm <năm>)',
        'vào N<năm> (cụ thể T<tháng>/<năm>)'
    ]
    
    return random.choice(listYearDesc)

dict_choice = {
    0 : genMonthDesc(),
    1 : genQuarterDesc(),
    2 : genYearDesc()
}

def genDetail(groupKPI,groupEval):
    assert(len(groupKPI) == len(groupEval))
    
    sente = ""
    for kpi,res in zip(groupKPI,groupEval):
        sente += f'\n+ Chỉ tiêu "{kpi}" có kết quả là: {res}'
    return sente    

def genCtyDescribe(groupKPI=['A','B','C'],groupEval=['Đạt','Không đạt','Đạt'],choice=1):
    A = ""
    B = ""
    
    dat = len([ele for ele in groupEval if ele == "Đạt"])
    all = len(groupKPI)
    koDat = all - dat
    if dat != all:
        B = f", có số chỉ tiêu không đạt là {koDat}/{all} KPIs"
    if dat != 0:
        A = f"có số chỉ tiêu KPI đạt là {dat}/{all} KPIs"
    if random.random() < 0.3:
        postFix = genDetail(groupKPI,groupEval)
    else:
        postFix = ""
    return f"{dict_choice[choice]}, <tổng công ty> {A} {B} {postFix}".replace("  "," ")