# IMPORTED FROM MY OWN A* CODE:

class graph ():
    def __init__ (self, nodes):
        self.nodes = nodes

"""
    If we already know the full strucure of the graph & we dont have to explore for neighbors:
"""
class ExplicitGraphNode ():
    def __init__ (self, key, neighbors = []):
        # neighbors = [[node, cost], [node,cost], ect]  (arr of arrs)
        self.key = key
        self.neighbors = neighbors 
        # Needs to also add itself to the neighbor list for the other functions
        for neighborArr in neighbors:
            neighbor = neighborArr[0]
            cost = neighborArr[1]
            neighbor.addNewNeighbor([self, cost])

    def addNewNeighbor (self, neighbor):
        self.neighbors.append(neighbor)

    # Defines how two nodes should be compared with (<) - Needed to break ties
    def __lt__(self, other):
        return self.key < other.key 

    def __repr__  (self):
        return self.key

    # def generateNeighbors (self, neighborFunction):
    #     neighbors = neighborFunction(self.stateValue) # list of graph nodes that they might be neighbors with
    #     for neighbor in neighbors:
            
        
"""
    If the graph is huge and we dont know the full structure (we need to discover the graph )
"""
class ImplicitGraphNode ():
    def __init__ (self, key, stateValue, discoveryFunction, neighbors = []):
        """
            key = unique identifier str,
            stateValue 
            neighbors = [[node, cost], [node,cost], ect]  (arr of arrs)
            neighbors are here so it doesnt have to re-explore for neighbors it already knows it has (usually whatever node found it)
        """
        # Used to define the node state space
        self.stateValue = stateValue

        self.key = key
        self.neighbors = neighbors 
        self.discoveryFunction = discoveryFunction#(self,neighbors) # Function that takes in the node and produces (new) neighbors

    # General discover function 
    def discover (self):
        newNeighbors = self.discoveryFunction (self, self.neighbors)  
        # Each neighbor must be [node, cost] for the relationship
        # It must discard neighobrs that already exist
        for neighbor in newNeighbors:
            # neighbor = [neighborNode,cost]
            self.neighbors.append(neighbor)
        
    # Defines how two nodes should be compared with (<) - Needed to break ties
    def __lt__(self, other):
        return self.key < other.key 

    def __repr__  (self):
        return self.key