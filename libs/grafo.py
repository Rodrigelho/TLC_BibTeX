import numpy 
import sys
numpy.set_printoptions(threshold=sys.maxsize)


class Grafo:
    def __init__(self):
        self.nodos=[]
        self.mapa_colaboraciones=[]

    def extract_position(self,name):
        for i in range(0,len(self.nodos)):
            if(self.nodos[i].is_samePerson(name)):
                return i
        else:
             return -1

    def load_names(self,list_autors):
        for author in list_autors:
            self.nodos.append(author)

        self.load_matrix()

    def load_matrix(self):
        self.mapa_colaboraciones=[[0 for x in range(len(self.nodos))] for y in range(len(self.nodos))] 


    def map_authors(self):
        for author in self.nodos:
            i=self.extract_position(author)
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
            f.write('"'+self.parse(self.nodos[i].get_name()+'"'+"->{"))
            first=True
            for j in range(i,len(self.nodos)):
                if(self.mapa_colaboraciones[i][j]>0):
                    if(first):
                        f.write('"'+self.parse(self.nodos[j].get_name())+'"')
                        first=False
                    else:
                        f.write(","+'"'+self.parse(self.nodos[j].get_name())+'"')
            f.write('}[arrowhead="none"]\n')
            
        f.write('}')
        f.close()

    def generate_graph_author(self,author,file):
        i=self.extract_position(author)
        f=open(file,"w", encoding="UTF-8")
        f.write("digraph G{\n")
        f.write('"'+self.parse(self.nodos[i].get_name()+'"'+"->{"))
        first=True
        for j in range(0,len(self.nodos)):
            if(self.mapa_colaboraciones[i][j]>0):
                if(first):
                    f.write('"'+self.parse(self.nodos[j].get_name())+'"')
                    first=False
                else:
                    f.write(","+'"'+self.parse(self.nodos[j].get_name())+'"')
        f.write('}[arrowhead="none"]\n')
            
        f.write('}')
        f.close()






