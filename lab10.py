# %%
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

def perform_clustering(G, clusters):
    n_clusters = len(np.unique(clusters))
    nodes = G.nodes()
    distances = np.zeros((len(nodes), len(nodes)))

    i = 0
    for n1 in nodes:
        j = 0
        for n2 in nodes:
            if n1 == n2:
                continue

            distances[i, j] = nx.shortest_path_length(G, n1, n2)
            j += 1
        i += 1

    import genieclust
    g = genieclust.Genie(n_clusters=n_clusters, gini_threshold=0.3)

    labels = g.fit_predict(distances)

    pos = nx.spring_layout(G)
    nx.draw(G, pos = pos, node_color = clusters)
    plt.title('Correct labels')
    plt.show()

    nx.draw(G, pos = pos, node_color = labels)
    plt.title('Clustering result')
    plt.show()

# %%
def gen_communityER(N, p_inside, p_outside, communities):
    community_size = N / communities

    G = nx.Graph()

    for i in range(N):
        G.add_node(i)

    for i in range(N):
        for j in range(i + 1, N):
            if i // community_size == j // community_size:
                if random.random() < p_inside:
                    G.add_edge(i, j)
            else:
                if random.random() < p_outside:
                    G.add_edge(i, j)
    
    clusters = np.repeat(np.arange(0, communities), community_size)
    return G, clusters

# %% [markdown]
## Hierarchical clustering

# %%
N = 400
p_inside = 0.5
p_outside = 0.05
n_clusters = 8
G, clusters = gen_communityER(N, p_inside, p_outside, n_clusters)
perform_clustering(G, clusters)

# %%
N = 100
p_inside = 0.5
p_outside = 0.05
n_clusters = 4
G, clusters = gen_communityER(N, p_inside, p_outside, n_clusters)
perform_clustering(G, clusters)

# %%
N = 48
p_inside = 0.5
p_outside = 0.2
n_clusters = 4
G, clusters = gen_communityER(N, p_inside, p_outside, n_clusters)
perform_clustering(G, clusters)

# %%
