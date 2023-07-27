import random

#I.OneKPI
#==========genPreAdv==========
############################################
def genPrefixAdv():
    listAdv = [
        "Hiện tại",
        "Điểm dữ liệu này cho ta quan sát",
        "Ta thấy được rằng",
        "Ta nhận xét rằng",
        'Dữ liệu cho thấy',
        "Dữ liệu chỉ ra",
        ""
    ]
    return random.choice(listAdv)
#==========genPreAdv==========

#==========genDesc==========
##(quý <quý> năm <năm> | <quý>/<năm>)
def genQuaterYear():
    listQuaterYear = [
       "quý <quý> năm <năm>",
       "Q<quý>/<năm>",
       "Q<quý> năm <năm>"
    ]
    
    return random.choice(listQuaterYear)

##(tổng công ty|đơn vị|)
def genCompanyDesc():
    listCompanyDesc = [
        "tổng công ty",
        "đơn vị",
        "công ty",
        ""
    ]
    
    return random.choice(listCompanyDesc)

##(kết quả là | đã)
def genResultDesc():
    listResultDesc = [
        "có kết quả", 
        "được đánh gía",
        "ghi nhận",
        
    ]
    
    return random.choice(listResultDesc)

############################################
def genPrefixDesc():
    listPrefixDesc = [
        f"trong {genQuaterYear()}, chỉ tiêu <tên chỉ tiêu> của {genCompanyDesc()} <tổng công ty> {genResultDesc()} là <đạt/không đạt>",
        f"trong {genQuaterYear()}, {genCompanyDesc()} <tổng công ty> có chỉ tiêu <tên chỉ tiêu> {genResultDesc()} là <đạt/không đạt>",
        f"chỉ tiêu <tên chỉ tiêu> của {genCompanyDesc()} <tên tổng công ty> trong {genQuaterYear()} {genResultDesc()} là <đạt/không đạt>",
        f"{genCompanyDesc()} <tên tổng công ty> có chỉ tiêu <tên chỉ tiêu> trong {genQuaterYear()} {genResultDesc()} là <đạt/không đạt>",
        f"{genCompanyDesc()} <tên tổng công ty> trong {genQuaterYear()} có chỉ tiêu <tên chỉ tiêu> {genResultDesc()} là <đạt/không đạt>",
    ]
    
    return random.choice(listPrefixDesc)
#==========genDesc==========

#==========genOneKPI==========
##(tăng|giảm|chênh lệch)
def genDiffDesc(sign = 1):
    if sign == 1:
        return "tăng"
    elif sign == -1:
        return "giảm"
    
    listDiffDesc = [
        "chênh lệch",
        "sai khác"
    ]
    return random.choice(listDiffDesc)

##(gấp|chỉ bằng)
def genRatioDesc(res = 1):
    if res >= 1:
        return "gấp"
    return "chỉ bằng"

##(quý|hiện đạt được|)
def genQuaterKPIDesc():
    listQuaterKPIDesc = [
        "quý",
        "hiện có được",
        ""
    ]
    
    return random.choice(listQuaterKPIDesc)

##(,(tăng|giảm)<Độ tăng giảm so với KPIs mục tiêu>,(gấp|chỉ bằng)<Tỉ lệ so với KPIs mục tiêu>)
def genDetailKPIQuater(sign=1,res=1,index=None):
    listDetailKPIQuater = [
        f"{genDiffDesc(sign)} <Độ tăng giảm so với KPIs mục tiêu><đơn vị>, {genRatioDesc(res)} <Tỉ lệ so với KPIs mục tiêu> lần",
        f"{genRatioDesc(res)} <Tỉ lệ so với KPIs mục tiêu> lần, {genDiffDesc(sign)} <Độ tăng giảm so với KPIs mục tiêu><đơn vị>",
        ""
    ]
    
    if index is None:
        return random.choice(listDetailKPIQuater)
    
    assert(index < len(listDetailKPIQuater))
    return listDetailKPIQuater[index]

##(đề ra là <mục tiêu KPI><đơn vị>)
def genDetailTarget():
    listDetailTarget = [
        "đề ra là <mục tiêu KPI><đơn vị>",
        "đặt ra là <mục tiêu KPI><đơn vị>",
        "có giá trị <mục tiêu KPI><đơn vị>",
        ""
    ]
    return random.choice(listDetailTarget)

##(trong khi mục tiêu| so với mục tiêu KPI)
def genDescribeTarget():
    listDescribeTarget = [
        "trong khi mục tiêu",
        "so với mục tiêu KPI",
    ]
    
    return random.choice(listDescribeTarget)

############################################
def genOneKPI(sign=1,ratio=1,index=None):
    listOneKPI = [
        "có kêt quả là <hiện trạng KPI><đơn vị>", #View ngắn gọn
        f"chỉ tiêu hiện đã {genRatioDesc(ratio)} <Tỉ lệ so với KPIs mục tiêu> lần so với mục tiêu KPI ban đầu {genDetailTarget()}", #View bao quát - bằng tỉ lệ
        f"với hiện trạng là <hiện trạng KPI><đơn vị>, {genDiffDesc(sign)} <Độ tăng giảm so với KPIs mục tiêu><đơn vị> so với mục tiêu KPI là <mục tiêu KPI><đơn vị>", #View bao quát - bằng delta
        f"với kết quả {genQuaterKPIDesc()} là <hiện trạng KPI><đơn vị> {genDescribeTarget()} đề ra là <mục tiêu KPI><đơn vị> {genDetailKPIQuater()}" #View chi tiết
    ]
    
    if index is None:
        return random.choice(listOneKPI)
    
    assert(index < len(listOneKPI))
    return listOneKPI[index]
#==========genOneKPI==========

#==========compareKPIQuaterBefore==========
##(1 góc nhìn khác|bên cạnh đó|tuy nhiên)
def genDescAdv():
    listDescAdv = [
        "1 góc nhìn khác",
        "bên cạnh đó",
        "tuy nhiên",
        ""
    ]
    
    return random.choice(listDescAdv)

##(so với quý trước|trong khi <quý - 1> /<năm>)
def genQuaterBeforeDesc():
    listQuaterBeforeDesc = [
        "quý trước",
        "Q<quý-1>/<năm>",
        "vào quý <quý-1> năm <năm>",
        "quý trước đó",
    ]
    
    return random.choice(listQuaterBeforeDesc)
    
##(tăng|giảm)<Độ tăng giảm so với KPI quý trước>|(gấp|chỉ bằng)<Tỉ lệ so với KPI quý trước>lần)
def genDetailKPIQuaterBefore(sign=1,ratio=1):
    listDetailKPIQuaterBefore = [
        f"{genDiffDesc(sign)} <Độ tăng giảm so với KPI quý trước><đơn vị>",
        f"{genRatioDesc(ratio)} <Tỉ lệ so với KPI quý trước> lần",
    ]
    
    return random.choice(listDetailKPIQuaterBefore)

############################################
def genCompareKPIQuaterBefore(sign=1,ratio=1,index=None):
    listCompareKPIQuaterBefore = [
        f"đối với KPI quý trước có được là <KPI quý trước><đơn vị>", #View ngắn gọn
        f"{genDetailKPIQuaterBefore(sign,ratio)} so với KPI là {genQuaterBeforeDesc()}", #View bao quát hơn
        f"{genDescAdv()} trong khi {genQuaterBeforeDesc()} đạt <KPI quý trước><đơn vị>, {genDetailKPIQuater(sign,ratio)}", #View thể hiện chi tiết
    ]
    
    if index is None:
        return random.choice(listCompareKPIQuaterBefore)
    
    assert(index < len(listCompareKPIQuaterBefore))
    return listCompareKPIQuaterBefore[index]
#==========compareKPIQuaterBefore==========

#==========compareKPIMYearBefore==========
##(Ngoài ra|Trong khi đó|)
def genDescAdvYear():
    listDescAdvYear = [
        "ngoài ra",
        "trong khi đó",
        "dữ liệu còn cho biết",
        ""
    ]
    
    return random.choice(listDescAdvYear)

##(so với cùng kỳ năm ngoái | với <quý>/<năm -1> | quý <quý> năm <năm -1>)
def genYearBeforeDesc():
    listYearBeforeDesc = [
        "so với cùng kỳ năm ngoái",
        "với <quý>/<năm-1>",
        "quý <quý> năm <năm-1>",
        "cùng kỳ năm trước"
    ]
    
    return random.choice(listYearBeforeDesc)

##(,(tăng|giảm)<Độ tăng giảm so với KPI cùng kỳ năm trước><đơn vị>|,(gấp|chỉ bằng)<Tỉ lệ so với KPI cùng kỳ năm trước>lần|)
def genDetailKPIYearBefore(sign=1,ratio=1):
    listDetailKPIYearBefore = [
        f"{genDiffDesc(sign)} <Độ tăng giảm so với KPI cùng kỳ năm trước><đơn vị>",
        f"{genRatioDesc(ratio)} <Tỉ lệ so với KPI cùng kỳ năm trước> lần",
        ""
    ]
    
    return random.choice(listDetailKPIYearBefore)
############################################
def genCompareKPIMYearBefore(sign=1,ratio=1,index=None):
    listCompareKPIMYearBefore = [
        f"{genDetailKPIYearBefore(sign,ratio)} so với kết quả là {genYearBeforeDesc()}", #View bao quát
        f"{genDescAdvYear()} {genYearBeforeDesc()} chỉ tiêu có được là <KPI cùng kỳ năm trước><đơn vị> {genDetailKPIYearBefore(sign,ratio)}", #View thể hiện chi tiết
    ]
    
    if index is None:
        return random.choice(listCompareKPIMYearBefore)
    
    assert(index < len(listCompareKPIMYearBefore))
    return listCompareKPIMYearBefore[index]
#==========compareKPIMYearBefore==========

#==========genFullQuaterView==========
############################################
def genFullView(sign=[1,1,1],ratio=[1,1,1],indexQuaterNow=None,indexQuaterBefore=None,indexYearBefore=None,index=None):
    prefix = genOneKPI(sign=sign[0],ratio=ratio[0],index=indexQuaterNow)
    Quater = genCompareKPIQuaterBefore(sign=sign[1],ratio=ratio[1],index=indexQuaterBefore)
    year = genCompareKPIMYearBefore(sign=sign[2],ratio=ratio[2],index=indexYearBefore)
    listFullQuaterView = [
        f"{prefix}", #chỉ quý hiện tại
        f"{prefix}. {Quater}", #so sánh thêm quý trước đó
        f"{prefix}. {year}", #so sánh cùng kỳ quý
        f"{prefix}. {Quater}. {year}", #so sánh cả quý trước và cùng kỳ quý
    ]
    
    if index is None:
        return random.choice(listFullQuaterView).replace("  "," ")
    
    assert(index < len(listFullQuaterView))
    return listFullQuaterView[index].replace("  "," ")
#==========genFullQuaterView==========

if __name__ == "__main__":
    print(genPrefixAdv() + ' ' + genPrefixDesc() + ' ' + genFullView())