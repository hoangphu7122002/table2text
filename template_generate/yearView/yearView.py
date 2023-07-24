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
        "Dựa trên thông tin về dữ liệu báo cáo",
        "Dựa trên thông tin về dữ liệu báo cáo ta thấy được rằng",
        ""
    ]
    return random.choice(listAdv)
#==========genPreAdv==========


#==========genDesc==========
##(tháng <tháng> năm <năm> | <tháng>/<năm>)
def genYear():
    listMonthYear = [
       "trong <năm>",
       "ở <năm>",
       "tại <năm>"
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
        "được đánh gía",
        "có đánh giá",
    ]
    
    return random.choice(listResultDesc)

############################################
def genPrefixDesc():
    listPrefixDesc = [
        f"{genYear()}, chỉ tiêu <tên chỉ tiêu> của {genCompanyDesc()} <tổng công ty> {genResultDesc()} <đạt/không đạt>",
        f"chỉ tiêu <tên chỉ tiêu> của {genCompanyDesc()} <tên tổng công ty> {genYear()} {genResultDesc()} <đạt/không đạt>",
        f"{genCompanyDesc()} <tên tổng công ty> có chỉ tiêu <tên chỉ tiêu> {genYear()} {genResultDesc()} <đạt/không đạt>",
        f"{genCompanyDesc()} <tên tổng công ty> {genYear()} có chỉ tiêu <tên chỉ tiêu> {genResultDesc()} <đạt/không đạt>"   
    ]
    
    return random.choice(listPrefixDesc)
#==========genDesc==========|


#==========genOneKPI==========
##(tăng|giảm|chênh lệch)
def genDiffDesc(sign = 1):
    if sign == 1:
        return "tăng"
    elif sign == -1:
        return "giảm"
    
    listDiffDesc = [
        "chênh lệch",
        "sai khác",
        "biến động",
        "khác biệt"
    ]
    return random.choice(listDiffDesc)

#(gấp|chỉ bằng)
def genRatioDesc(res = 1):
    if res >= 1:
        return random.choice(["gấp", "đạt được"])
    return random.choice(["chỉ bằng", "chỉ đạt được"])

#(năm|hiện đạt được|năm hiện)
def genYearKPIDesc():
    listYearKPIDesc = ['năm', 'hiện đạt được', 'năm hiện']
    return random.choice(listYearKPIDesc)

##(,(tăng|giảm)<Độ tăng giảm so với KPIs mục tiêu>,(gấp|chỉ bằng)<Tỉ lệ so với KPIs mục tiêu>)
def genDetailKPIYear(sign=1,res=1,index=None):
    listDetailKPIYear = [
        f"{genDiffDesc(sign)} <Độ tăng giảm so với KPIs mục tiêu>, {genRatioDesc(res)} <Tỉ lệ so với KPIs mục tiêu> lần",
        ""
    ]
    
    if index is None:
        return random.choice(listDetailKPIYear)
    
    assert(index < len(listDetailKPIYear))
    return listDetailKPIYear[index]

##(đề ra là <mục tiêu KPI><đơn vị>)
def genDetailTarget():
    str_ = '<mục tiêu KPI><đơn vị>'
    verb_ = random.choice(['đề ra', 'xác định', 'quyết định', 'đặt ra'])
    listDetailTarget = [
        f" ban đầu {verb_} là {str_}",
        f" ban đầu là {str_}",
        f" được {verb_} ban đầu là {str_}",
        f" {verb_} ban đầu là {str_}",
        f" ban đầu được {verb_} là {str_}",
        ""
    ]
    return random.choice(listDetailTarget)

##(trong khi mục tiêu| so với mục tiêu KPI)
def genDescribeTarget():
    listDescribeTarget = [
        "trong khi mục tiêu",
        "so với mục tiêu KPI",
        "trong khi đó so sánh với mục tiêu",
        "đối chiếu với KPI được"
    ]
    
    return random.choice(listDescribeTarget)

def genOneKPI(sign=1,ratio=1,index=None):
    listOneKPI = [
        "có KPI đạt được là <hiện trạng KPI><đơn vị>", #View ngắn gọn
        f"với con số đạt được là <hiện trạng KPI><đơn vị>, {genDiffDesc(sign)} <Độ tăng giảm so với KPIs mục tiêu> khi so sánh với mục tiêu KPI đề ra là <mục tiêu KPI><đơn vị>", #View bao quát - bằng delta
        f"với hiện trạng đạt được là <hiện trạng KPI><đơn vị>, {genDiffDesc(sign)} <Độ tăng giảm so với KPIs mục tiêu> so với mục tiêu KPI là <mục tiêu KPI><đơn vị>", #View bao quát - bằng delta
        f"chỉ tiêu hiện đã {genRatioDesc(ratio)} <Tỉ lệ so với KPIs mục tiêu> lần so với mục tiêu KPI{genDetailTarget()}", #View bao quát - bằng tỉ lệ
        f"chỉ tiêu hiện đã {genRatioDesc(ratio)} <Tỉ lệ so với KPIs mục tiêu> lần khi được đem so sánh với mục tiêu KPI{genDetailTarget()}", #View bao quát - bằng tỉ lệ
        f"khi KPI {genYearKPIDesc()} là <hiện trạng KPI><đơn vị> {genDescribeTarget()} đề ra là <mục tiêu KPI><đơn vị>{genDetailKPIYear()}" #View chi tiết
    ]
    
    if index is None:
        return random.choice(listOneKPI)
    
    assert(index < len(listOneKPI))
    return listOneKPI[index]
#==========genOneKPI==========

##(1 góc nhìn khác|bên cạnh đó|tuy nhiên)
def genDescAdv():
    listDescAdv = [
        "Một góc nhìn khác",
        "Bên cạnh đó",
        "Tuy nhiên",
        "Ngoài ra bên cạnh đó",
        "Ngoài ra theo một góc nhìn khác",
        "Đối với một góc nhìn khác",
        ""
    ]
    
    return random.choice(listDescAdv)

##(so với năm trước|trong khi <năm - 1>)
def genLastYearDesc():
    listMonthBeforeDesc = [
        "năm trước",
        "năm ngoái",
        "vào năm <năm>",
        "vào năm trước - năm <năm - 1>",
        "vào năm ngoái - năm <năm - 1>",
        "tại năm <năm - 1>"
    ]
    return random.choice(listMonthBeforeDesc)

##(tăng|giảm)<Độ tăng giảm so với KPI năm trước>|(gấp|chỉ bằng)<Tỉ lệ so với KPI năm trước>lần)
def genDetailKPILastYear(sign=1,ratio=1):
    listDetailKPIYearBefore = [
        f"{genDiffDesc(sign)} <Độ tăng giảm so với KPI năm trước>",
        f"{genRatioDesc(ratio)} <Tỉ lệ so với KPI năm trước> lần",
    ]
    
    return random.choice(listDetailKPIYearBefore)

############################################
def genCompareKPILastYear(sign=1,ratio=1,index=None):
    gen_desc_adv = genDescAdv()
    listCompareKPIMonthBefore = [
        f". Đối với KPI năm trước đạt được <KPI năm trước><đơn vị>", #View ngắn gọn
        f", {genDetailKPILastYear(sign,ratio)} so với KPI đạt được {genLastYearDesc()}", #View bao quát hơn
        f". {gen_desc_adv}{'trong' if gen_desc_adv == '' else ' trong'} khi {genLastYearDesc()} đạt <KPI tháng trước><đơn vị>, {genDetailKPILastYear(sign,ratio)}", #View thể hiện chi tiết
    ]
    
    if index is None:
        return random.choice(listCompareKPIMonthBefore)
    
    assert(index < len(listCompareKPIMonthBefore))
    return listCompareKPIMonthBefore[index]
#==========compareKPILastYear==========

#==========genFullYearView==========
############################################
def genFullYearView(sign=[1,1],ratio=[1,1],indexYear=None, indexLastYear=None,index=None):
    prefix = genOneKPI(sign=sign[0],ratio=ratio[0],index=indexYear)
    year = genCompareKPILastYear(sign=sign[1],ratio=ratio[1],index=indexLastYear)
    listFullYearView = [
        f"{prefix}", #chỉ tháng hiện tại
        f"{prefix}{year}", #so sánh cùng với năm trước
    ]
    
    if index is None:
        return random.choice(listFullYearView).replace("  "," ")
    
    assert(index < len(listFullYearView))
    return listFullYearView[index].replace("  "," ")
#==========genFullYearView==========

if __name__ == '__main__':
    final_res = (genPrefixAdv().capitalize() + ' ' + genPrefixDesc() + ' ' + genFullYearView()).strip()
    final_res = (' '.join(final_res.split()))
    final_res
