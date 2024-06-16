import networkx as nx
import csv
import matplotlib.pyplot as plt
import sklearn.preprocessing 

# Create an undirected weighted graph of all the films

with open('top_rated_movies.csv', 'r', encoding="utf8") as f:
    films = list(csv.reader(f))
#remove films where budget or revenue is 0
films = [film for film in films if film[1] != '$0'] 
films = [film for film in films if film[6] != '$0']

movie_graph = nx.Graph()
for film in films:
    if film[0] != 'Title':
        # calculate the weight of the node based on the (revenue / budget) + rating
        revenue = int(film[6].replace('$', '').replace(',', ''))
        budget = int(film[1].replace('$', '').replace(',', ''))
        rating = float(film[5])
        movie_graph.add_node(film[0], revenue=revenue, budget=budget, rating=rating)
# make weighted edges between films that share an actor
for i in range(1,len(films)):
    for j in range(i + 1, len(films)):
        # Normalize actor names by stripping whitespace and converting to lowercase
        actors_i = set(actor.strip().lower() for actor in films[i][3][1:-1].split(','))
        actors_j = set(actor.strip().lower() for actor in films[j][3][1:-1].split(','))

        genres_i = set(genre.strip().lower() for genre in films[i][2][1:-1].split(','))
        genres_j = set(genre.strip().lower() for genre in films[j][2][1:-1].split(','))

        production_companies_i = set(company.strip().lower() for company in films[i][6][1:-1].split(','))
        production_companies_j = set(company.strip().lower() for company in films[j][6][1:-1].split(','))
        # Find common actors
        common_actors = actors_i.intersection(actors_j)

        # Find common production companies
        common_production_companies = production_companies_i.intersection(production_companies_j)
        # Add an edge if there are common actors
        if len(common_actors) >= 2:
            movie_graph.add_edge(films[i][0], films[j][0], weight=(len(common_actors)*2+len(common_production_companies)))
#write nodes and edges to files
nx.write_edgelist(movie_graph, 'movie_edges.txt', delimiter='=', data=['weight'])
# write nodes to file
with open('movie_nodes.txt', 'w', encoding='utf8') as f:
    for node in movie_graph.nodes(data=True):
        f.write(str(list(node))+'\n')
# visualize the graph
# pos = nx.spring_layout(movie_graph)
# plt.figure(figsize=(12, 12))
# nx.draw_networkx_nodes(movie_graph, pos, node_size=100)
# nx.draw_networkx_edges(movie_graph, pos, alpha=0.5)
# nx.draw_networkx_labels(movie_graph, pos)
# plt.axis('off')
# plt.show()
