import re
from libs.functions import sub_array, get_specialchars,applyER_text,split_array,count_matches
import pickle

EXTRACT_NAME_ER = r'([A-Z])(.+ +)+(.+)$'
CORRECT_NAME_ER = r'(.+), *(.+)'
SPECIAL_CHARS_ER = r"\\([´`~^'][aeiou])"

class Document:
    def __init__(self,category,authors,title,key):
        self.category = category
        self.key = key
        self.authors = sub_array(sub_array(sub_array(authors,CORRECT_NAME_ER,r'\2 \1'),r' $',r''),SPECIAL_CHARS_ER,get_specialchars)
        self.title = re.sub(SPECIAL_CHARS_ER,get_specialchars,title)
    
    def clear_authors(self,dic):
        self.Authors = []
        for author in self.authors:
            aux = Person(author)
            colaborators = dic[aux.get_iniciales()]
            for colab in colaborators:
                if colab.is_samePerson(aux):
                    self.Authors.append(colab.get_name())

    
class Person:
    def __init__(self,name):
        self.raw_name = name
        match = re.search(r'([A-Z])([^ ]*) +.* *([A-Z])([^ ]*)',name)
        splits = re.split(r' +',name)
        self.DefaultName = None
        self.middle_inicial = None
        self.Name = ''
        if match:
            self.iniciales = f'{match.group(1)}. {match.group(3)}.'
            self.FirstName = f'{match.group(1)}{match.group(2)}'
            if '.' in self.FirstName:
                if len(self.FirstName) > 2:
                    self.middle_inicial = self.FirstName[-2]
                self.Name += self.FirstName+' '
                self.FirstName = None
            else:
                self.Name += self.FirstName+' '
            if len(splits)>2:
                self.MiddleName = ""
                for s in splits[1:-1]:
                    self.MiddleName += s+' '
                if '.' in self.MiddleName:
                    self.middle_inicial = re.sub(r'[. ]','',self.MiddleName)
                    self.MiddleName = None
                    self.Name += self.middle_inicial+'. '
                else:
                    self.middle_inicial = self.MiddleName[0]
                    self.Name += self.MiddleName
            else:
                self.MiddleName = None
            self.LastName = f'{match.group(3)}{match.group(4)}'
            self.Name += self.LastName
        else:
            self.DefaultName = name
        
    
    def is_samePerson(self,person):
        if self.DefaultName or person.DefaultName:
            return 
        if self.get_name() == person.get_name():
            return True
        FN = self.FirstName and person.FirstName and self.FirstName == person.FirstName
        MN = self.MiddleName and person.MiddleName and self.MiddleName == person.MiddleName
        LN = self.LastName and person.LastName and self.LastName == person.LastName
        IN = self.iniciales == person.iniciales
        MIN = self.middle_inicial and person.middle_inicial and self.middle_inicial == person.middle_inicial
        if not IN:
            return False
        if FN and MN and LN:
            return True
        if MIN and FN and LN:
            return True
        if MN and LN:
            return True
        if MIN and LN:
            return True
        return FN and LN
    
    def get_name(self):
        if self.DefaultName:
            return self.DefaultName
        return self.Name

    def get_iniciales(self):
        if self.DefaultName:
            return self.DefaultName
        return self.iniciales

class Author(Person):
    def __init__(self,author):
        super().__init__(author)
        self.publications = []
        self.colaborators = []

    def add_colaborator(self,name):
        if not name in self.colaborators:
            self.colaborators.append(name)
            
    def add_publication(self,doc):
        self.publications.append(doc.title)
        for auth in doc.authors:
            if auth != self.raw_name:
                self.add_colaborator(auth)
    
    def concat_author(self, author):
        self.publications += author.publications
        for colab in author.colaborators:
            self.add_colaborator(colab)

    def clean_authors(self,dic):
        aux_colaborators = []
        authors = self.colaborators
        authors.sort()
        for auth in authors:
            auth1 = Person(auth)
            for bauth in authors:
                if auth == bauth:
                    continue
                auth2 = Person(bauth)
                if auth1.is_samePerson(auth2):
                    if len(bauth) > len(auth):
                        auth,bauth = bauth,auth
                    authors.remove(bauth)
            aux = Person(auth)
            colaborators = dic[aux.get_iniciales()]
            for colab in colaborators:
                if colab.is_samePerson(aux):
                    aux_colaborators.append(colab.get_name())
        self.colaborators = aux_colaborators
    

    def print_author(self):
        print(f'{self.get_name()}:\n  Publicaciones:')
        for pub in self.publications:
            print(f'\t -{pub}')
    
    def print_colaborators(self):
        print(f'{self.get_name()}:\n  Colaboradores:')
        for colab in self.colaborators:
            print(f'\t -{colab}')

CATEGORY_ER = r'@([a-zA-Z]+)'
KEY_ER = r'\{([a-zA-Z0-9.:\-\\]+),\n'
AUTHOR_ER = r'(?i:author)[ \t]*=[ \t]*[{"]([^}"]+)[\n\t ]*[}"]' 
TITLE_ER = r' (?i:title)[ \t]*=[ \t]*((.+?|[\n\t ])*?)(?=[}"] ?,)'
EXTRACT_NAME_ER = r'([A-Z])(.+ +)+(.+)$'


def create_objects(PATH,FILENAME):
    FILE = PATH+FILENAME
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
    for a in authors:
        try:
            dic_names[dic_authors[a].get_iniciales()] += [dic_authors[a]]
        except:
            dic_names[dic_authors[a].get_iniciales()] = [dic_authors[a]]

    for a in authors:
        dic_authors[a].clean_authors(dic_names)

    dic_documents = {}

    for doc in DOCUMENTS:
        doc.clear_authors(dic_names)
        dic_documents[doc.key] = doc

    return dic_documents,dic_authors,dic_categories

LIBRARY_PATH = 'library/'

def save_objects(INPUT_PATH,FILENAME):
    dic_documents,dic_authors,dic_categories = create_objects(INPUT_PATH,FILENAME)
    docs = open(LIBRARY_PATH+'data_documents.pkl','wb')
    pickle.dump(dic_documents,docs,pickle.HIGHEST_PROTOCOL)
    docs.close()
    docs = open(LIBRARY_PATH+'data_authors.pkl','wb')
    pickle.dump(dic_authors,docs,pickle.HIGHEST_PROTOCOL)
    docs.close()
    docs = open(LIBRARY_PATH+'data_categories.pkl','wb')
    pickle.dump(dic_categories,docs,pickle.HIGHEST_PROTOCOL)
    docs.close()

def open_objects(key):
    if key == 'authors':
        docs = open(LIBRARY_PATH+'data_authors.pkl','rb')
        return pickle.load(docs)
    if key == 'documents':
        docs = open(LIBRARY_PATH+'data_documents.pkl','rb')
        return pickle.load(docs)
    if key == 'categories':
        docs = open(LIBRARY_PATH+'data_categories.pkl','rb')
        return pickle.load(docs)