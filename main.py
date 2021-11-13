from libs.objects import create_objects
from libs.functions import listToString
from libs.grafo import Grafo
from libs.html_indexer import write_to_file, write_document
import graphviz
import sys,getopt
import os

OUT_PATH = 'output_files/'
DOT_PATH = OUT_PATH+'dot/'
GRAPH_PATH = OUT_PATH+'graph/'

HELP = 'main.py <Runs everything>\n\
        -A "authors name" <Shows every publication by that author>\n\
        -C "authors name" <Shows every colaborator by that author>\n\
        -G <Shows the graph of every author and their colaborators>\n\
        -G "authors name" <Shows the graph of that author and his/hers colaborators>\n\
        -H <Prints Help>\n\
        -E <Writes html file for exercise 1>\n\
        -e <Writes html file for exercise 2>\n\
        -B <Shows every author>'


if __name__ == '__main__':
    DOCUMENTS,dic_authors,dic_categories = create_objects()

    if not os.path.exists(OUT_PATH):
        os.mkdir(OUT_PATH)

    if not os.path.exists(DOT_PATH):
        os.mkdir(DOT_PATH)

    if not os.path.exists(GRAPH_PATH):
        os.mkdir(GRAPH_PATH)

    if len(sys.argv) > 1:
        opts, args = getopt.getopt(sys.argv[1:],"A,C,G,D,H,E,e,B")
        for opt,arg in opts:
            if opt == '-A':
                    dic_authors[listToString(args)].print_author()
            if opt == '-C':
                    dic_authors[listToString(args)].print_colaborators()
            if opt == '-G':
                grafo=Grafo()
                grafo.load_names(list(dic_authors.values()))
                grafo.map_authors()
                if len(args) == 0:
                    FILE_GRAPH = "authors_colaborations"
                    grafo.generate_graph(DOT_PATH+FILE_GRAPH+".dot")
                    total_graph = graphviz.Source.from_file(DOT_PATH+FILE_GRAPH+".dot")
                    total_graph.render(GRAPH_PATH+FILE_GRAPH,view = True)
                    os.remove(GRAPH_PATH+FILE_GRAPH)
                elif len(args) == 1:
                    FILE_GRAPH = listToString(args)
                    grafo.generate_graph_author(dic_authors[listToString(args)],DOT_PATH+FILE_GRAPH+".dot")
                    author_graph = graphviz.Source.from_file(DOT_PATH+FILE_GRAPH+".dot")
                    author_graph.render(GRAPH_PATH+FILE_GRAPH,view = True)
                    os.remove(GRAPH_PATH+FILE_GRAPH)
            if opt == '-E':
                write_document(DOCUMENTS,OUT_PATH+"exercise1.html")
            if opt == '-e':
                write_to_file(dic_categories,OUT_PATH+"exercise2.html")
            if opt == '-H':
                print(HELP)
            if opt == '-B':
                for a in dic_authors:
                    print(dic_authors[a].get_name())
    else:
        write_to_file(dic_categories,OUT_PATH+"exercise2.html")
        write_document(DOCUMENTS,OUT_PATH+"exercise1.html")

