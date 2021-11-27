from os import listdir
from os.path import join

from graph import Graph

if __name__ == '__main__':
    for file in listdir('input'):
        graph = Graph.read_from_file(join('input', file))
        print(graph)
