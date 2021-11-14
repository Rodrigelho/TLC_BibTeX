from libs.functions import listToString
from libs.grafo import Grafo
from libs.html_indexer import convert2HTML,write_document,write_file
from libs.objects import save_objects, open_objects
import graphviz
import sys,getopt
import os

INPUT_PATH = 'input_files/'
FILENAME = 'exemplo-utf8.bib'
LIBRARY_PATH = 'library/'
OUT_PATH = 'output_files/'
DOT_PATH = OUT_PATH+'dot/'
GRAPH_PATH = OUT_PATH+'graph/'

HELP = '-A <Prints every author and their publications>\n\
        -A "authors name" <Prints every publication by that author>\n\
        -C "authors name" <Prints every colaborator by that author>\n\
        -G < Creates dot file and shows the graph of every author and their colaborators>\n\
        -G "authors name" <Creates dot file and shows the graph of that author and his/hers colaborators>\n\
        -H <Prints Help>\n\
        -E <Writes html file for exercise 1>\n\
        -B <Prints every author>\n\
        -R "FileName.bib" <Reads the bib file and make the Objects>'


if __name__ == '__main__':
    if not os.path.exists(LIBRARY_PATH):
        os.mkdir(LIBRARY_PATH)
        save_objects(INPUT_PATH,FILENAME)

    if not os.path.exists(OUT_PATH):
        os.mkdir(OUT_PATH)

    if not os.path.exists(DOT_PATH):
        os.mkdir(DOT_PATH)

    if not os.path.exists(GRAPH_PATH):
        os.mkdir(GRAPH_PATH)

    if len(sys.argv) > 1:
        opts, args = getopt.getopt(sys.argv[1:],"A,C,G,D,H,E,B,R")
        for opt,arg in opts:
            if opt == '-R':
                if len(args) == 1:
                    save_objects(INPUT_PATH,listToString(args))
                if len(args) == 0:
                    save_objects(INPUT_PATH,FILENAME)
            if opt == '-A':
                dic_authors = open_objects('authors')
                if len(args) == 1:
                    try:
                        dic_authors[listToString(args)].print_author()
                    except KeyError:
                        print('O autor inserido nao e valido')
                elif len(args) == 0:
                    for author in dic_authors:
                        dic_authors[author].print_author()
                else:
                    opt = '-H'
            if opt == '-C':
                dic_authors = open_objects('authors')
                if len(args) == 1:
                    try:
                        dic_authors[listToString(args)].print_colaborators()
                    except KeyError:
                        print('O autor inserido nao e valido')
                else:
                    opt = '-H'
            if opt == '-G':
                dic_authors = open_objects('authors')
                dic_documents = open_objects('documents')
                docs = list(dic_documents.keys())
                docs.sort()
                DOCUMENTS = []
                for key in docs:
                    DOCUMENTS.append(dic_documents[key])
                grafo=Grafo(list(dic_authors.keys()))
                grafo.map_authors(DOCUMENTS)
                if len(args) == 0:
                    FILE_GRAPH = "authors_colaborations"
                    grafo.generate_graph(DOT_PATH+FILE_GRAPH+".dot")
                    total_graph = graphviz.Source.from_file(DOT_PATH+FILE_GRAPH+".dot")
                    total_graph.render(GRAPH_PATH+FILE_GRAPH,view = True)
                    os.remove(GRAPH_PATH+FILE_GRAPH)
                elif len(args) == 1:
                    FILE_GRAPH = listToString(args)
                    grafo.generate_graph_author(listToString(args),DOT_PATH+FILE_GRAPH+".dot")
                    author_graph = graphviz.Source.from_file(DOT_PATH+FILE_GRAPH+".dot")
                    author_graph.render(GRAPH_PATH+FILE_GRAPH,view = True)
                    os.remove(GRAPH_PATH+FILE_GRAPH)
                else:
                    opt = '-H'
            if opt == '-E':
                dic_categories = open_objects('categories')
                dic_documents = open_objects('documents')
                docs = list(dic_documents.keys())
                docs.sort()
                DOCUMENTS = []
                for key in docs:
                    DOCUMENTS.append(dic_documents[key])
                TEXT = convert2HTML(dic_categories)+"\n<h1 align=\"center\">Documentos</h1></br>\n"+write_document(DOCUMENTS)
                write_file(TEXT,OUT_PATH+'index.html')
            if opt == '-H':
                print(HELP)
            if opt == '-B':
                dic_authors = open_objects('authors')
                list_authors = list(dic_authors.keys())
                list_authors.sort()
                for a in list_authors:
                    print(dic_authors[a].get_name())
