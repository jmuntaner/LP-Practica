import sys
from antlr4 import *
from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from antlr4.InputStream import InputStream
from EnquestesVisitor import EnquestesVisitor
import matplotlib.pyplot as plt
import networkx as nx
if len(sys.argv) > 1:
    input_stream = FileStream(sys.argv[1])
else:
    input_stream = InputStream(input('? '))
lexer = EnquestesLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = EnquestesParser(token_stream)
tree = parser.root()
# print(tree.toStringTree(recog=parser))

visitor = EnquestesVisitor()
visitor.visit(tree)

G = visitor.getGraph().copy()
name = 'graf' + G.graph['title']
extension = '.gpickle'
nx.write_gpickle(G,name + extension)
# G=nx.read_gpickle("grafE.pickle")
edge_labels = nx.get_edge_attributes(G,'id')
edge_labels1 = nx.get_edge_attributes(G,'resposta')
edge_colors = ['blue' if e in edge_labels else 'green' if e in edge_labels1 else 'black' for e in G.edges]
nx.draw_circular(G, with_labels=True, edge_color = edge_colors, node_size=600)
nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G), edge_labels=edge_labels, font_color='blue')
nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G), edge_labels=edge_labels1, font_color='green')
# plt.show()
