import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import seaborn as sns

def load_data(file_path):
    """Load the graph data from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def build_graph(data):
    """Construct a NetworkX graph from the dataset."""
    G = nx.Graph()
    
    # Add nodes (notes)
    for note in data['notes']:
        G.add_node(note, path=data['notes'][note])
    
    # Add edges (links)
    for src, targets in data['links'].items():
        for tgt in targets:
            G.add_edge(src, tgt)
    
    return G

def compute_centrality(G):
    """Compute centrality metrics for graph nodes."""
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
    
    return {
        "degree": degree_centrality,
        "betweenness": betweenness_centrality,
        "eigenvector": eigenvector_centrality,
    }

def find_clusters(G):
    """Detect clusters using the Louvain method (if available) or connected components."""
    try:
        import community as community_louvain
        partition = community_louvain.best_partition(G)
        return partition
    except ImportError:
        return list(nx.connected_components(G))

def tag_cooccurrence_analysis(data):
    """Find notes that share multiple tags to infer hidden relationships."""
    tag_map = defaultdict(set)
    for tag, notes in data['tags'].items():
        for note in notes:
            tag_map[note].add(tag)
    
    cooccurrence = defaultdict(lambda: defaultdict(int))
    notes = list(tag_map.keys())
    
    for i, note1 in enumerate(notes):
        for j in range(i + 1, len(notes)):
            note2 = notes[j]
            common_tags = tag_map[note1] & tag_map[note2]
            if common_tags:
                cooccurrence[note1][note2] = len(common_tags)
                cooccurrence[note2][note1] = len(common_tags)
    
    return cooccurrence

def visualize_graph(G):
    """Visualize the graph with Matplotlib."""
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10)
    plt.title("Graph Visualization")
    plt.show()

def plot_cooccurrence(cooccurrence):

    notes = list(cooccurrence.keys())
    matrix = np.zeros((len(notes), len(notes)))

    for i, note in enumerate(notes):
        for j, related_note in enumerate(notes):
            matrix[i, j] = cooccurrence[note].get(related_note, 0)

    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, xticklabels=notes, yticklabels=notes, cmap="coolwarm", annot=True)
    plt.title("Tag Co-occurrence Heatmap")
    plt.show()

def plot_centrality(centrality):
    """
    Plots bar charts for different centrality measures.
    """
    sns.set(style="whitegrid")  # Set a clean style for Seaborn
    for metric, scores in centrality.items():
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        nodes, values = zip(*sorted_scores)  # Extract names & values

        plt.figure(figsize=(10, 5))
        sns.barplot(x=list(nodes), y=list(values), palette="viridis")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel(metric.capitalize())
        plt.xlabel("Notes")
        plt.title(f"{metric.capitalize()} Centrality")
        plt.show()


def analyse(file_path, flag):
    data = load_data(file_path)
    G = build_graph(data)
    
    centrality = compute_centrality(G)
    clusters = find_clusters(G)
    cooccurrence = tag_cooccurrence_analysis(data)
    
   


    if flag == "hmap":
        plot_cooccurrence(tag_cooccurrence_analysis(data))
        print("\nTag Co-occurrence Analysis:")
        for note, related in cooccurrence.items():
            print(f"  {note} -> {dict(related)}")
    elif flag == "cen":
        plot_centrality(centrality)
    elif flag == "viz":
        visualize_graph(G)