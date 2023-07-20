import random
import a_monthView

#===========genGroupMonthOverall===========
##(bao gồm <tổng số chỉ tiêu con> chỉ tiêu con|có số chỉ tiêu con là <tổng số chỉ tiêu con>)
def genTimeMonth():
    listTimeMonth = [
        "Trong <tháng> năm <năm>,",
        "Với T<tháng>/<năm>,",
    ]
    
    return random.choice(listTimeMonth)

def genGroupDesc():
    listGroupDesc = [
        "bao gồm <tổng số chỉ tiêu con> chỉ tiêu con",
        "có số chỉ tiêu con là <tổng số chỉ tiêu con>"
    ]
    
    return random.choice(listGroupDesc)

##(với đơn vị <đơn vị> và <điều kiện>|)
def genUnitDesc():
    listUnitDesc = [
        "với đơn vị <đơn vị> và <điều kiện>",
        ""
    ]
    
    return random.choice(listUnitDesc)

##zip(list(<tên chỉ tiêu con>) có kết quả là list(<kết quả đạt được tương ứng>))
def genListedOneKPI(groupKPI = ["A","B","C"], groupResult = ["Đạt", "Không Đạt", "Không Đạt"]):
    assert(len(groupKPI) == len(groupResult))
    
    sente = ""
    for kpi,res in zip(groupKPI,groupResult):
        sente += f"\n+ Chỉ tiêu {kpi} có kết quả là: {res}"
    return sente

################################################
def genGroupMonthOverall(groupKPI = ["A","B","C"], groupResult = ["Đạt", "Không Đạt", "Không Đạt"],index = None):
    listGroupMonthOverall = [
        f"{genTimeMonth()} cụm chỉ tiêu <tên cụm chỉ tiêu> {genUnitDesc()} có số chỉ tiêu con là <tổng số chỉ tiêu con>, trong đó có số chỉ tiêu không đạt là <Số chỉ tiêu không đạt> chỉ tiêu, số chỉ tiêu đạt là <Số chỉ tiêu đạt> chỉ tiêu.", #View bao quát
        f"{genTimeMonth()} cụm chỉ tiêu <tên cụm chỉ tiêu> {genUnitDesc()} {genGroupDesc()}, tên và kết quả tương ứng lần lượt là: {genListedOneKPI(groupKPI,groupResult)}"  #View liệt kê
    ]
    if index is None:
        return random.choice(listGroupMonthOverall)
    
    assert(index < len(listGroupMonthOverall))
    return listGroupMonthOverall[index]

#===========genGroupMonthOverall===========

#===========genGroupMonthDetail===========
##(Đi sâu hơn ta ta có được | Từng chỉ tiêu riêng lẻ ta có nhận xét như sau | Bao gồm)
def genDescListedOverall():
    listDescListedOverall = [
        "đi sâu hơn ta ta có được:",
        "từng chỉ tiêu riêng lẻ ta có nhận xét như sau:",
        "bao gồm:"
    ]
    
    return random.choice(listDescListedOverall)

def genListedOneKPIDetail(lenChildKPI,index_detail=None):
    
    sente = ""
    indexMonthNow = random.choice([*range(4)])
    indexMonthBefore = random.choice([*range(3)])
    indexYearBefore = random.choice([*range(2)])
    for _ in range(lenChildKPI):
        sente += f"""\n+ {a_monthView.genFullMonthView(indexMonthNow=indexMonthNow,
                                                    indexMonthBefore=indexMonthBefore,
                                                    indexYearBefore=indexYearBefore,
                                                    index=index_detail)}"""
    return sente

################################################
def genGroupMonthDetail(lenChildKPI=3,index = None):
    prefix = f"{genGroupMonthOverall(index = 0)} {genDescListedOverall()}"
    desc = [
        f"{prefix} {genDescListedOverall()}", #View liệt kê tổng thể,
        f"{prefix} Những KPI đạt là:", #View chỉ liệt kê những KPI đạt
        f"{prefix} Những KPI {random.choice(['không','chưa'])} đạt là:", #View chỉ liệt kê những KPI không đạt
    ]
    
    index_detail = random.choice([*range(4)])
    
    if index is None:
        return random.choice(desc) + genListedOneKPIDetail(lenChildKPI,index_detail)
    
    assert(index < len(desc))
    return desc[index] + genListedOneKPIDetail(lenChildKPI,index_detail)

#===========genGroupMonthDetail===========

#===========genChildInferenceMom===========
## (hiện trạng đạt được <hiện trạng KPI><đơn vị>|)
def genNowHave():
    listNowHave = [
        "hiện trạng đạt được <hiện trạng KPI><đơn vị>"
        "|"
    ]
    
    return random.choice(listNowHave)
  
## (nhóm chỉ tiêu <tên cụm chỉ tiêu>|cụm chỉ tiêu <tên cụm chỉ tiêu>|chỉ tiêu mẹ <tên cụm chỉ tiêu>)
def genParentDesc():
    listParentDesc = [
        "nhóm chỉ tiêu <tên cụm chỉ tiêu>",
        "cụm chỉ tiêu <tên cụm chỉ tiêu>",
        "chỉ tiêu mẹ <tên cụm chỉ tiêu>"
    ] 
    
    return random.choice(listParentDesc)

##############################################
def genChildInferenceMom(groupKPI = ["A","B","C"], groupResult = ["Đạt", "Không Đạt", "Không Đạt"], index=None):
    prefix = f"Chỉ tiêu <tên chỉ tiêu con> {genNowHave()} thuộc về {genParentDesc()} của tổng công ty <tên tổng công ty>."
    listChildInferenceMom = [
        f"{prefix} Ngoài ra nhóm chỉ tiêu này còn những chỉ tiêu con khác như: {genListedOneKPI(groupKPI,groupResult)}", #View từ con -> mẹ -> những con khác
        f"{prefix} Trong cùng năm, chỉ tiêu này có số KPI không đạt là len([D]), số KPI đạt là len([C]) và dự đoán tháng tiếp theo có thể <đạt/không đạt>." #View từ con -> mẹ -> liên hệ với con đó của quá khứ (cần xác định mức độ quá khứ - có thể dự đoán nho nhỏ)
    ]
    
    if index is None:
        return random.choice(listChildInferenceMom)
    
    assert(index < len(listChildInferenceMom))
    return listChildInferenceMom[index]

#===========genChildInferenceMom===========

if __name__ == "__main__":
    print(genChildInferenceMom())