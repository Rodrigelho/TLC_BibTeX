import re

PATH = 'input_files/'
base_file=PATH+"html_base.txt"

###Using the "@" as a separator, when the for comes to it's line writes all the data 
def write_file(text, filename):
    c=open(base_file,"r")
    html=""
    for line in c.readlines():
        if(line.__contains__("@")):
            html+=text
        else:    
            html+=str(line)    

    with open(filename,'w',encoding="utf-8") as f:
        f.write(html)
        f.close()
    c.close()

def convert2HTML(dic):
    s = '<UL>\n'
    tags = [x for x in dic]
    for tag in tags:
        s += f'\t<LI>{tag[0:]}: {dic[tag]}</LI>\n'
    s += '</UL>'
    return s




def write_to_file(dic,file):
    text= convert2HTML(dic)
    write_file(text,file)


def parse_search(matches):
    return convert2HTML(matches)

def parse_document(doc):
    authors=""
    i=0
    for auth in doc.Authors: 
        i+=1
        authors += auth 
        if(i<len(doc.Authors)>1):
            authors+=","
    title = re.sub(r'\\.+{([^}]+)}',r'<textsc>\1</textsc>',str(doc.title))
    s='<div id="box" align="center"><div id="text_box" text-align="left">\n'
    s+="<h1><strong>"+re.sub(r'{([^}]+)}',r'\1',title)+"</strong></h1>\n"
    s+="\t<p> <strong>Autores:</strong> "+str(authors)+" </p>\n"
    s+="\t<p> <strong>Categoría:</strong> "+str(doc.category)  +" </p>\n"
    s+="\t<p> <strong>Clave:</strong> "+str(doc.key)+" </p>\n"
    s+="</div></div>"
    return s


def write_document(documents,file):
    text=""
    for document in documents:
        text += parse_document(document)
    write_file(text,file)




