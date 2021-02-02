# Gideon Marsh
# github.com/GideonMarsh

from random import random
from math import floor

INPUT_NODES = 3
OUTPUT_NODES = 2

'''
Nodes with innovation numbers 1 through INPUT_NODES are the input nodes
Nodes with innovation numbers 1 + INPUT_NODES through OUTPUT_NODES + INPUT_NODES are the output nodes
Nodes with any other innovation number are hidden nodes
'''

nodeCount = INPUT_NODES + OUTPUT_NODES
connectionCount = 0

class NodeGene:
    def __init__(self, innovationNumber=None):
        if (innovationNumber):
            self.inum = innovationNumber
        else:
            global nodeCount
            nodeCount = nodeCount + 1
            self.inum = nodeCount
        self.value = 0

class ConnectionGene:
    def __init__(self, inNode, outNode, weight=0, innovationNumber=None):
        if (innovationNumber):
            self.inum = innovationNumber
        else:
            global connectionCount
            connectionCount = connectionCount + 1
            self.inum = connectionCount
        self.weight = weight
        self.enabled = True
        self.inNode = inNode
        self.outNode = outNode
        self.nextConnection = None

    def addNewConnection(self, newConnection):
        if (self.nextConnection == None):
            self.nextConnection = newConnection
        else:
            self.nextConnection.addNewConnection(newConnection)

    def calculateValue(self, nodes, futureNodes):
        if (self.enabled):
            nodes[self.outNode].value = nodes[self.outNode].value + nodes[self.inNode].value * self.weight
        futureNodes.append(self.outNode)
        if (self.nextConnection):
            self.nextConnection.calculateValue(nodes, futureNodes)

class Brain:
    def __init__(self):
        self.fitness = 0
        self.nodes = {}
        self.connections = {}

    # make this brain from scratch, with only input and output nodes and no connections
    # should only be used when creating the initial population
    def initNewBrain(self):
        for i in range(INPUT_NODES):
            self.nodes[i + 1] = NodeGene(i + 1)
        for i in range(OUTPUT_NODES):
            self.nodes[i + 1 + INPUT_NODES] = NodeGene(i + 1 + INPUT_NODES)

    # make this brain the offspring of two parents
    def crossover(self, parentA, parentB):
        pass

    # calculate the outputs based on given inputs
    def think(self, inputs):
        # reset all node values
        for n in self.nodes.values():
            n.value = 0
        # set inputs
        nodesToCalculate = list()
        for i in range(INPUT_NODES):
            self.nodes[i + 1].value = inputs[i]
            nodesToCalculate.append(i + 1)

        # calculate values
        while (len(nodesToCalculate) > 0):
            nextNode = nodesToCalculate.pop(0)
            if (nextNode in self.connections):
                self.connections[nextNode].calculateValue(self.nodes, nodesToCalculate)

        # return outputs
        outputs = list()
        for i in range(OUTPUT_NODES):
            outputs.append(self.nodes[i + 1 + INPUT_NODES].value)
        return outputs

    # check if a node is later in the tree than the given node
    def isNodeLaterOnPath(self, startNodeINum, locateINum):
        q = list()
        q.append(startNodeINum)
        while (len(q) > 0):
            nextNode = q.pop(0)
            if (nextNode == locateINum):
                return True
            if (nextNode in self.connections):
                q.append(self.connections[nextNode].outNode)
                currentConnection = self.connections[nextNode]
                while (currentConnection.nextConnection):
                    currentConnection = currentConnection.nextConnection
                    q.append(currentConnection.outNode)
        return False

    # add a new connection between two nodes
    # takes the inum values of the nodes as input, not the node objects
    def addNewConnection(self, inNode, outNode, weight=0, innovationNumber=None):
        # return false if the end of the connection is an input node
        if (self.nodes[outNode].inum <= INPUT_NODES):
            raise ValueError('Connections cannot end at an input node!')
        # return false if the beginning of the connection is an output node
        if (self.nodes[inNode].inum > INPUT_NODES and self.nodes[inNode].inum <= INPUT_NODES + OUTPUT_NODES):
            raise ValueError('Connections cannot start at an output node!')
        # return false if this connection will create a cycle
        if (self.isNodeLaterOnPath(outNode, inNode)):
            raise ValueError('Connections cannot create cycles!')

        # create the connection and return true
        newConnection = ConnectionGene(inNode, outNode, weight, innovationNumber)
        if (inNode in self.connections):
            self.connections[inNode].addNewConnection(newConnection)
        else:
            self.connections[inNode] = newConnection

    # adds a new node in the middle of an existing connection, modifying connections as necessary
    def addNewNode(self, oldConnection):
        newNode = NodeGene()
        self.nodes[newNode.inum] = newNode

        oldConnection.enabled = False

        self.addNewConnection(oldConnection.inNode, newNode.inum, oldConnection.weight)
        self.addNewConnection(newNode.inum, oldConnection.outNode, oldConnection.weight)

    # return a list of all connections
    def getAllConnections(self):
        allConnections = list()
        baseConnections = list(self.connections.values())
        if (len(baseConnections) == 0):
            return allConnections
        while (len(baseConnections) > 0):
            c = baseConnections.pop(0)
            allConnections.append(c)
            while (c.nextConnection):
                c = c.nextConnection
                allConnections.append(c)

        return allConnections

    # make one random structural mutation to the neural network
    # if there are no connections, add a connection
    # otherwise, choose randomly between adding a connection and adding a node
    def mutateStructure(self):
        allConnections = self.getAllConnections()
        if (len(allConnections) == 0 or random() < 0.5):
            # add a connection
            w = round(2 * (random() - 0.5), 2)      # the weight of the new connection
            '''
            A random connection is made as follows:
            1. pick a node at random to be the start node
            2. pick a node at random to be the end node (can be same as start node)
            3. check to see if this connection already exists
              a. if so, and it is disabled, enable it and return
              b. if so, and it is already enabled, return to step 2 and pick another end node at random without replacement
            4. attempt to make a new connection between the two nodes
              a. if new connection is successful, return
              b. if not, return to step 2 and pick another end node at random without replacement
            5. once all end nodes have been tried, return to step 1 and pick a new node without replacement

            Using this system all potential connections between nodes will be tried, even illegal connections
            Once a valid connection has been found, it will be made and the function will return
            If there are no valid connections remaining in the structure, function will return
            '''
            startNodes = list(self.nodes.values())
            while (len(startNodes) > 0):
                # step 1
                startIndex = floor(len(startNodes) * random())
                s = startNodes.pop(startIndex)
                endNodes = list(self.nodes.values())
                while (len(endNodes) > 0):
                    # step 2
                    endIndex = floor(len(endNodes) * random())
                    e = endNodes.pop(endIndex)
                    try:
                        # step 3
                        for c in allConnections:
                            if (c.inNode == s.inum and c.outNode == e.inum):
                                if (c.enabled):
                                    raise ValueError('Connection already exists!')
                                else:
                                    # step 3a
                                    c.enabled = True
                                    return
                        # step 4
                        self.addNewConnection(s.inum, e.inum, w)
                        # step 4a
                        return
                    except ValueError:
                        # step 3b and 4b
                        pass
                # step 5 (back to start of outer while loop)
            # if code reaches here, all valid connections already exist in this structure
            return
        else:
            # add a node
            changeIndex = floor(len(allConnections) * random())
            self.addNewNode(allConnections[changeIndex])

    # modify the weights of each connection in the neural network with the given probability
    def mutateWeights(self, chance=0.01):
        allConnections = self.getAllConnections()

        for c in allConnections:
            if (random() < chance):
                c.weight + round(2 * (random() - 0.5), 2)


a = Brain()
a.initNewBrain()
print(len(list(a.nodes.values())))
print(len(a.getAllConnections()))
print(a.think((1,2,2)))
a.mutateStructure()
print(len(list(a.nodes.values())))
print(len(a.getAllConnections()))
print(a.think((1,2,2)))
