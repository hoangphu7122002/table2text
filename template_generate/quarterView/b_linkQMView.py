import os, sys

def import_src():
    dir2 = os.path.abspath('')
    dir1 = os.path.dirname(dir2)
    if not dir1 in sys.path: sys.path.append(dir1)
    # print(f'Append {dir1} to sys.path')

import random
# import_src()
sys.path.append('/home/tungpth/table2text/template_generate')
import helperFunction

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
        "là <hiện trạng KPI tháng><đơn vị> so với mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị>",
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
        f"Tuy nhiên, hiện trạng năm đánh giá là không đạt khi KPI đạt được <hiện trạng KPI năm><đơn vị> nhưng mục tiêu đề ra là <mục tiêu KPI năm><đơn vị>. {genExplain()}", #năm không đạt
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

#==============genMonthViewKoDatOverall==============
def genMonthViewKoDatOverall():
    listMonthViewKoDatOverall = [
        "Cả tháng <tháng> và quý <quý> trong cùng <năm> của chỉ tiêu <tên chỉ tiêu> đều được đánh giá là không đạt."
    ]
    
    return random.choice(listMonthViewKoDatOverall)
#==============genMonthViewKoDatOverall==============


#==============genMonthViewKoDatDetail==============
##(Ngoài ra | ta cũng có được)
def genAdv1():
    listAdv1 = [
        "Ngoài ra",
        "Ta cũng có được",
        "Tôi thấy được"
    ]
    
    return random.choice(listAdv1)
##(khi KPI đạt được <hiện trạng KPI năm><đơn vị> nhưng mục tiêu đề ra là <mục tiêu KPI năm>|)
def genYearKoDatDetail():
    listYearKoDatExplain = [
        "khi KPI đạt được <hiện trạng KPI năm><đơn vị> nhưng mục tiêu đề ra là <mục tiêu KPI năm><đơn vị>",
        ""
    ]
    
    return random.choice(listYearKoDatExplain)

##góc nhìn khác
def genYearKoDatExplain(index=None):
    listYearKoDatExplain = [
        f"Tuy nhiên KPI năm lại đạt, trường hợp này chưa thấy xảy ra bao giờ", #năm đạt
        f"{genAdv1()} hiện trạng KPI của năm được đánh giá là không đạt {genYearKoDatDetail()}. {genRequireAdjustKoDat()}", #nếu năm không đạt
        ""
    ]
    
    if index is None:
        return random.choice(listYearKoDatExplain)
    
    assert(index < len(listYearKoDatExplain))
    return listYearKoDatExplain[index]

##Yêu cầu giải trình và điều chỉnh
def genRequireAdjustKoDat():
    listRequireAdjustKoDat = [
        "cần giải trình nguyên nhân dẫn đến kết quả không tốt này từ <tổng công ty>", #Yêu cầu giải trình
        "kết quả này xảy ra có thể do mục tiêu KPI đề ra quá cao, có thể điều chỉnh các con số này lại sao cho phù hợp hơn với tình cảnh hiện tại", #Yêu cầu điều chỉnh
        ""
    ]
    
    return random.choice(listRequireAdjustKoDat)

####################################################
def genMonthViewKoDatDetail(year = 1):
    index_detail = random.choice([0,1])
    listMonthViewDatDetail = [
        f"với chỉ tiêu <tên chỉ tiêu>, hiện trạng có được trong {genMonthDesc()} {genDetailQMDesc(index_detail)} được đánh giá là không đạt và kết quả này vẫn xảy ra trong {genQuarterDesc()} {genDetailQMDesc(index_detail)}, cho thấy {genYearKoDatExplain(index=year)}",
    ]
    
    return random.choice(listMonthViewDatDetail)
#==============genMonthViewKoDatDetail==============

#Tháng đạt, quý không đạt
#==============genTKoDatQDat================
##(nhưng mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị>|giảm <độ chênh lệch KPI> so với KPI của mục tiêu tháng|chỉ bằng <tỉ lệ> một phần của KPI mục tiêu tháng)
def genDecreaseKPIMonth(index=None):
    listDecreaseKPIMonth = [
        "nhưng mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị>",
        "giảm <độ chênh lệch tháng> so với KPI của mục tiêu tháng",
        "chỉ bằng <tỉ lệ tháng> lần của KPI mục tiêu tháng"
    ]
    
    if index is None:
        return random.choice(listDecreaseKPIMonth)
    assert(index < len(listDecreaseKPIMonth))
    return listDecreaseKPIMonth[index]

##(khi KPI hiện trạng đạt được <hiện trạng KPI tháng><đơn vị> (genDescreaseKPIMonth)|)
def genDescribeKPIMonth(index=None,index_detail=None):
    listDescribeKPIMonth = [
        f"khi KPI hiện trạng đạt được <hiện trạng KPI tháng><đơn vị> {genDecreaseKPIMonth(index_detail)}",
        ""
    ]
    if index is None:    
        return random.choice(listDescribeKPIMonth)
    assert(index < len(listDescribeKPIMonth))
    
    return listDescribeKPIMonth[index]

##("vượt qua mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị>"|"tăng <độ chênh lệch> so với KPI của mục tiêu tháng"|"gấp <tỉ lệ> lần của KPI mục tiêu tháng")
def genIncreaseKPIQuarter(index = None):
    listIncreaseKPIQuarter = [
        "vượt qua mục tiêu đề ra là <mục tiêu KPI quý><đơn vị>",
        "tăng <độ chênh lệch quý> so với KPI của mục tiêu quý",
        "gấp <tỉ lệ quý> lần của KPI mục tiêu quý"
    ]
    
    if index is None:
        return random.choice(listIncreaseKPIQuarter)
    assert(index < len(listIncreaseKPIQuarter))
    return listIncreaseKPIQuarter[index]

##(khi KPI của quý đạt được <hiện trạng KPI quý> đơn vị> {genIncreaseKPIQuarter()}|)
def genDescribeKPIQuarter(index=None,index_detail=None):
    listDescribeKPIQuarter = [
        f"khi KPI hiện trạng đạt được <hiện trạng KPI quý><đơn vị> {genIncreaseKPIQuarter(index_detail)}",
        ""
    ]
    if index is None:    
        return random.choice(listDescribeKPIQuarter)
    assert(index < len(listDescribeKPIQuarter))
    
    return listDescribeKPIQuarter[index]

####################################################
def genTKoDatQDat(year=None):
    index_detail = random.choice([*range(3)])
    index = random.choice([*range(2)])
    listTKoDatQDat = [
        f"tuy kết quả của tháng với chỉ tiêu <tên chỉ tiêu> được đánh giá là không đạt {genDescribeKPIMonth(index,index_detail)} nhưng hiện kết quả đánh giá của quý vẫn đạt {genDescribeKPIQuarter(index,index_detail)}. Điều này cho thấy, các hiện trạng KPI tháng trước đã kéo kết quả của quý hiện tại lên mức đạt. {genExplainYear1(year)}",
    ]
    
    return random.choice(listTKoDatQDat)
    
def genYearDetail1(index=None):
    listYearDat1 = [
        f"tuy nhiên kết quả đánh giá của KPI của năm lại đạt",
        f"do kết quả KPI của năm tính đến hiện tại là <hiện trạng KPI năm><đơn vị> so với mục tiêu KPI năm là <mục tiêu KPI năm><đơn vị>",    
        f"bên cạnh đó kết quả đánh giá của KPI của năm lại không đạt",
    ]
    
    if index is None:
        return random.choice(listYearDat1)
    assert(index < len(listYearDat1))
    
    return listYearDat1[index]

def genExplainYear1(index=None):
    listExplainYear1 = [
        f"{genYearDetail1(random.choice([0,1]))} điều này chứng tỏ kết quả không đạt của chỉ tiêu tháng này không ảnh hưởng nhiều đến kết quả KPI dự kiến của năm.", #Nếu năm đạt:
        f"{genYearDetail1(random.choice([2,1]))} cho ta thấy được các quý trước có kết quả không tốt đã ảnh hưởng tới cả kết quả của quý này. Cần xem lại các kết quả của quý trước.", #Nếu năm không đạt (nếu quý hiện tại != Q1)
        ""
    ]
    
    if index is None:
        return random.choice(listExplainYear1)
    assert(index < len(listExplainYear1))
    
    return listExplainYear1[index]

#==============genTKoDatQDat================

#==============genTDatQKoDat================
##(với mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị>|tăng <độ chênh lệch> so với KPI của mục tiêu tháng|gấp <tỉ lệ> lần của KPI mục tiêu tháng)
def genIncreaseKPIMonth(index=None):
    listIncreaseKPIMonth = [
        "với mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị>",
        "tăng <độ chênh lệch tháng> so với KPI của mục tiêu tháng",
        "gấp <tỉ lệ tháng> lần của KPI mục tiêu tháng"
    ]
    
    if index is None:
        return random.choice(listIncreaseKPIMonth)
    assert(index < len(listIncreaseKPIMonth))
    return listIncreaseKPIMonth[index]

##(khi KPI hiện trạng đạt được <hiện trạng KPI tháng><đơn vị> (genDescreaseKPIMonth)|)
def genDescribeKPIMonth_Inc(index=None,index_detail=None):
    listDescribeKPIMonth_Inc = [
        f"khi KPI hiện trạng đạt được <hiện trạng KPI tháng><đơn vị> {genIncreaseKPIMonth(index_detail)}",
        ""
    ]
    if index is None:    
        return random.choice(listDescribeKPIMonth_Inc)
    assert(index < len(listDescribeKPIMonth_Inc))
    
    return listDescribeKPIMonth_Inc[index]

##("trong khi đó mục tiêu đề ra là <mục tiêu KPI tháng><đơn vị>"|"giảm <độ chênh lệch> so với KPI của mục tiêu tháng"|"chỉ bằng <tỉ lệ> lần của KPI mục tiêu tháng")
def genDescreaseKPIQuarter(index = None):
    listDescreaseKPIQuarter = [
        "trong khi đó mục tiêu đề ra là <mục tiêu KPI quý><đơn vị>",
        "giảm <độ chênh lệch quý> so với KPI của mục tiêu quý",
        "chỉ bằng <tỉ lệ quý> lần của KPI mục tiêu quý"
    ]
    
    if index is None:
        return random.choice(listDescreaseKPIQuarter)
    assert(index < len(listDescreaseKPIQuarter))
    return listDescreaseKPIQuarter[index]

##(khi KPI của quý đạt được <hiện trạng KPI quý> đơn vị> {genIncreaseKPIQuarter()}|)
def genDescribeKPIQuarter_Des(index=None,index_detail=None):
    listDescribeKPIQuarter_Des = [
        f"khi KPI hiện trạng đạt được <hiện trạng KPI quý><đơn vị> {genDescreaseKPIQuarter(index_detail)}",
        ""
    ]
    if index is None:    
        return random.choice(listDescribeKPIQuarter_Des)
    assert(index < len(listDescribeKPIQuarter_Des))
    
    return listDescribeKPIQuarter_Des[index]

################################################################
def genTDatQKoDat(year = None):
    index_detail = random.choice([*range(3)])
    index = random.choice([*range(2)])
    listTDatQKoDat = [
        f"ta thấy kết quả của tháng với chỉ tiêu <tên chỉ tiêu> được đánh giá là đạt {genDescribeKPIMonth_Inc(index,index_detail)} nhưng hiện kết quả đánh giá của quý vẫn chưa đạt {genDescribeKPIQuarter_Des(index,index_detail)}. \
        Điều này cho thấy, các hiện trạng KPI tháng trước đã kéo kết quả của quý hiện tại xuống mức không đạt. {genExplainYear1(year)}",
    ]
    
    return random.choice(listTDatQKoDat)
#==============genTDatQKoDat================

if __name__ == "__main__":
    print(helperFunction.postProcessOutput(genTDatQKoDat()))