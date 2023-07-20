import random

#==============genMonthViewDatOverview==============
##(cả tháng <tháng> và quý <quý> của năm <năm>|trong T<tháng>/<năm> và Q<quý>/<năm>)
def genQuarterMonthDesc():
    listQuarterMonthDesc = [
        "cả tháng <tháng> và quý <quý> của năm <năm>",
        "trong T<tháng>/<năm> và Q<quý>/<năm>"
    ]
    
    return random.choice(listQuarterMonthDesc)

##View tháng, quý kết quả đều đạt - 2 (tổng quan):
def genMonthViewDatOverview():
    prefix = genQuarterMonthDesc()
    listMonthViewDat = [
        f"{prefix}, chỉ tiêu <tên chỉ tiêu> đều được đánh giá là đạt."
        f"Chỉ tiêu <tên chỉ tiêu> đều được đánh giá là đạt {prefix}"
    ]
    
    return random.choice(listMonthViewDat)
#==============genMonthViewDatOverview==============

#==============genMonthViewDatDetail==============
##(T<tháng>/<năm>| tháng <tháng> năm <năm>)
def genMonthDesc():
    listMonthViewDatDetail = [
        "T<tháng>/<năm>",
        "tháng <tháng> năm <năm>"
    ]

    return random.choice(listMonthViewDatDetail)

##(quý <quý> cùng kỳ | quý <quý> năm <năm> | Q<quý>/<năm>)
def genQuarterDesc():
    listQuarterDescB = [
        "quý <quý> cùng kỳ",
        "quý <quý> năm <năm>",
        "Q<quý>/<năm>"
    ]
    
    return random.choice(listQuarterDescB)

##(là <hiện trạng KPI tháng><đơn vị> so với mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị>|)
def genDetailQMDesc(index = None):
    listDetailQMDesc = [
        "là <hiện trạng KPI tháng><đơn vị> so với mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị",
        ""
    ]
    
    if index is None:
        return random.choice(listDetailQMDesc)
    
    assert(index < len(listDetailQMDesc))
    return listDetailQMDesc[index]

##(đã đáp ứng đầy đủ với kế hoạch đặt ra của chỉ tiêu này | chỉ tiêu đề ra tạm đáp ứng thành công)
def genDatDesc():
    listDatDesc = [
        "đã đáp ứng đầy đủ với kế hoạch đặt ra của chỉ tiêu này",
        "chỉ tiêu đề ra tạm đáp ứng thành công"
    ]
    
    return random.choice(listDatDesc)

##generate yearExplainInMVDat
def genExplain(index=None):
    listExplain = [
        "Thông tin này cho thấy cần yêu cầu tổng công ty <tên tổng công ty> giải trình các mục tiêu đề ra ban đầu.", #Yêu cầu giải trình
        "Điều này cho thấy cần điều chỉnh lại các mục tiêu KPI đề ra của cả tháng và quý hoặc là điều chỉnh KPI của năm.", #Yêu cầu điều chỉnh
        ""
    ]
    
    if index is None:
        return random.choice(listExplain)
    assert(index < len(listExplain))
    return listExplain[index]

def genYearExplain(index = None):
    listYearExplain = [
        f"Bên cạnh đó chỉ tiêu hiện giờ của năm đề ra vẫn đang giữ vững kết quả đánh giá là đạt", #năm đạt
        f"Tuy nhiên, hiện trạng năm đánh giá là không đạt khi KPI đạt được <hiện trạng KPI năm><đơn vị> nhưng mục tiêu đề ra là <mục tiêu KPI năm>. {genExplain()}", #năm không đạt
        ""
    ]

    if index is None:
        return random.choice(listYearExplain)
    assert(index < len(listYearExplain))
    
    return listYearExplain[index]

####################################################
def genMonthViewDatDetail(year = 0):
    index_detail = random.choice([0,1])
    listMonthViewDatDetail = [
        f"với chỉ tiêu <tên chỉ tiêu>, hiện trạng có được trong {genMonthDesc()} {genDetailQMDesc(index_detail)} được đánh giá là đạt và kết quả này vẫn duy trì trong {genQuarterDesc()} {genDetailQMDesc(index_detail)}, cho thấy {genDatDesc()}. {genYearExplain(year)}",
    ]
    
    return random.choice(listMonthViewDatDetail)
        
#==============genMonthViewDatDetail==============

if __name__ == "__main__":
    print(genMonthViewDatDetail())