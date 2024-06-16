import sklearn.preprocessing
import numpy as np
import networkx as nx
import itertools
# load graph from movie_edges and movie_nodes
# create a subgraph of the giant connected component
# calculate the pagerank

with open('movie_nodes.txt', 'r', encoding='utf8') as f:
    nodes = f.readlines()
#Find a normalized success score for each movie
#Normalize the revenue, budget, and rating 
#to be between 0 and 1
scaler = sklearn.preprocessing.MinMaxScaler()

for node_str in nodes:
    # Evaluate the node string
    node = eval(node_str)
    # Print the movie title
    
    # Extract revenue, budget, and rating from the node dictionary
    revenue = node[1]["revenue"]
    budget = node[1]["budget"]
    rating = node[1]["rating"]
    
    # Print revenue, budget, and rating

# Make NumPy arrays of revenue, budget, and rating
revenues = np.array([eval(node_str)[1]["revenue"] for node_str in nodes])
budgets = np.array([eval(node_str)[1]["budget"] for node_str in nodes])
ratings = np.array([eval(node_str)[1]["rating"] for node_str in nodes])
profits = revenues - budgets

profits = profits.reshape(-1, 1)
ratings = ratings.reshape(-1, 1)

normalized_profits = scaler.fit_transform(profits)
normalized_ratings = scaler.fit_transform(ratings)

#calculate the normalized success score
success_score = ((0.5 * normalized_profits) + (0.5 * normalized_ratings)) * (10)# print each movies with their success score
for i, node_str in enumerate(nodes):
    node = eval(node_str)
    # print(node[0], success_score[i][0])

# print top 10 movies with the highest success score
sorted_indices = np.argsort(success_score, axis=0)[::-1]
for i in range(10):
    node = eval(nodes[sorted_indices[i][0]])
#print the worst 10 movies with the lowest success score
for i in range(10):
    node = eval(nodes[sorted_indices[-i-1][0]])

# print to file nodes with success score
with open('movie_nodes_with_scores.txt', 'w', encoding='utf8') as f:
    for i, node_str in enumerate(nodes):
        node = eval(node_str)
        # Write the node to the file with each name having quotations and the success score
        f.write(f'"{node[0]}"={success_score[i][0]}\n')

#write top 10 movies with success score to file
with open('top50_movies_with_scores.txt', 'w', encoding='utf8') as f:
    for i in range(50):
        node = eval(nodes[sorted_indices[i][0]])
        f.write(f'"{node[0]}"={success_score[sorted_indices[i][0]][0]}\n')
# Create graph with nodes having the success score as a node attribute
movie_graph_with_scores = nx.Graph()
for i, node_str in enumerate(nodes):
    node = eval(node_str)
    movie_graph_with_scores.add_node(node[0], success_score=success_score[i][0])
print(len(movie_graph_with_scores.nodes(data=True)))
# Add edges to the graph
with open('movie_edges.txt', 'r', encoding='utf8') as f:
    edges = f.readlines()
for edge_str in edges:
    edge = edge_str.strip().split('=')
    node1 = edge[0].strip()
    node2 = edge[1].strip()
    weight = int(edge[2].strip())
    if movie_graph_with_scores.has_node(node1) and movie_graph_with_scores.has_node(node2):
        movie_graph_with_scores.add_edge(node1, node2, weight=weight)
    else:
        print(f"Edge skipped, one of the nodes not found: {node1}, {node2}")
print(len(movie_graph_with_scores.nodes(data=True)), len(movie_graph_with_scores.edges(data=True)))

# Calculate the PageRank of the graph with the success score as the personalization vector
page_rank = nx.pagerank(movie_graph_with_scores, personalization=nx.get_node_attributes(movie_graph_with_scores, 'success_score'),weight='weight')
# print top 10 movies with the highest PageRank
sorted_page_rank = sorted(page_rank.items(), key=lambda x: x[1], reverse=True)
#Write pagerank to file

#Calculate degree centrality with weights
degree_centrality = nx.degree_centrality(movie_graph_with_scores)
# print top 10 movies with the highest degree centrality
sorted_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
# write degree centrality to file
with open('movies_degree_centrality.txt', 'w', encoding='utf8') as f:
    for movie, centrality in sorted_degree_centrality:
        f.write(f'{movie}={centrality}\n')
# write top10 degree centrality to file
with open('top50_movies_degree_centrality.txt', 'w', encoding='utf8') as f:
    for movie, centrality in sorted_degree_centrality[:50]:
        f.write(f'{movie}={centrality}\n')


with open('movies_pagerank.txt', 'w', encoding='utf8') as f:
    for movie, rank in sorted_page_rank:
        f.write(f'{movie}={rank}\n')
# write top10 pagerank to file
with open('top50_movies_pagerank.txt', 'w', encoding='utf8') as f:
    for movie, rank in sorted_page_rank[:50]:
        f.write(f'{movie}={rank}\n')

#Find the common movies among the top 25 movies with the highest PageRank and the top 25 movies with the highest degree centrality and the top 25 movies with the highest success score
top25_page_rank = [movie for movie, rank in sorted_page_rank[:30]]
top25_degree_centrality = [movie for movie, centrality in sorted_degree_centrality[:20]]
#Get movies and success score from graph
success_score = nx.get_node_attributes(movie_graph_with_scores, 'success_score')
top25_success_score = [movie for movie, score in sorted(success_score.items(), key=lambda x: x[1], reverse=True)[:20]]
common_movies = set(top25_page_rank).intersection(top25_degree_centrality).intersection(top25_success_score)
# print the common movies


# print nodes and edges length comp = girvan_newman(movie_graph_with_scores)
communities = nx.community.louvain_communities(movie_graph_with_scores, weight='weight', resolution=1, threshold=1e-07, max_level=None, seed=None)

# Sort communities by size in descending order
sorted_communities = sorted(communities, key=len, reverse=True)

# Write the sorted communities to a file
with open('movie_communities.txt', 'w', encoding='utf8') as f:
    for i, community in enumerate(sorted_communities):
        f.write(f'Community {i+1}:\n')
        f.write(f'{len(community)} movies\n')
        f.write(f'{sorted(community)}\n\n')