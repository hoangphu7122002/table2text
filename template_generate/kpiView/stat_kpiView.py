import random

#===============ViewOneKpiStat===============
##(tháng|quý|năm)
def genStyleView(index = None):
    listStyleView = [
        "tháng",
        "quý",
        "năm"
    ]
    
    if index is None:
        return random.choice(listStyleView)
    
    assert(index < len(listStyleView))
    return listStyleView[index]

##(tháng <tháng> năm <năm>|quý <quý> năm <năm>|năm<năm>)
def genFullView1(index=None):
    listFullView1 = [
        "tháng <tháng> năm <năm>",
        "quý <quý> năm <năm>",
        "năm <năm>"
    ]
    
    if index is None:
        return random.choice(listFullView1)
    
    assert(index < len(listFullView1))
    return listFullView1[index]

##("T<tháng>/<năm>"|"Q<quý>/<năm>"|"N<năm>")
def genFullView2(index=None):
    listFullView2 = [
        "T<tháng>/<năm>",
        "Q<quý>/<năm>",
        "N<năm>"
    ]
    
    if index is None:
        return random.choice(listFullView2)
    
    assert(index < len(listFullView2))
    return listFullView2[index]

##(genFullView1() | genFullView2())
def genChooseView(index=None,index_detail = None):
    if index is None:
        return random.choice([genFullView1(index_detail),genFullView2(index_detail)])
    
    assert(index < 2)
    if index == 0: return genFullView1(index_detail)
    return genFullView2(index_detail)

##(tháng <tháng-m> năm <năm-m>|quý <quý-m> năm <năm-m>|năm<năm-m>)
def genStatView1(index=None):
    listStatView1 = [
        "tháng <tháng-m> năm <năm-m>",
        "quý <quý-m> năm <năm-m> (cụ thể là tháng <tháng-m> năm <năm-m>)",
        "năm <năm-m> (cụ thể là tháng <tháng-m> năm <năm-m>)"
    ]
    
    if index is None:
        return random.choice(listStatView1)
    
    assert(index < len(listStatView1))
    return listStatView1[index]

##("T<tháng-m>/<năm-m>"|"Q<quý-m>/<năm-m>"|"N<năm-m>")
def genStatView2(index=None):
    listStatView2 = [
        "T<tháng-m>/<năm-m>",
        "Q<quý-m>/<năm-m>",
        "N<năm-m>"
    ]
    
    if index is None:
        return random.choice(listStatView2)
    
    assert(index < len(listStatView2))
    return listStatView2[index]

##(genStatView1() | genStatView2())
def genChooseStatView(index=None,index_detail = None):
    if index is None:
        return random.choice([genStatView1(index_detail),genStatView2(index_detail)])
    
    assert(index < 2)
    if index == 0: return genStatView1(index_detail)
    return genStatView2(index_detail)

##(lớn nhất | bé nhất)
def genMinMax(index=None):
    listMinMax = [
        "lớn nhất",
        "bé nhất"
    ]
    
    if index is None: return random.choice(listMinMax)
    assert(index < len(listMinMax))
    
    return listMinMax[index]

##(đạt được mốc <KPI trung bình> là <kết quả KPI trung bình><đơn vị> | thì vào (tháng <tháng-m> năm <năm-m>| T<tháng-m>/<năm-m>| quý <quý-m> năm <năm -m> | Q<quý-m>/<năm-m>| N<năm-m>|năm <năm-m>) đạt được kết quả KPI (lớn nhất | bé nhất) là <hiện trạng KPI-m><đơn vị>)
def genViewStat(index = None, indexStatView = None, indexDescStatView=None, flagMinMax=None):
    listDetail = random.choice([
        "với điều kiện để đạt được là <điều kiện>",
        ""
    ])
    listViewStat = [
        f"đạt được mốc KPI trung bình là <kết quả KPI trung bình><đơn vị>", #kpi trung bình
        f"thì vào {genChooseStatView(indexStatView,indexDescStatView)} đạt được kết quả KPI {genMinMax(flagMinMax)} là <hiện trạng KPI-m><đơn vị> {listDetail}", #kpi min, max
    ]
    
    if index is None:
        return random.choice(listViewStat)
    assert(index < len(listViewStat))
    
    return listViewStat[index]

#########################################
def genViewOneKpiStat(index=None,indexView=None,flagMeanMM=None,flagMinMax=None):
    indexStyle = random.choice([0,1])
    #indexView has value [0,1,2] correspond ["tháng","quý","năm"]
    
    listViewOneKpiStat = [
        f"Trong len([A]) {genStyleView(indexView)} gần nhất tính đến {genChooseView(indexStyle,indexView)}, chỉ tiêu <tên chỉ tiêu> của <tổng công ty> {genViewStat(flagMeanMM,indexStyle,indexView,flagMinMax)}.",
        f"Với chỉ tiêu <tên chỉ tiêu> của tổng công ty <tổng công ty> trong len([A]) {genStyleView(indexView)} gần nhất tính đến {genChooseView(indexStyle,indexView)} {genViewStat(flagMeanMM,indexStyle,indexView,flagMinMax)}."
    ]
    
    if index is None:
        return random.choice(listViewOneKpiStat)
    assert(index < len(listViewOneKpiStat))
    
    return listViewOneKpiStat[index]

#===============ViewOneKpiStat===============

#===============genViewOneGroupKPIStat===============
##(của tổng công ty <tên tổng công ty>|) 
def genDescCompany(index=None):
    listDescCompany = [
        "của tổng công ty <tên tổng công ty>",
        ""
    ]
    
    if index is None:
        return random.choice(listDescCompany)
    assert(index < len(listDescCompany))
    
    return listDescCompany[index]

##(với <KPI-m><đơn vị>|)
def genDescDetail(index=None):
    listDescDetail = [
        "",
        "với <KPI-m><đơn vị>"
    ]
    
    if index is None:
        return random.choice(listDescDetail)
    assert(index < len(listDescDetail))
    
    return listDescDetail[index]

##genMean()
def genMean(index=None):
    listMeanDescribe = [
        "có trung bình KPI đạt được là <KPI trung bình><đơn vị>",
        "cụm chỉ tiêu <tên cụm chỉ tiêu> đạt được trung bình KPI là <KPI trung bình><đơn vị>"
    ]
    
    if index is None:
        return random.choice(listMeanDescribe)
    assert(index < len(listMeanDescribe))
    
    return listMeanDescribe[index]

##genMinMaxDesc()
def genMinMaxDesc(index=None,flagMinMax=None):
    listMinMaxDesc = [
        f"có KPI {genMinMax(flagMinMax)} đạt được là <KPI-m><đơn vị> là chỉ tiêu <tên chỉ tiêu-m>",
        f"<tên chỉ tiêu> là chỉ tiêu đạt trạng thái KPI {genMinMax(flagMinMax)} {genDescDetail(index)} trong cụm chỉ tiêu <tên cụm chỉ tiêu>"
    ]
    
    if index is None:
        return random.choice(listMinMaxDesc)
    
    assert(index < len(listMinMaxDesc))
    
    return listMinMaxDesc[index]

#################################################
def genViewOneGroupKPIStat(index=None,indexView=None,flagMeanMM=None,flagMinMax=None):
    indexStyle = random.choice([0,1])
    #indexView has value [0,1,2] correspond ["tháng","quý","năm"]
    milestone = genMean(index)
    if flagMeanMM == 1:
        milestone = genMinMaxDesc(index,flagMinMax)
    listOneGroupKPIStat = [
        f"Cụm chỉ tiêu <tên cụm chỉ tiêu> {genDescCompany()} trong {genChooseView(indexStyle,indexView)} {milestone}",
        f"Vào {genChooseView(indexStyle,indexView)}, {milestone} {genDescCompany()}.",
    ]
    
    if index is None:
        return random.choice(listOneGroupKPIStat)
    assert(index < len(listOneGroupKPIStat))
    
    return listOneGroupKPIStat[index]
#===============genViewOneGroupKPIStat===============

if __name__ == '__main__':
    print(genViewOneGroupKPIStat(indexView=random.choice([0,1,2])))