import random

#==============ViewStatSeason==============
##Listed
def genListedStat(lenStat=3):
    prefix = "Cụ thể ta có thể nhìn thấy:"
    for _ in range(lenStat):
        prefix += "\nT<tháng>/<năm> đạt được KPI là: <hiện trạng KPI tháng><đơn vị> được đánh giá là <đạt/không đạt>"
    return prefix

##################################
def genViewStatSeason():
    listViewStatSeason = [
        f"""hiện tại tình hình của chỉ tiêu <tên chỉ tiêu> của tổng công ty <tên tổng công ty> của tháng <tháng> trong len([D]) \
            năm gần nhất được đánh giá đạt được bao gồm len([D] ⇔ đạt) lần và không đạt là len([D] ⇔ không đạt) lần. {random.choice([genListedStat(),""])}""",
        f"""Vào thời điểm hiện tại, chỉ số <tên chỉ tiêu> của tổng công ty <tên tổng công ty> trong tháng <tháng> của năm gần \
            nhất đã được đánh giá và có len([D] ⇔ đạt) lần đạt và len([D] ⇔ không đạt) lần không đạt. {random.choice([genListedStat(),""])}"""
    ]
    
    return random.choice(listViewStatSeason)
#==============ViewStatSeason==============

#==============ViewStatMonthBefore==============
##################################
def genViewStatMonthBefore():
    listViewStatMonthBefore = [
        f"""hiện tại tình hình của chỉ tiêu <tên chỉ tiêu> của tổng công ty <tên tổng công ty> trong {random.choice(["năm nay","<năm>"])} đạt được đánh giá là đạt bao gồm \
            len([A] ⇔ đạt) lần và không đạt là len([A] ⇔ không đạt). {random.choice([genListedStat(),""])}""",
    ]
    
    return random.choice(listViewStatMonthBefore)
#==============ViewStatMonthBefore==============

#==============ViewPredictMonthBefore==============
##((<tháng>/<năm>)|(tháng <tháng> năm <năm>))
def genMonthDesc():
    listMonthDesc = [
        "T<tháng>/<năm>",
        "tháng <tháng> năm <năm>"   
    ]
    
    return random.choice(listMonthDesc)

##(tiếp theo| kế tiếp|<tháng + 1>)
def genAdv2():
    listAdv2 = [
        "tiếp theo",
        "kế tiếp",
        "<tháng + 1>"
    ]
    
    return random.choice(listAdv2)

##(đề ra là <mục tiêu KPI quý><đơn vị>|)
def genDetail2(index = None):
    listDetail2 = [
        "đề ra là <mục tiêu KPI quý><đơn vị>",
        ""   
    ]
    
    if index is None:
        return random.choice(listDetail2)
    assert(index < len(listDetail2))
    return listDetail2[index]

##################################

def genViewPredictMonthBefore():
    index_detail = random.choice([0,1])
    listViewPredictMonthBefore = [
        f"""dựa vào các tháng gần nhất trong cùng 1 năm <năm> tính đến hiện tại {genMonthDesc()}, chỉ tiêu <tên chỉ tiêu> của tổng công ty <tên tổng công ty> được dự báo đạt được mốc KPI là <kết quả dự báo><đơn vị> trong tháng {genAdv2()}. Kết quả này dự đoán sẽ được đánh giá <đạt/không đạt> so với mục tiêu KPI quý <quý> {genDetail2(index_detail)} và so với mục tiêu KPI của năm {genDetail2(index_detail)} được đánh giá là <đạt/không đạt>.""",
    ]
    
    return random.choice(listViewPredictMonthBefore)
#==============ViewPredictMonthBefore==============

#==============ViewPredictYearSeasonBefore==============
##################################
def genViewPredictMonthBefore():
    index_detail = random.choice([0,1])
    listViewPredictMonthBefore = [
        f"""dựa vào trong <tháng> của len([D]) năm gần nhất tính đến năm <năm> {genMonthDesc()}, chỉ tiêu <tên chỉ tiêu> của tổng công ty <tên tổng công ty> được dự báo đạt được mốc KPI là <kết quả dự báo><đơn vị> trong tháng {genAdv2()}. Kết quả này dự đoán sẽ được đánh giá <đạt/không đạt> so với mục tiêu KPI quý <quý> {genDetail2(index_detail)} và so với mục tiêu KPI của năm {genDetail2(index_detail)} được đánh giá là <đạt/không đạt>.""",
    ]
    
    return random.choice(listViewPredictMonthBefore)
#==============ViewPredictYearSeasonBefore==============

#==============ViewExplainResult==============
def genViewExplain1(index = None):
    listViewExplain1 = [
        f"""Do kết quả đánh là đạt, cho thấy tháng này chỉ tiêu <chỉ tiêu> đã {random.choice(["đáp ứng đúng đầy đủ nhu cầu","hoàn thành tốt"])} và sấp xỉ so với KPI dự báo.""",#Nếu kết quả đánh giá là đạt và dự báo cũng gần KPI tháng
        f"Kết quả của KPI hiện tại được đánh giá là đạt, tuy khác xa kết quả dự báo từ các tháng trước điều này cho thấy có thể KPI các tháng trước chưa hoàn thành tốt hoặc chưa đáp ứng đầy đủ.",#Nếu kết quả đánh giá là đạt và dự báo xa KPI tháng
        f"Kết quả của tháng này hiện được đánh giá không đạt. Điều này cũng được dự đoán từ trước khi rất gần KPI dự đoán, cho thấy ta có thể cần điều chỉnh lại kì vọng KPI mục tiêu",#Nếu kết quả đánh giá là không đạt và dự báo gần KPI tháng
        f"Có một bất thường xảy ra khi KPI hiện tại không đạt và khác xa dự đoán kì vọng từ các tháng trước, vì thế <chỉ tiêu> này cần được tổng công ty <tên tổng công ty> giải trình rõ ràng.",#Nếu kết quả đánh giá là không đạt và dự báo xa KPI tháng
    ]
    
    if index is None:
        return random.choice(listViewExplain1)
    assert(index < len(listViewExplain1))
    
    return listViewExplain1[index]

##################################
def genViewExplainResult(index_detail = None):
    if index_detail is None:
        index_detail = random.choice([*range(4)])
    index_detail = min(index_detail,3)
    listViewExlainResult = [
        f"""trong {genMonthDesc()}, chỉ tiêu <tên chỉ tiêu> đạt được hiện trạng KPI là <hiện trạng KPI tháng><đơn vị> và so với dự báo từ len([A]) tháng trước thì tháng này đạt được <kết quả dự báo><đơn vị>. {genViewExplain1(index_detail)}""",
    ]

    return random.choice(listViewExlainResult)
#==============ViewExplainResult==============

#==============ViewDetermineTrend==============
##(nhanh | chậm |)
def genLevelTrend(index = None):
    listLevelTrend = [
        "nhanh",
        "chậm",
        ""
    ]
    
    if index is None:
        return random.choice(listLevelTrend)
    
    assert(index < len(listLevelTrend))
    return listLevelTrend[index]

##(tăng | giảm | không sai khác quá nhiều)
def genDescTrend(index = None):
    listDescTrend = [
        "tăng",
        "giảm",
        "không sai khác quá nhiều"
    ]
    
    if index is None:
        return random.choice(listDescTrend)
    assert(index < len(listDescTrend))
    return listDescTrend[index]
##(có kết quả dự báo là <kết quả dự báo><đơn vị>|)
def genDetail2(index=None):
    listDetail2 = [
        "có kết quả dự báo là <kết quả dự báo><đơn vị>",
        ""
    ]
    if index is None:
        return random.choice(listDetail2)
    assert(index < len(listDetail2))
    return listDetail2[index]

################################################
def genViewDetermineTrend(index1=None,index2=None):
    listViewDetermineTrend = [
        f"dựa vào kết quả hiện có tính đến {genMonthDesc()} của chỉ tiêu <tên chỉ tiêu> {genDetail2()}, kết quả này cho ta thấy trend hiện {genDescTrend(index1)} {genLevelTrend(index2)}"
    ]
    return random.choice(listViewDetermineTrend)
#==============ViewDetermineTrend==============

if __name__ == '__main__':
    print(genViewDetermineTrend())