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
title = G.graph['title']
nodes = nx.descendants(G, title)
nodes.add(title)
H = G.subgraph(nodes).copy()
name = 'graf' + title
extension = '.gpickle'
nx.write_gpickle(H, name + extension)
edge_labels = nx.get_edge_attributes(H, 'id')
edge_labels1 = nx.get_edge_attributes(H, 'resposta')
edge_colors = ['blue' if e in edge_labels else 'green' if e in edge_labels1 else 'black' for e in H.edges]
nx.draw_circular(H, with_labels=True, edge_color=edge_colors, node_size=600)
nx.draw_networkx_edge_labels(H, pos=nx.circular_layout(H), edge_labels=edge_labels, font_color='blue')
nx.draw_networkx_edge_labels(H, pos=nx.circular_layout(H), edge_labels=edge_labels1, font_color='green')
plt.show()
