import sys
import random
import networkx as nx
import matplotlib.pyplot as plt
import os

# Definire un numero massimo di distanza (simile a infinito)
INFINITY = sys.maxsize

# Classe che rappresenta ogni nodo
class Node:
    def __init__(self, name, all_nodes):
        self.name = name
        self.routing_table = {}  # La tabella di routing inizialmente è vuota
        self.neighbors = {}  # Lista dei vicini e delle distanze iniziali verso di essi

        # Inizializza la tabella di routing con tutti i nodi come non raggiungibili (INFINITY)
        for node_name in all_nodes:
            if node_name != self.name:
                self.routing_table[node_name] = {'distance': INFINITY, 'next_hop': None}
    
    # Funzione per aggiungere un vicino e la distanza
    def add_neighbor(self, neighbor, distance):
        self.neighbors[neighbor.name] = distance
        self.routing_table[neighbor.name] = {'distance': distance, 'next_hop': neighbor.name}
    
    # Funzione per aggiornare la tabella di routing
    def update_routing_table(self, neighbor_table):
        updated = False
        # Ottieni il nome del vicino dalla tabella
        neighbor_name = neighbor_table['from']

        for dest, info in neighbor_table.items():
            if dest == 'from':  # Ignoriamo l'attributo 'from'
                continue
            if dest == self.name:  # Evitiamo di aggiornare se il nodo è se stesso
                continue

            # Calcola la nuova distanza
            new_distance = self.neighbors[neighbor_name] + info['distance']

            # Aggiorna la tabella di routing se troviamo un percorso più breve
            if dest not in self.routing_table or new_distance < self.routing_table[dest]['distance']:
                self.routing_table[dest] = {'distance': new_distance, 'next_hop': neighbor_name}
                updated = True
        return updated

    # Mostra la tabella di routing
    def print_routing_table(self):
        print(f"Routing table for {self.name}:")
        for dest, info in self.routing_table.items():
            distance = '∞' if info['distance'] == INFINITY else info['distance']
            next_hop = info['next_hop'] if info['next_hop'] else '-'
            print(f"  Destination: {dest}, Distance: {distance}, Next hop: {next_hop}")
        print()

# Simulazione della rete
class Network:
    def __init__(self):
        self.nodes = []
        self.graph = nx.Graph()
    
    # Aggiungere un nodo alla rete
    def add_node(self, node):
        self.nodes.append(node)
        self.graph.add_node(node.name)
    
    # Aggiungere un arco alla rete
    def add_edge(self, node1, node2, distance):
        self.graph.add_edge(node1.name, node2.name, weight=distance)
    
    # Simulare lo scambio di aggiornamenti
    def simulate(self):
        converged = False
        iteration = 0
        while not converged:
            print(f"Iteration {iteration}:")
            converged = True
            for node in self.nodes:
                for neighbor_name in node.neighbors:
                    neighbor = self.get_node_by_name(neighbor_name)
                    neighbor_table = neighbor.routing_table.copy()
                    neighbor_table['from'] = neighbor.name
                    if node.update_routing_table(neighbor_table):
                        converged = False
            iteration += 1
            self.print_all_routing_tables()

    # Trova il nodo per nome
    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    # Mostra tutte le tabelle di routing
    def print_all_routing_tables(self):
        for node in self.nodes:
            node.print_routing_table()

    # Funzione per visualizzare la rete come un grafo
    def showGraphNetwork(self):
        pos = nx.spring_layout(self.graph)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()

def createNetwork(num_nodes):
    # Creazione di nodi casuali
    random.seed(42)
    # Creare i nodi assegnando loro lettere dell'alfabeto uniche
    print(f"Creating a network with {num_nodes} nodes...")
    node_names = [chr(65 + i) for i in range(num_nodes % 26)]  # max nodes: A - Z
    nodes = {name: Node(name, node_names) for name in node_names}

    # Definire vicini e distanze casuali garantendo la connessione completa
    for i, node in enumerate(nodes.values()):
        # Ensure that node is connected to the next one, creating a basic spanning tree
        if i < len(node_names) - 1:
            neighbor_name = node_names[i + 1]
            distance = random.randint(1, 10)
            node.add_neighbor(nodes[neighbor_name], distance)
            nodes[neighbor_name].add_neighbor(node, distance)

    # Aggiungere ulteriori vicini casuali per diversificare la rete
    for node in nodes.values():
        num_neighbors = random.randint(1, len(node_names) - 1)
        neighbors = random.sample(node_names, num_neighbors)
        for neighbor_name in neighbors:
            if neighbor_name != node.name and neighbor_name not in node.neighbors:
                distance = random.randint(1, 10)
                node.add_neighbor(nodes[neighbor_name], distance)
                nodes[neighbor_name].add_neighbor(node, distance)  # Make it bidirectional

    # Creare la rete e aggiungere i nodi
    network = Network()
    for node in nodes.values():
        network.add_node(node)
        for neighbor_name, distance in node.neighbors.items():
            network.add_edge(node, nodes[neighbor_name], distance)

    # Simulare la rete
    network.simulate()

    # Disegnare la rete finale
    network.showGraphNetwork()

# Prendere il numero di nodi dagli argomenti
createNetwork(int(sys.argv[1]) if len(sys.argv) > 1 else 7)