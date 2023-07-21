import re

#===========================================================================
#post process output:
##Viết hoa đầu câu hoặc sau dấu chấm
##Bỏ đi một số dấu bị dư (kiểu như hai dấu liên tiếp như: ",,", ", ", ". ")
##Đưa dạng "abc ," về dạng "abc,"
##Strip,Replace("  "," ").

def replace_commas_and_dots(input_string):
    # Thay thế ",," thành ","
    replaced_string = re.sub(r',+', ',', input_string)
    # Thay thế ".." thành "."
    replaced_string = re.sub(r'\.+', '.', replaced_string)
    return replaced_string

def postProcessOutput(sent):
    sent = sent.lower().strip().replace('  ',' ').replace(' ,',',').replace(' .','.')
    sent = replace_commas_and_dots(sent)
    sents = sent.split('.')
    newSent = []
    for text in sents:
        if len(text) == 0: continue
        text = text.strip()
        firstDigit = text[0]
        parital = text[1:]
        newSent.append(firstDigit.upper()+parital)
    return ". ".join(newSent)

#===========================================================================