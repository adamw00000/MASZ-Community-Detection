# %%
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import time
from copy import deepcopy

def test(G_orig, number_of_clusters, clusters):
    G = deepcopy(G_orig)
    start = time.time()
    pos = nx.spring_layout(G)
    # print(len(G.edges))
    number_of_current_clusters = nx.number_connected_components(G)
    plt.figure()
    nx.draw(G_orig, pos=pos, node_color=clusters)
    plt.title('Correct labels')
    plt.show()
    k = len(G.nodes)
    if len(G.edges) > 1000:
        k = round(len(G.nodes) * 0.1)
    while number_of_current_clusters < number_of_clusters:
        # if len(G.edges) % 10 == 0:
            # print(len(G.edges))
            # print(number_of_current_clusters)
            #plt.figure()
            #nx.draw(G, pos=pos)
            #plt.show()
        edge_centrality = nx.edge_betweenness(G, k)
        u, v = max(edge_centrality, key=lambda key: edge_centrality[key])
        G.remove_edge(u, v)
        number_of_current_clusters = nx.number_connected_components(G)
    # print(len(G.edges))
    # print(number_of_current_clusters)

    res = [c for c in nx.connected_components(G)]
    our_clusters = []
    for node in G.nodes:
        for i in range(len(res)):
            if node in res[i]:
                our_clusters.append(i)
                break
    # print(our_clusters)
    plt.cla()
    plt.title('Clustering result')
    nx.draw(G_orig, pos=pos, node_color=our_clusters)
    plt.show()
    end = time.time()
    # print(end - start)
    return G

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
## Edge betweenness

# %%
G, clusters = gen_communityER(400, 0.5, 0.05, 8)
A = nx.karate_club_graph()
A_clusters = [0 for x in A.nodes]
test(A, 2, A_clusters)

# %%
N = 100
p_inside = 0.5
p_outside = 0.05
n_clusters = 4
G, clusters = gen_communityER(N, p_inside, p_outside, n_clusters)
test(G, len(np.unique(clusters)), clusters)

# %%
N = 48
p_inside = 0.5
p_outside = 0.2
n_clusters = 4
G, clusters = gen_communityER(N, p_inside, p_outside, n_clusters)
test(G, len(np.unique(clusters)), clusters)

# %%
