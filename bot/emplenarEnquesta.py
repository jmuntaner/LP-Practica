import pickle

# Genera dades per EnquestaPlena
data = {'P1': {2: 6, 1: 5, 0: 1, 3: 0}, 'P2': {0: 1, 1: 9, 2: 1, 3: 1}, 'P3': {1: 5, 2: 1, 3: 6}, 'P4': {1: 1, 2: 0}, 'P5': {1: 0, 2: 2, 3: 0, 4: 1}}
with open('respostesEnquestaPlena.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
