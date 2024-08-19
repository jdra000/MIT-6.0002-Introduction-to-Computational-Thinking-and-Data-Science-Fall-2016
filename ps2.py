# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings with dijikstra
#

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: 
# - Nodes represent each builing in the map
# - Edges represent the connection between one or more buildings
# - Distances represent the time we need to move from point a to point b

# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs an adj graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        an adj list representing the map
    """

    # TODO
    print("Loading map from file...")
    # range(77) cause it is the biggest number of a builing in the map
    adj = {k: [] for k in range(77)}
    with open(map_filename) as file:
        read_data = file.read().split('\n')
        read_data = read_data[:-1]
        
        for entry in read_data:
            raw_data = entry.split(" ") # [32, 36, 70, 0]
    
            src = int(raw_data[0]) # source node
            dest = int(raw_data[1]) # neighbour of that node
            weight = int(raw_data[2]) # total time qty 
            outdoor = int(raw_data[3]) # outdoor walk qty
            
            adj[src].append([dest,weight,outdoor])
            
    return adj

# adj with the form {0: [], 1: [[2, 75, 60], [4, 80, 65], [3, 36, 0], [5, 32, 0]],

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

# graph = load_map("mit_map.txt")
# print(graph)

#
# Problem 3: Finding the Shorest Path 
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
# 
# Answer:
# - The objective function is to find the shortest path either we are using constraints
# or not.
# - The constraints are max time walking outdoor and max time walking total.


# Problem 3b: Implement shortest_path
import heapq
def shortest_path(adj, start, max_out = None):
    """
    Finds the shortest distance to each node from starting node

    Parameters:
        adj: graph instance
            The graph on which to carry out the search.
        start: int
            Building number at which to start.
        max_out: int
            Maximum distance spent outdoors on a path.

    Returns:
        A dict called 'dist' where we save the shortest distance to each node
        from starting node.
    """
    # TODO
    # Initialize the values of all nodes with infinity
    dist = {node: float('inf') for node in adj.keys()}
    dist[start] = 0 # Set the source value to 0
    
    pq = []
    # Adds an element to the queue with its associated priority.
    heapq.heappush(pq, (0, start))
    
    visited = set()
    
    while pq:
        # We take out the distance-node tuple with the min distance
        current_distance, current_node = heapq.heappop(pq)
        # varibale to measure oudoor time 
        out_acum = 0
        
        if current_node in visited:
            continue
        visited.add(current_node)
        
        for l in adj[current_node]:
            neighbour = l[0]
            weight = l[1]
            out = l[2]
            # Calculate the distance from current_node to the neighbor
            tentative_distance = current_distance + weight
            
            # 1. Case (substraint outdoors)
            if max_out != None:
                    
                tentative_out = out_acum + out
                
                if tentative_distance < dist[neighbour] and tentative_out <= max_out:
                    dist[neighbour] = tentative_distance
                    out_acum += out
                    
                    # push that to q
                    heapq.heappush(pq, (tentative_distance, neighbour))
            
            # 2. Case (no substraint)          
            else:
                if tentative_distance < dist[neighbour]:
                    dist[neighbour] = tentative_distance
                    
                    # push that to q
                    heapq.heappush(pq, (tentative_distance, neighbour))
                
    predecessors = {node: None for node in graph.keys()}
    
    # dist looks like this
    # The distance to each node
    # {0: inf, 1: 75, 2: 0, 3: 70, 4: 36, 5: 107, 6: 41 ...
    
    for node, distance in dist.items():
        for l in adj[node]:
            neighbour = l[0]
            weight = l[1]
            # Here we track the predecessor of each node
            if dist[neighbour] == distance + weight:
                predecessors[neighbour] = node
                
    return predecessors
    # predecessors looks like this
    # {0: None, 1: None, 2: 1, 3: 1, 4: 1, 5: 1, 6: 2 ...


def get_best_path(adj, starting_node: int, target_node: int, max_out = None):
    '''
    Reconstruct the shortes path starting from target_node.
    
    Parameters:
        adj: graph instance
            The graph on which to carry out the search.
        starting_node: int
            Building number at which to start.
        target_node: int
            Building number at which to arrive.
        max_out: int
            Maximum distance spent outdoors on a path.
            
    Returns:
       A list containing the shortest path represented by numbers.
    '''
    
    # Generate the predecessors dict
    predecessors = shortest_path(adj, starting_node, max_out)
    
    path = []
    current_node = target_node
    
    while current_node:
        path.append(str(current_node))
        # At the end the predecessors[B] will be none and we will exit the loop
        current_node = predecessors[current_node]
        
    path.reverse()
    
    return path

# TESTING:

graph = load_map('mit_map.txt')

# Shortest path from Building 2 to 9 
# Expected:  ['2', '3', '7', '9']
print(get_best_path(graph, 2, 9))

# Shortest path from Building 1 to 32 
# Expected:  ['1', '4', '12', '32']
print(get_best_path(graph, 1, 32))

# Shortest path from Building 2 to 9 without walking more than 0m outdoors
# Expected:  ['2', '4', '10', '13', '9']
print(get_best_path(graph, 2, 9, 0))

# Shortest path from Building 1 to 32 without walking more than 0m outdoors
# Expected:  ['1', '3', '10', '4', '12', '24', '34', '36', '32']
print(get_best_path(graph, 1, 32, 0))

# Shortest path from Building 32 to 56 without walking more than 0m outdoors
# Expected:  ['32', '36', '26', '16', '56']
print(get_best_path(graph, 32, 56, 0))

# Shortest path from Building 32 to 56 
# Expected:  ['32', '56']
print(get_best_path(graph, 32, 56))

# ================================================================

