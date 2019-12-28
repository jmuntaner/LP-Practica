import matplotlib.pyplot as plt
import networkx as nx

path = "../Compilador/" + "grafE" + ".gpickle"
G=nx.read_gpickle(path)
enquesta = nx.get_edge_attributes(G,'type')
print(enquesta)
n = 'E'
m = n
while n != 'END':
    if G.nodes[n]['type'] == 'pregunta':
        print(G.nodes[n]['pregunta'])
        for r in G[n]:
            if G[n][r]['type'] == 'item':
                print(G.nodes[r]['res'])

    # Continua l'enquesta
    for e in G[n]:
        if G[n][e]['type'] == 'enquesta':
            m = e
        elif G[n][e]['type'] == 'alternativa':
            print(G[n][e]['resposta'])
            if G.nodes[e]['type'] == 'pregunta':
                print(G.nodes[e]['pregunta'])
                for r in G[e]:
                    if G[e][r]['type'] == 'item':
                        print(G.nodes[r]['res'])
    # fi
    n = m
