import re

def applyER_text(ER,file,ngroup=0):
    matches = []
    with open(file,'r',encoding='UTF-8') as f:
        text = f.read()
        f.close()

    while m:=re.search(ER,text):
        text = text[m.end()+1:]
        matches.append(m.group(ngroup))
    return matches

def split_array(array,er):
    for k,a in enumerate(array):
        array[k] = re.split(er,a)
    return array


def sub_array(array,er,sub):
    for k,a in enumerate(array):
        array[k] = re.sub(er,sub,a)
    return array

def search_array(array,er,ngroup=0):
    matches = []
    for a in array:
        matches.append(re.search(er,a)).group(ngroup)
    return matches

def count_matches(matches):
    dic = {}
    for match in matches:
        try:
            dic[match] += 1
        except:
            dic[match] = 1
    return dic

special_chars = {
    "~a" : "ã",
    "´a" : "á",
    "`a" : "à",
    "^a" : "â",
    "'a" : "á",
    "´e" : "é",
    "`e" : "è",
    "^e" : "ê",
    "'e" : "é",
    "´i" : "í",
    "`i" : "ì",
    "^i" : "î",
    "~o" : "õ",
    "´o" : "ó",
    "`o" : "ò",
    "^o" : "ô",
    "'o" : "ó",
    "´u" : "ú",
    "`u" : "ù",
    "^u" : "û",
    "~A" : "Ã",
    "´A" : "Á",
    "`A" : "À",
    "^A" : "Â",
    "'A" : "Á",
    "´E" : "É",
    "`E" : "È",
    "^E" : "Ê",
    "'E" : "É",
    "´I" : "Í",
    "`I" : "Ì",
    "^I" : "Î",
    "~O" : "Õ",
    "´O" : "Ó",
    "`O" : "Ò",
    "^O" : "Ô",
    "'O" : "Ó",
    "´U" : "Ú",
    "`U" : "Ù",
    "^U" : "Û",
}

def get_specialchars(m):
    special_char = m[1]
    trade_char = special_chars[special_char]
    return trade_char

def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += ele  
    return str1 
        