from libs.objects import create_objects,Author,Document
from libs.functions import listToString
from libs.grafo import Grafo
from libs.html_indexer import write_to_file, write_document
import graphviz
import sys,getopt

PATH = 'input_files/'
OUT_PATH = 'output_files/'
FILENAME = 'exemplo-utf8.bib'
FILE = PATH+FILENAME

HELP = 'main.py <Runs everything>\n\
        -A "authors name" <Shows every publication by that author>\n\
        -G <Shows the graph of every author and their colaborators>\n\
        -G "authors name" <Shows the graph of that author and his/hers colaborators>\n\
        -H <Prints Help>\n\
        -E <Writes html file for exercise 1>\n\
        -e <Writes html file for exercise 2>'


if __name__ == '__main__':
    DOCUMENTS,dic_authors,dic_categories = create_objects()

    if len(sys.argv) > 1:
        opts, args = getopt.getopt(sys.argv[1:],"A,G,D,H,E,e")
        for opt,arg in opts:
            if opt == '-A':
                    try:
                        dic_authors[listToString(args)].print_author()
                    except:
                        continue
            if opt == '-G':
                if len(args) == 0:
                    grafo=Grafo()
                    grafo.load_names(list(dic_authors.values()))
                    grafo.map_authors()
                    grafo.generate_graph(OUT_PATH+"authors_colaborations.dot")
                    total_graph = graphviz.Source.from_file(OUT_PATH+"authors_colaborations.dot")
                    total_graph.render(OUT_PATH+'authors_colaborations.dot',view = True)
                elif len(args) == 1:
                    grafo=Grafo()
                    grafo.load_names(list(dic_authors.values()))
                    grafo.map_authors()
                    grafo.generate_graph_author(dic_authors[listToString(args)],OUT_PATH+"author_colaboration.dot")
                    author_graph = graphviz.Source.from_file(OUT_PATH+"author_colaboration.dot")
                    author_graph.render(OUT_PATH+'author_colaboration.dot',view = True)
            if opt == '-H':
                    print(HELP)
    else:
        write_to_file(dic_categories,OUT_PATH+"exercise2.html")
        write_document(DOCUMENTS,OUT_PATH+"exercise1.html")

        grafo=Grafo()
        grafo.load_names(list(dic_authors.values()))
        grafo.map_authors()
        grafo.generate_graph(OUT_PATH+"authors_colaborations.dot")
        grafo.generate_graph_author(dic_authors['Pedro Rangel Henriques'],OUT_PATH+"author_colaboration.dot")
        
        total_graph = graphviz.Source.from_file(OUT_PATH+"authors_colaborations.dot")
        total_graph.render(OUT_PATH+'authors_colaborations.gv',view = True)
        author_graph = graphviz.Source.from_file(OUT_PATH+"author_colaboration.dot")
        author_graph.render(OUT_PATH+'author_colaboration.gv',view = True)
