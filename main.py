from libs.functions import applyER_text, count_matches, sub_array ,split_array
from libs.objects import Author, Document
from libs.grafo import Grafo
from libs.html_indexer import write_to_file, write_document

PATH = 'input_files/'
OUT_PATH = 'output_files/'
FILENAME = 'exemplo-utf8.bib'
FILE = PATH+FILENAME

CATEGORY_ER = r'@([a-zA-Z]+)'
KEY_ER = r'\{([a-zA-Z0-9.:\-\\]+),\n'
AUTHOR_ER = r'(?i:author)[ \t]*=[ \t]*[{"]([^}"]+)[\n\t ]*[}"]' 
TITLE_ER = r' (?i:title)[ \t]*=[ \t]*((.+?|[\n\t ])*?)(?=[}"] ?,)'
EXTRACT_NAME_ER = r'([A-Z])(.+ +)+(.+)$'


if __name__ == '__main__':
    categories =applyER_text(CATEGORY_ER,FILE,1)
    keys = applyER_text(KEY_ER,FILE,1)
    authors = split_array(sub_array(sub_array(sub_array(applyER_text(AUTHOR_ER,FILE,1),r'[ \-\n\t{]+'," "),r'^ ',r''),r'([ ]+and)([ ]+and[ ]*)',r'\2'),'[ ]+and[ ]*')
    titles = sub_array(sub_array(applyER_text(TITLE_ER,FILE,1),r'^[{"]',""),r'[\n\t ]+',r' ')

    DOCUMENTS = [Document(categories[i],authors[i],titles[i],keys[i]) for i in range(len(keys))]

    dic_categories = count_matches(categories)
    dic_authors = {}
    for doc in DOCUMENTS:
        for auth in doc.authors:
            aux_auth = Author(auth)
            aux_auth.add_publication(doc)
            try:
                dic_authors[auth].concat_author(aux_auth)
            except:
                dic_authors[auth] = aux_auth
    
    authors = list(dic_authors.keys())
    for auth in authors:
        for bauth in authors:
            if auth == bauth:
                continue
            if dic_authors[auth].is_samePerson(dic_authors[bauth]):
                if len(bauth) > len(auth):
                    auth,bauth = bauth,auth
                dic_authors[auth].concat_author(dic_authors[bauth])
                dic_authors.pop(bauth)
                authors.remove(bauth)

    authors = list(dic_authors.keys())
    authors.sort()
    dic_names = {}
    for i,a in enumerate(authors):
        try:
            dic_names[dic_authors[a].get_iniciales()] += [dic_authors[a]]
        except:
            dic_names[dic_authors[a].get_iniciales()] = [dic_authors[a]]
        author = dic_authors[a]

    for a in authors:
        dic_authors[a].clean_authors(dic_names)

    for doc in DOCUMENTS:
        doc.clear_authors(dic_names)
    
    write_to_file(dic_categories,OUT_PATH+"exercise2.html")
    write_document(DOCUMENTS,OUT_PATH+"exercise1.html")

    grafo=Grafo()
    grafo.load_names(list(dic_authors.values()))
    grafo.map_authors()
    grafo.generate_graph("authors_colaborations.txt")
    grafo.generate_graph_author(dic_authors['Alexandre Carvalho'],"author_colaboration.txt")


