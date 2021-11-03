
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
        s += f'\t<LI>{tag[1:]}: {dic[tag]}</LI>\n'
    s += '</UL>'
    return s




def write_to_file(dic,file):
    text= convert2HTML(dic)
    write_file(text,file)


def parse_search(matches,file):
    return convert2HTML(matches)

def parse_document(doc):
    authors=""
    i=0
    for auth in doc.Authors: 
        i+=1
        authors += auth 
        if(i<len(doc.Authors)>1):
            authors+=","

    s='<div id="box" align="center"><div text-align="left">'
    s+="<strong>"+str(doc.title)+"</strong>"
    for i in range(1,len(list(authors))):
        if(i % 40==0):
            authors=str(authors[:i])+"-\n"+str(authors[i:])
        i+=1
    s+="<p> Autores:"+str(authors)+" </p>"
    s+="<p> Categoría:"+str(doc.category)  +" </p>"
    s+="<p> Clave:"+str(doc.key)+" </p>"
    s+="</div></div>"
    return s


def write_document(documents,file):
    text=""
    for document in documents:
        text += parse_document(document)
    write_file(text,file)




