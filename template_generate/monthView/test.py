import random

##(tháng <tháng> năm <năm> | <tháng>/<năm>) => (A|B)

def genMonthYearDesc():
    listMonthYearDesc = [
        "tháng <tháng> năm <năm>",
        "<tháng>/<năm>"
    ]
    
    return random.choice(listMonthYearDesc)

def genPrefixDesc(index=None):
    listPrefixDesc = [
        f"trong {genMonthYearDesc()}, chỉ tiêu <tên chỉ tiêu> của (tổng công ty|) <tổng công ty> có (kết quả là | đã) <đạt/không đạt>",
        "Chỉ tiêu <tên chỉ tiêu> của (tổng công ty|) <tên tổng công ty> trong (tháng <tháng> năm <năm> | <tháng>/<năm>) có (kết quả là | đã) <đạt/không đạt>"
    ]
    
    if index is None:
        return random.choice(listPrefixDesc)

    assert(index < len(listPrefixDesc))
    return listPrefixDesc[index]