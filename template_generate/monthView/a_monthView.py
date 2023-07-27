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
        ""
    ]
    return random.choice(listAdv)
#==========genPreAdv==========

#==========genDesc==========
##(tháng <tháng> năm <năm> | <tháng>/<năm>)
def genMonthYear():
    listMonthYear = [
       "tháng <tháng> năm <năm>",
       "T<tháng>/<năm>"
    ]
    
    return random.choice(listMonthYear)

##(tổng công ty|đơn vị|)
def genCompanyDesc():
    listCompanyDesc = [
        "tổng công ty",
        "đơn vị",
        ""
    ]
    
    return random.choice(listCompanyDesc)

##(kết quả là | đã)
def genResultDesc():
    listResultDesc = [
        "có kết quả là",
        "đã",
        "được đánh gía"
    ]
    
    return random.choice(listResultDesc)

############################################
def genPrefixDesc():
    listPrefixDesc = [
        f"trong {genMonthYear()}, chỉ tiêu <tên chỉ tiêu> của {genCompanyDesc()} <tổng công ty> {genResultDesc()} <đạt/không đạt>",
        f"chỉ tiêu <tên chỉ tiêu> của {genCompanyDesc()} <tên tổng công ty> trong {genMonthYear()} {genResultDesc()} <đạt/không đạt>",
        f"{genCompanyDesc()} <tên tổng công ty> có chỉ tiêu <tên chỉ tiêu> trong {genMonthYear()} {genResultDesc()} <đạt/không đạt>",
        f"{genCompanyDesc()} <tên tổng công ty> trong {genMonthYear()} có chỉ tiêu <tên chỉ tiêu> {genResultDesc()} <đạt/không đạt>"   
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

##(tháng|hiện đạt được|)
def genMonthKPIDesc():
    listMonthKPIDesc = [
        "tháng",
        "hiện có được",
        ""
    ]
    
    return random.choice(listMonthKPIDesc)

##(,(tăng|giảm)<Độ tăng giảm so với KPIs mục tiêu>,(gấp|chỉ bằng)<Tỉ lệ so với KPIs mục tiêu>)
def genDetailKPIMonth(sign=1,res=1,index=None):
    listDetailKPIMonth = [
        f"{genDiffDesc(sign)} <Độ tăng giảm so với KPIs mục tiêu><đơn vị>, {genRatioDesc(res)} <Tỉ lệ so với KPIs mục tiêu> lần",
        ""
    ]
    
    if index is None:
        return random.choice(listDetailKPIMonth)
    
    assert(index < len(listDetailKPIMonth))
    return listDetailKPIMonth[index]

##(đề ra là <mục tiêu KPI><đơn vị>)
def genDetailTarget():
    listDetailTarget = [
        "đề ra là <mục tiêu KPI><đơn vị>",
        ""
    ]
    return random.choice(listDetailTarget)

##(trong khi mục tiêu| so với mục tiêu KPI)
def genDescribeTarget():
    listDescribeTarget = [
        "trong khi mục tiêu",
        "so với mục tiêu KPI"
    ]
    
    return random.choice(listDescribeTarget)

############################################
def genOneKPI(sign=1,ratio=1,index=None):
    listOneKPI = [
        "có kết quả là <hiện trạng KPI><đơn vị>", #View ngắn gọn
        f"với hiện trạng có kết quả là <hiện trạng KPI><đơn vị>, {genDiffDesc(sign)} <Độ tăng giảm so với KPIs mục tiêu><đơn vị> so với mục tiêu KPI là <mục tiêu KPI><đơn vị>", #View bao quát - bằng delta
        f"chỉ tiêu hiện đã {genRatioDesc(ratio)} <Tỉ lệ so với KPIs mục tiêu> lần so với mục tiêu KPI ban đầu {genDetailTarget()}", #View bao quát - bằng tỉ lệ
        f"khi KPI {genMonthKPIDesc()} là <hiện trạng KPI><đơn vị> {genDescribeTarget()} đề ra là <mục tiêu KPI><đơn vị> {genDetailKPIMonth()}" #View chi tiết
    ]
    
    if index is None:
        return random.choice(listOneKPI)
    
    assert(index < len(listOneKPI))
    return listOneKPI[index]
#==========genOneKPI==========

#==========compareKPIMonthBefore==========
##(1 góc nhìn khác|bên cạnh đó|tuy nhiên)
def genDescAdv():
    listDescAdv = [
        "1 góc nhìn khác",
        "bên cạnh đó",
        "tuy nhiên",
        ""
    ]
    
    return random.choice(listDescAdv)

##(so với tháng trước|trong khi <tháng - 1> /<năm>)
def genMonthBeforeDesc():
    listMonthBeforeDesc = [
        "tháng trước",
        "T<tháng-1>/<năm>",
        "vào tháng <tháng-1> năm <năm>"
    ]
    
    return random.choice(listMonthBeforeDesc)
    
##(tăng|giảm)<Độ tăng giảm so với KPI tháng trước>|(gấp|chỉ bằng)<Tỉ lệ so với KPI tháng trước>lần)
def genDetailKPIMonthBefore(sign=1,ratio=1):
    listDetailKPIMonthBefore = [
        f"{genDiffDesc(sign)} <Độ tăng giảm so với KPI tháng trước><đơn vị>",
        f"{genRatioDesc(ratio)} <Tỉ lệ so với KPI tháng trước> lần",
    ]
    
    return random.choice(listDetailKPIMonthBefore)

############################################
def genCompareKPIMonthBefore(sign=1,ratio=1,index=None):
    listCompareKPIMonthBefore = [
        f"đối với KPI tháng trước là <KPI tháng trước><đơn vị>", #View ngắn gọn
        f"{genDetailKPIMonthBefore(sign,ratio)} so với KPI là {genMonthBeforeDesc()}", #View bao quát hơn
        f"{genDescAdv()} trong khi {genMonthBeforeDesc()} đạt <KPI tháng trước><đơn vị>, {genDetailKPIMonth(sign,ratio)}", #View thể hiện chi tiết
    ]
    
    if index is None:
        return random.choice(listCompareKPIMonthBefore)
    
    assert(index < len(listCompareKPIMonthBefore))
    return listCompareKPIMonthBefore[index]
#==========compareKPIMonthBefore==========

#==========compareKPIMYearBefore==========
##(Ngoài ra|Trong khi đó|)
def genDescAdvYear():
    listDescAdvYear = [
        "ngoài ra",
        "trong khi đó",
        ""
    ]
    
    return random.choice(listDescAdvYear)

##(so với cùng kỳ năm ngoái | với <tháng>/<năm -1> | tháng <tháng> năm <năm -1>)
def genYearBeforeDesc():
    listYearBeforeDesc = [
        "so với cùng kỳ năm ngoái",
        "với <tháng>/<năm-1>",
        "tháng <tháng> năm <năm-1>",
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
        f"{genDetailKPIYearBefore(sign,ratio)} so với KPI là {genYearBeforeDesc()}", #View bao quát
        f"{genDescAdvYear()} {genYearBeforeDesc()} chỉ tiêu có được là <KPI cùng kỳ năm trước><đơn vị> {genDetailKPIYearBefore(sign,ratio)}", #View thể hiện chi tiết
    ]
    
    if index is None:
        return random.choice(listCompareKPIMYearBefore)
    
    assert(index < len(listCompareKPIMYearBefore))
    return listCompareKPIMYearBefore[index]
#==========compareKPIMYearBefore==========

#==========genFullMonthView==========
############################################
def genFullView(sign=[1,1,1],ratio=[1,1,1],indexMonthNow=None,indexMonthBefore=None,indexYearBefore=None,index=None):
    prefix = genOneKPI(sign=sign[0],ratio=ratio[0],index=indexMonthNow)
    month = genCompareKPIMonthBefore(sign=sign[1],ratio=ratio[1],index=indexMonthBefore)
    year = genCompareKPIMYearBefore(sign=sign[2],ratio=ratio[2],index=indexYearBefore)
    listFullMonthView = [
        f"{prefix}", #chỉ tháng hiện tại
        f"{prefix}. {month}", #so sánh thêm tháng trước đó
        f"{prefix}. {year}", #so sánh cùng kỳ quý
        f"{prefix}. {month} .{year}", #so sánh cả tháng trước và cùng kỳ quý
    ]
    
    if index is None:
        return random.choice(listFullMonthView).replace("  "," ")
    
    assert(index < len(listFullMonthView))
    return listFullMonthView[index].replace("  "," ")
#==========genFullMonthView==========

if __name__ == "__main__":
    print(genPrefixAdv() + ' ' + genPrefixDesc() + ' ' + genFullView())