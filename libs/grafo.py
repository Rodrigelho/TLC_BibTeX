import numpy 
import sys
numpy.set_printoptions(threshold=sys.maxsize)


class Grafo:
    def __init__(self):
        self.nodos=[]
        self.mapa_colaboraciones=[]

    def extract_position(self,name):
        return self.dic[name][0]

    def load_names(self,dic_authors):
        self.dic = dic_authors
        list_authors = list(dic_authors.keys())
        list_authors.sort()
        for author in list_authors:
            self.nodos.append(dic_authors[author][1])
        self.load_matrix()

    def load_matrix(self):
        self.mapa_colaboraciones=[[0 for x in range(len(self.nodos))] for y in range(len(self.nodos))] 


    def map_authors(self):
        for i,author in enumerate(self.nodos):
            for colaborator in author.colaborators:
                j=self.extract_position(colaborator)
                self.mapa_colaboraciones[i][j]+=1

        self.make_bidiretional()

    def make_bidiretional(self):
        for i in range(0,len(self.nodos)):
            for j in range(0,len(self.nodos)):
                self.mapa_colaboraciones[i][j]+=self.mapa_colaboraciones[j][i]
    
    def parse(self,text):
        return text

    def generate_graph(self,file):
        f=open(file,"w", encoding="UTF-8")
        f.write("digraph G{\n")
        for i in range(0,len(self.nodos)):
            f.write('  "'+self.parse(self.nodos[i].get_name()+'"'+"->{"))
            first=True
            for j in range(i,len(self.nodos)):
                if(self.mapa_colaboraciones[i][j]>0):
                    if(first):
                        f.write('  "'+self.parse(self.nodos[j].get_name())+'"')
                        first=False
                    else:
                        f.write(","+'  "'+self.parse(self.nodos[j].get_name())+'"')
            f.write('}[arrowhead="none"]\n')
            
        f.write('}')
        f.close()

    def generate_graph_author(self,author,file):
        i=self.extract_position(author)
        f=open(file,"w", encoding="UTF-8")
        f.write("digraph G{\n")
        f.write('  "'+self.parse(self.nodos[i].get_name()+'"'+"->{"))
        first=True
        for j in range(0,len(self.nodos)):
            if(self.mapa_colaboraciones[i][j]>0):
                if(first):
                    f.write('  "'+self.parse(self.nodos[j].get_name())+'"')
                    first=False
                else:
                    f.write(","+'"'+self.parse(self.nodos[j].get_name())+'"')
        f.write('}[arrowhead="none"]\n')
            
        f.write('}')
        f.close()






