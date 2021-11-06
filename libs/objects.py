import re
from libs.functions import sub_array, get_specialchars

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
                    aux_colaborators.append(colab)
        self.colaborators = aux_colaborators
    

    def print_author(self):
        print(f'{self.raw_name}:\n  Publicaciones:')
        for pub in self.publications:
            print(f'\t -{pub}')
        print(f'  Colaboradores:')
        colaborators = list(self.colaborators.keys())
        colaborators.sort()
        for colab in colaborators:
            print(f'    -{colab} = {self.colaborators[colab]}')