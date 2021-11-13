import numpy as np

class Grafo:
    def __init__(self, list_authors):
        list_authors.sort()
        self.nodos = list_authors
        self.mapa_colaboraciones = np.zeros((len(self.nodos),len(self.nodos)),int)

    def extract_position(self,name):
        for i,author in enumerate(self.nodos):
            if author == name:
                return i

    def map_authors(self, documents):
        for document in documents:
            for a1 in document.Authors:
                i = self.extract_position(a1)
                for a2 in document.Authors:
                    j = self.extract_position(a2)
                    if i != j:
                        self.mapa_colaboraciones[i,j] += 1
    
    def generate_graph(self,file):
        f=open(file,"w", encoding="UTF-8")
        f.write("digraph G{\n")
        for i in range(0,len(self.nodos)):
            f.write('"'+str(self.nodos[i])+'"'+"->{")
            first=True
            for j in range(i,len(self.nodos)):
                if(self.mapa_colaboraciones[i][j]>0):
                    if(first):
                        f.write('"'+str(self.nodos[j])+'"')
                        first=False
                    else:
                        f.write(","+'"'+str(self.nodos[j])+'"')
            f.write('}[arrowhead="none"]\n')
            
        f.write('}')
        f.close()

    def generate_graph_author(self,author,file):
        i=self.extract_position(author)
        f=open(file,"w", encoding="UTF-8")
        f.write("digraph G{\n")
        for j in range(0,len(self.nodos)):
            if(self.mapa_colaboraciones[i][j]>0):
                f.write('"'+str(self.nodos[i])+'"'+"->")
                f.write(f'"{self.nodos[j]}"'+f'[ label = "{self.mapa_colaboraciones[i][j]}", arrowhead="none"]\n')
           
        f.write('}')
        f.close()






