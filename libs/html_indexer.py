import re

PATH = 'input_files/'
base_file=PATH+"html_base.txt"

###Using the "@" as a separator, when the for comes to it's line writes all the data 
def write_file(text, filename):
    c=open(base_file,"r")
    html=""
    for line in c.readlines():
        if re.search(r'@',line):
            html+=text
        else:    
            html+=str(line)    

    with open(filename,'w',encoding="utf-8") as f:
        f.write(html)
        f.close()
    c.close()

def convert2HTML(dic):
    s = '''<div id="box" align="center"><table>
    <tr>
    <th>Categoria</th>
    <th>Ocorrencias</th>
    <tr>
    '''
    tags = [x for x in dic]
    for tag in tags:
        s += f'\t<tr>\n\t\t<td>{tag[0:]}</td>\n\t\t<td>{dic[tag]}</td>\n\t</tr>\n'
    s += '</table></div>'
    return s

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


def write_document(documents):
    text=""
    for document in documents:
        text += parse_document(document)
    return text




