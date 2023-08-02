import random

#=================common part==================
def genDesPerson():
    listDesPerson = [
        "tôi",
        "tui",
        "t",
        ""
    ]
    
    return random.choice(listDesPerson)

def genDesExplain(person = "tôi"):
    listDesExplain = [
        "giải thích về",
        f"cho {person} biết thêm",
        "làm rõ thêm về",
        "tường tận thêm về",
        "trình bày thêm về"
    ]
    
    return random.choice(listDesExplain)

def genPrefixQuestion():
    person = genDesPerson()
    
    listPrefixQuestion = [
        f"cho {person} hỏi",
        f"{person} muốn biết",
        f"xin hỏi",
        f"cho {person} biết",
        f"có thể cho {person} biết",
        f"{person} có một câu hỏi là",
        f"{person} có một vấn đề cần được giải đáp",
        f"bạn hãy giúp {person} giải đáp thắc mắc sau",
        f"bạn có thể {genDesExplain(person)}",
        f"hãy giúp {person} hiểu hơn về"
        "",
    ]
    
    return random.choice(listPrefixQuestion)

def genDesViewMonth(index=None):
    listDesViewMonth = [
        "tháng <tháng>, năm <năm>",
        "t<tháng>/<năm>",
        "tháng <tháng>, <năm>"
    ]
    
    if index is None:
        return random.choice(listDesViewMonth)
    
    assert(index < len(listDesViewMonth))
    return listDesViewMonth[index]

def genDesViewQuarter():
    listDesViewQuarter = [
        "quý <quý>, năm <năm>",
        "q<quý>/<năm>",
        "quý <quý>, <năm>"
    ]
    
    index = random.choice([*range(3)])
    
    return listDesViewQuarter[index],index

def genDesViewYear():
    listYear = [
        "năm <năm>",
        "n<năm>",
        "năm <năm>"
    ]
    
    index = random.choice([*range(3)])
    
    return listYear[index],index

def genDesc():
    listDesc = [
        "tính đến",
        "cho đến",
        "đến hết",
        "bắt đầu đến hết"
    ]
    
    return random.choice(listDesc)

def genDesc2():
    listDesc2 = [
        "từ đầu",
        "trong khoảng thời gian từ",
        "trong giai đoạn",
        "từ giữa",
        "trong"
    ]
    
    return random.choice(listDesc2)

def genDesView(view):
    if view is None:
        view = random.choice(["month","quarter","year"])
        
    if view == "month": return genDesViewMonth()
    if view == "quarter": des,index = genDesViewQuarter()
    else: des,index = genDesViewYear()
    
    des2 = genDesViewMonth(index)
    return f"{genDesc2()} {des} {genDesc()} {des2}"

def genComp():
    listComp = [
        f"của tổng công ty <tổng công ty>",
        f"của <tổng công ty>",
        f"do <tổng công ty> quản lý",
        f"được quản lý bởi tổng công ty <tổng công ty>"
        f"được <tổng công ty> điều hành",
        f"liên quan <tổng công ty>",
        f"",
        f""
    ]
    
    return random.choice(listComp)
#=================common part==================

#=================oneKPI===================
def genDesAdv():
    listDesAdv = [
        "tổng quan",
        "chi tiết",
        "sâu hơn",
        "khái quát",
        "tổng thể",
        "cụ thể",
        "tường minh",
        "rõ ràng",
    ]
    
    return random.choice(listDesAdv)

def genPosfix():
    listPostfix = [
        "được hay không",
        "có được không",
        "nhé",
        "được không",
        "đi bạn",
        "ha",
        ""
    ]
    
    return random.choice(listPostfix)

def genDesAdv2():
    listDesAdv2 = [
        "khả quan",
        "tốt",
        "đạt",
        "không đạt",
        "như mong đợi",
        "như mục tiêu",
        "hiệu quả chưa",
        "hiệu quả như mong đợi chưa"
    ]
    
    return random.choice(listDesAdv2)

def genDesOneKPI():
    listDesOneKPI = [
        f"{genDesAdv()} về chỉ tiêu <tên chỉ tiêu> {genComp()} {genPosfix()}",
        f"{genComp()}, {genDesAdv()} về chỉ tiêu <tên chỉ tiêu> {genPosfix()}",
        f"về hiện trạng chỉ 1 chỉ tiêu <tên chỉ tiêu>",
        f"chỉ tiêu <tên chỉ tiêu> này {genComp()} như thế nào rồi",
        f"liệu chỉ tiêu <tên chỉ tiêu> này có kết quả {genDesAdv2()}",
        f"kết quả của chỉ tiêu <tên chỉ tiêu> ra sao",
        f"chỉ tiêu <tên chỉ tiêu> {genComp()} đã đem lại {genDesAdv2()}",
        f"tình hình thực hiện chỉ tiêu <tên chỉ tiêu> như thế nào {genComp()}",
        f"chỉ tiêu <tên chỉ tiêu> có được kết quả {genDesAdv2()}",
    ]
    
    return random.choice(listDesOneKPI)

def genQuesOneKPI(view = None):
    listQuesOneKPI = [
        f"{genDesView(view)} {genPrefixQuestion()} {genDesOneKPI()} ?",
        f"{genPrefixQuestion()} {genDesView(view)} {genDesOneKPI()} ?",
        f"{genPrefixQuestion()} {genDesOneKPI()} {genDesView(view)} ?"
    ]
    
    return random.choice(listQuesOneKPI)

#=================oneKPI===================

#=================groupKPIOverall===================

def genPharaCum():
    listPharaCum = [
        "nhóm",
        "cụm",
        "tập hợp"
    ]
    
    return random.choice(listPharaCum)

def genOverall():
    listOverall = [
        "khái quát",
        "tổng quan",
        "tổng thể",
        "cơ bản",
        "tổng hợp",
        "tóm tắt"
    ]
    
    return random.choice(listOverall)

def genVision():
    listVision = [
        "góc nhìn",
        "khía cạnh",
        "cái nhìn",
        "tầm nhìn",
        "phân tích",
        "quan sát",
        "quan điểm",
        "tiếp cận",
        "đánh giá",
        "mô tả",
        "tình hình",
        ""
    ]

    return random.choice(listVision)

def genPostfixGroup():
    listPostfixGroup = [
        "như thế nào",
        "thế nào",
        "ra làm sao",
        "ra sao"
    ]
    
    return random.choice(listPostfixGroup)

def genDesOverall():
    listDesOverall = [
        f"{genVision()} {genOverall()} của {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> {genComp()}",
        f"{genVision()} {genOverall()} các chỉ tiêu con của {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> {genComp()}",
        f"{genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> có {genOverall()} về các chỉ tiêu con {genPostfixGroup()}",
        f"{genOverall()} các chỉ tiêu thuộc về {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> {genComp()}",
        f"liệt kê {genOverall()} hơn về các chỉ tiêu trong {genPharaCum()} chỉ tiêu <tên chỉ tiêu> {genComp()}",
        f"{genVision()} {genOverall()} của {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> {genPostfixGroup()}",
        f"{genVision()} {genOverall()} {genPostfixGroup()} về {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> {genComp()}",
    ]
    
    return random.choice(listDesOverall)

def genQuesGroupKPIOverall(view = None):
    listQuesGroupKPIOverall = [
        f"{genDesView(view)} {genPrefixQuestion()} {genDesOverall()} ?",
        f"{genPrefixQuestion()} {genDesView(view)} {genDesOverall()} ?",
        f"{genPrefixQuestion()} {genDesOverall()} {genDesView(view)} ?"
    ]
    
    return random.choice(listQuesGroupKPIOverall)    

#=================groupKPIOverall===================

#=================groupKPIDetail==================
def genDetail():
    listDetail = [
        "chi tiết",
        "sâu hơn",
        "tường tận",
        "cặn kẽ",
        "tỉ mỉ",
        "đầy đủ",
        "tường minh",
        "rõ ràng"    
    ]
    
    return random.choice(listDetail)

def genQuesDat():
    listQuesDat = [
        "chỉ những chỉ tiêu đạt",
        "với những chỉ tiêu đạt",
        "với những chỉ tiêu đã được đánh giá là đạt",
        "trong những chỉ tiêu đã được xác nhận là đạt",
        "bao gồm những chỉ tiêu đạt"
    ]
    
    return random.choice(listQuesDat)

def genQuesKoDat():
    listQuesKoDat = [
        "chỉ những chỉ tiêu không đạt",
        "với những chỉ tiêu chưa đạt",
        "với những chỉ tiêu đã được đánh giá là chưa đạt",
        "trong những chỉ tiêu đã được xác nhận là không đạt",
        "bao gồm những chỉ tiêu không đạt"
    ]

    return random.choice(listQuesKoDat)

def genQuesAll():
    listQuesAll = [
        "toàn bộ các chỉ tiêu con",
        "đầy đủ các chỉ tiêu con",
        "tất cả chỉ tiêu con trong nhóm này",
        "các chỉ tiêu con",
        "bao gồm tất cả chỉ tiêu"
    ]
    
    return random.choice(listQuesAll)

dict_ques = {
    0 : genQuesDat(),
    1 : genQuesKoDat(),
    2 : genQuesAll()
}

def genDetailQues(index=None):
    if index is None:
        index = random.choice([*range(3)])
    ques = dict_ques[index]
    listGenQues = [
        f"{genVision()} {genDetail()} của {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> {genComp()}",
        f"{genVision()} {genDetail()} hơn {ques} của {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> {genComp()}",
        f"chi tiết hơn của cụm chỉ tiêu <cụm chỉ tiêu> {ques} {genComp()}",
        f"thông tin {genDetail()} hơn về {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> {ques} {genComp()}",
        f"{ques} của {genPharaCum()} chỉ tiêu <tên cụm chỉ tiêu> để hiểu rõ hơn về nó",
    ]
    
    return random.choice(listGenQues)

def genGroupKPIDetail(view = None,index=None):
    listGroupKPIDetail = [
        f"{genDesView(view)} {genPrefixQuestion()} {genDetailQues(index)}?",
        f"{genPrefixQuestion()} trong {genDesView(view)} {genDetailQues(index)}?",
        f"{genPrefixQuestion()} {genDetailQues(index)} trong {genDesView(view)}?"
    ]
    
    return random.choice(listGroupKPIDetail)
#=================groupKPIDetail==================

#=================InferenceMom====================
def genAdv3():
    listAdv3 = [
        "bên cạnh đó",
        "ngoài ra",
        "thêm vào đó",
        "không chỉ vậy",
        "và còn nữa",
        "hơn thế"
    ]
    
    return random.choice(listAdv3)

def genDesc1():
    listDesc1 = [
        "cho biết thêm",
        "bổ sung",
        "liệt kê ra",
        "nêu thêm",
        "nói ra"
    ]
    
    return random.choice(listDesc1)

def genChainList():
    listChainList = [
        f"{genAdv3()} {genDesc1()} một vài thông tin của các chỉ tiêu trong {genComp()} chỉ tiêu mẹ này",
        f", trong chỉ tiêu mẹ này hãy cho {genDesPerson()} biết thêm thông tin các chỉ tiêu còn lại",
        f"{genAdv3()} và thêm cả thông tin các chỉ tiêu chung nhóm với <tên chỉ tiêu>",
        f"và một vài thông tin của các chỉ tiêu con khác",
        f"{genAdv3()} thông tin của các chỉ tiêu con khác trong cùng nhóm"
    ]
    
    return random.choice(listChainList)

def genChainList1():
    listChainList1 = [
        f"và tình hình các tháng trước của chỉ tiêu <tên chỉ tiêu> này như thế nào",
        f"{genAdv3()} chỉ tiêu này các tháng trước như thế nào",
        f"và <tên chỉ tiêu> các tháng trước ra làm sao",
        f"và các tháng trước có đạt nhiều hay không",
        f"{genAdv3()} có thể dự đoán tháng tiếp theo như thế nào không?",
        f"và các tháng trước có số kpi đạt bao nhiêu",
        f"{genAdv3()} số kpi chưa đạt tháng trước là bao nhiêu"
    ]
    
    return random.choice(listChainList1)

def genChain(index=None):
    listChain = [
        f"{genChainList()}",
        f"{genChainList1()}",
        ""
    ]
    
    if index is None:
        return random.choice(listChain)
    return listChain[index]

def genInferMomQues(index = None):
    listInferMom = [
        f"chỉ tiêu <tên chỉ tiêu> thuộc về chỉ tiêu mẹ <tên cụm chỉ tiêu> là gì",
        f"chỉ tiêu mẹ của chỉ tiêu <tên chỉ tiêu> là gì",
        f"chỉ tiêu con <tên chỉ tiêu> được phân loại vào {genPharaCum()} chỉ tiêu mẹ nào",
        f"chỉ tiêu mẹ của chỉ tiêu con <tên chỉ tiêu> có tên là gì trong danh sách chỉ tiêu",
        f"thông tin về chỉ tiêu mẹ của chỉ tiêu <tên chỉ tiêu>",
    ]
    
    return random.choice(listInferMom) + ' ' + genChain(index)

def genInferenceMom(index=None):
    listInfernceMom = [
        f"{genDesView('month')} {genPrefixQuestion()} {genInferMomQues(index)}?",
        f"{genPrefixQuestion()} trong {genDesView('month')} {genInferMomQues(index)}?",
        f"{genPrefixQuestion()} {genInferMomQues(index)} trong {genDesView('month')}?"
    ]
    
    return random.choice(listInfernceMom)
#=================InferenceMom====================

#=================CrossView====================
def genRes():
    listRes = [
        "đạt",
        "chưa đạt",
        "ổn",
        "không ổn",
        "tốt",
        "không tốt"
    ]
    
    return random.choice(listRes)


def genRes1():
    listRes1 = [
        "kết quả",
        "đánh giá",
        "tình hình",
        "xem xét",
        "hiện trạng nhận được"
    ]
    
    return random.choice(listRes1)

def genExplainYear():
    listExplainYear = [
        f", cho {genDesPerson()} biết thêm về {genRes1()} của năm được hay không",
        f", còn năm thì {genPostfixGroup()} đấy",
        f", liệu có ảnh hưởng gì kết quả năm hay không",
        f", {genRes1()} về KPI của năm ra làm sao",
        f", hiện trạng của năm bây giờ như thế nào",
        f"",
        f""
    ]
    
    return random.choice(listExplainYear)

def genStrange():
    listStrange = [
        "hiện tượng lạ",
        "bất thường",
        "nhiễu động",
        "sự bất thường",
        "hiện tượng kì lạ",
        "hiện tượng gì lạ"
    ]
    
    return random.choice(listStrange)
    
def genDescMonthQuarter():
    listDescMonthQuarter = [
        "quý và tháng",
        "tháng và quý",
        "tháng với quý",
        "quý vớI tháng"
    ]
    
    return random.choice(listDescMonthQuarter)
    
def genCross():
    listCross = [
        f"chỉ tiêu <tên chỉ tiêu> có kết quả đánh giá trong cùng {genDescMonthQuarter()} {genPostfixGroup()}",
        f"{genRes1()} đối với {genDescMonthQuarter()} {genPostfixGroup()} với chỉ tiêu <tên chỉ tiêu>"
        f"so sánh {genRes1()} nhận được của {genDescMonthQuarter()} với chỉ tiêu <tên chỉ tiêu>",
        f"so sánh {genRes1()} nhận được của chỉ tiêu <tên chỉ tiêu> trong {genDescMonthQuarter()}",
        f"{genRes1()} tháng của chỉ tiêu <tên chỉ tiêu> khác gì so với quý",
        f"{genRes1()} của quý mà chỉ tiêu <tên chỉ tiêu> khác nhau {genPostfixGroup()} so với tháng",
        f"liệu cả {genDescMonthQuarter()} của chỉ tiêu <tên chỉ tiêu> có cùng {genRes()} hay không",
        f"có {genStrange()} nào khi so sánh của kết quả {genDescMonthQuarter()} của chỉ tiêu <tên chỉ tiêu> hay không",
        f"cả {genDescMonthQuarter()} đều nhận được {genRes1()} {genRes()} của chỉ tiêu <tên chỉ tiêu> hay không",
        f"liệu có bất thường nào khi so sánh {genRes1()} tháng và quý của chỉ tiêu <tên chỉ tiêu> không",
        f"có thấy {genStrange()} khi so sánh {genRes1()} tháng và quý của chỉ tiêu <tên chỉ tiêu> không",
        f"{genRes1()} của tháng và quý của chỉ tiêu <tên chỉ tiêu> {genPostfixGroup()}",
        f"thống kê về kết quả của {genDescMonthQuarter()} chỉ tiêu <tên chỉ tiêu>"
    ]
    
    return random.choice(listCross) + ' ' + genExplainYear()

def genQuesCrossView():
    listQuesCrossView = [
        f"{genDesView('month')} {genPrefixQuestion()} {genCross()}?",
        f"{genPrefixQuestion()} trong {genDesView('month')} {genCross()}?",
        f"{genPrefixQuestion()} {genCross()} trong {genDesView('month')}?"
    ]
    
    return random.choice(listQuesCrossView)
#=================CrossView====================

#=================TongCongty===================
def genComp1():
    listComp1 = [
        'tổng công ty <tên tổng công ty>',
        '<tên tổng công ty>',
        'công ty <tên tổng công ty>',
        'tổng công ty có tên là <tên tổng công ty>',
        'tổng công ty mang tên <tên tổng công ty>'
    ]
    
    return random.choice(listComp1)

def genPrefix1():
    listPrefix1 = [
        "chi tiết",
        "tổng quát",
        "sâu hơn",
        "tổng quan"
    ]
    
    return random.choice(listPrefix1)

def genTongCongTy():
    listTongCongTy = [
        f"thống kê tình hình của {genComp1()}",
        f"{genComp1()} có {genRes1()} {genPostfixGroup()}",
        f"cho tôi biết tổng quan về {genComp1()} {genPosfix()}",
        f"thông tin về {genComp1()}",
        f"{genRes1()} làm việc của {genComp1()}",
        f"đưa ra báo cáo về tình hình {genComp1()}",
        f"{genPrefix1()} về hiện trạng KPI {genComp1()}",
        f"KPI của {genComp1()}"
    ]
    
    return random.choice(listTongCongTy)

def genQuesTongCongTy(view = None):
    listQuesTongCongTy = [
        f"{genDesView(view)} {genPrefixQuestion()} {genTongCongTy()}?",
        f"{genPrefixQuestion()} trong {genDesView(view)} {genTongCongTy()}?",
        f"{genPrefixQuestion()} {genTongCongTy()} trong {genDesView(view)}?"
    ]
    
    return random.choice(listQuesTongCongTy)
#=================TongCongty===================

#=================TrendStat====================
def genCheck():
    listCheck = [
        "cập nhật",
        "đánh giá",
        "cho biết",
        "tình hình",
        "thống kê"
    ]
    
    return random.choice(listCheck)

def genDescSeason():
    listDescSeason = [
        "gần đây",
        "gần nhất",
        "mới nhất",
        "mới gần đây",
        "vừa qua"
    ]
    
    return random.choice(listDescSeason)

def genSeason():
    listSeason = [
        f"trong <năm> năm {genDescSeason()} của tháng <tháng>, chỉ tiêu <tên chỉ tiêu> có {genCheck()} {genPostfixGroup()}",
        f"chỉ tiêu <tên chỉ tiêu> được đánh giá trong <năm> năm {genDescSeason()} của tháng <tháng> có {genCheck()} {genPosfix()}",
        f"vào tháng <tháng> của <năm> năm {genDescSeason()}, kết quả của chỉ tiêu <tên chỉ tiêu> {genPosfix()}",
        f"tính từ <tháng> với các năm từ 2020 đến <năm>, chỉ tiêu <tên chỉ tiêu> được đánh giá {genPostfixGroup()}"
        f"{genVision()} chỉ tiêu <tên chỉ tiêu> tính từ <tháng> với các năm từ 2020 đến <năm> {genPostfixGroup()}",
        f"{genRes1()} của chỉ tiêu <tên chỉ tiêu> trong <năm> năm {genDescSeason()} của tháng <tháng>"
    ]
    
    return random.choice(listSeason)

def genMonthBefore():
    listMonthBefore = [
        f"tính đến {genDesViewMonth()} và các tháng trước đó thì chỉ tiêu <tên chỉ tiêu> hiện được kết quả {genPostfixGroup()}",
        f"chỉ tiêu <tên chỉ tiêu> với các tháng trong năm tính đến {genDesViewMonth()} hiện được đánh giá thế nào",
        f"{genCheck()} về hiện trạng của chỉ tiêu <tên chỉ tiêu> từ đầu <năm> đến tháng <tháng>",
        f"{genRes1()} {genOverall()} từ đầu năm đến {genDesViewMonth()} của chỉ tiêu <tên chỉ tiêu>",
        f"{genCheck()} {genRes1()} của chỉ tiêu <tên chỉ tiêu> từ 1/<năm> đến <tháng>/<năm> {genPostfixGroup()}",
        f"từ 1/<năm> đến <tháng>/<năm>, hiện chỉ tiêu <tên chỉ tiêu> có {genCheck()} {genPostfixGroup()}",
        f"chỉ tiêu <tên chỉ tiêu> được đánh giá {genOverall()} ra làm sao với các tháng trong năm tính đến <tháng>/<năm>",
    ]
    
    return random.choice(listMonthBefore)

def genTrendStat(choice=""):
    if choice == "":
        choice = random.choice(['season','monthBefore'])
    if choice == "monthBefore": return genMonthBefore()
    return genSeason()

def genQuesTrendStat():
    listQuesTongCongTy = [
        f"{genPrefixQuestion()} {genComp()} {genTrendStat()}?",
        f"{genPrefixQuestion()} {genTrendStat()} {genComp()}?"
    ]
    
    return random.choice(listQuesTongCongTy)
#=================TrendStat====================

#=================TrendPredict=================
def genDescPredict():
    listDescPredict = [
        "dự đoán",
        "dự báo",
        "dự trù",
        "dự định",
        "uớc tính",
        "dự liệu",
        "ước lượng"
    ]
    
    return random.choice(listDescPredict)

def genNextMonth():
    listNextMonth = [
        "trong tháng tiếp theo",
        "vào tháng kế tiếp",
        "vào tháng sau",
        "vào tháng <tháng+1>",
        "vào tháng tới"
    ]
    
    return random.choice(listNextMonth)

def genResMonth():
    listResMonth = [
        "KPI đạt được là bao nhiêu",
        "kết quả nhận được là bao nhiêu",
        "hiện trạng là",
        "được bao nhiêu <đơn vị>",
        "KPI <đơn vị> nhận được là"
    ]
    
    return random.choice(listResMonth)

def genDescNextMonth():
    listDescNextMonth = [
        f"từ đầu <năm> đến tháng <tháng>",
        f"từ 1/<năm> đến <tháng>/<năm>",
        f"với các tháng trong năm tính đến <tháng>/<năm>",
        f"tháng <tháng> và các tháng trước đó trong <năm>"
    ]

    return random.choice(listDescNextMonth)

def genDescSeason1():
    listDescSeason = [
        f", trong <năm> năm {genDescSeason()} của tháng <tháng>",
        f", tính từ <tháng> với các năm từ 2020 đến <năm>",
        f", vào tháng <tháng> của <năm> năm {genDescSeason()}",
    ]
    
    return random.choice(listDescSeason)

def genKPI():
    listKPI = [
        "với các kết quả chỉ tiêu <tên chỉ tiêu> đã nhận",
        "với chỉ tiêu <tên chỉ tiêu> đã nhận",
        "khi nhận được các kết quả từ chỉ tiêu <tên chỉ tiêu>",
        "chỉ tiêu <tên chỉ tiêu> đã nhận được các đánh giá"
    ]
    
    return random.choice(listKPI)

def genTrendPredictNextMonth():
    now = random.choice([genKPI() + ' ' + genDescNextMonth(),
                         genDescNextMonth() + ' ' + genKPI()
                        ])
    
    listTrendPredictNextMonth = [
        f"{now} thì {genDescPredict()} {genNextMonth()} {genResMonth()}",
        f"{genKPI()} {genComp()} thì {genNextMonth()} {genDescPredict()} {genResMonth()} ({genDescNextMonth()})",
        f"{genDescNextMonth()} {genNextMonth()} {genDescPredict()} {genResMonth()} {genKPI()}"
    ]
    
    return random.choice(listTrendPredictNextMonth)

def genTrendPredictSeason():
    now = random.choice([genKPI() + ' ' + genComp() + ' ' + genDescSeason1(),
                         genDescSeason1() + ' ' + genKPI() + ' ' + genComp(),
                         genDescSeason1() + ' ' + genKPI(),
                         genKPI() + ' ' + genDescSeason1() 
                        ])
    
    listTrendPredictSeason = [
        f"{now} {genDescPredict()} {genResMonth()} {genNextMonth()}",
        f"{now} {genDescPredict()} {genNextMonth()} {genResMonth()}",
        f"{genKPI()} {genComp()} {genNextMonth()} {genDescPredict()} {genResMonth()} {genDescSeason1()}"
    ]
    
    return random.choice(listTrendPredictSeason)

def genTrendPredict(choice=""):
    if choice == "":
        choice = random.choice(['season','monthBefore'])
    if choice == "season": return genTrendPredictSeason()
    return genTrendPredictNextMonth()

def genQuesTrendPredict():
    listQuesTrendPredict = [
        f"{genPrefixQuestion()} {genTrendPredict()}?",
        f"{genPrefixQuestion()} {genTrendPredict()}?"
    ]
    
    return random.choice(listQuesTrendPredict)    
#=================TrendPredict=================

#=================ExplainResult================

#=================ExplainResult================

if __name__ == "__main__":
    print(genQuesTrendPredict())