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
            self.nextConection.addNewConnection(newConnection)

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
    def addNewConnection(self, inNode, outNode, weight=0, innovationNumber=None):
        # return false if the end of the connection is an input node
        if (self.nodes[outNode].inum <= INPUT_NODES):
            raise ValueError('Connections cannot end at an input node')
        # return false if the beginning of the connection is an output node
        if (self.nodes[inNode].inum > INPUT_NODES and self.nodes[inNode].inum <= INPUT_NODES + OUTPUT_NODES):
            raise ValueError('Connections cannot start at an output node')
        # return false if this connection will create a cycle
        if (self.isNodeLaterOnPath(outNode, inNode)):
            raise ValueError('Connections cannot create cycles')

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

    # make one random structural mutation to the neural network
    # if there are no connections, add a connection
    # otherwise, choose randomly between adding a connection and adding a node
    def mutateStructure(self):
        allConnections = list()
        baseConnections = self.connections.values()
        if (len(baseConnections) == 0 or random() < 0.5):
            # add a connection
            allNodes = self.nodes.values()
            # pick two nodes at random (without replacement)
            # verify that a connection between the two nodes would be legal
            # add the connection
        else:
            # add a node
            while (len(baseConnections) > 0):
                c = baseConnections.pop(0)
                allConnections.append(c)
                while (c.nextConnection):
                    c = c.nextConnection
                    allConnections.append(c)

            changeIndex = floor(len(allConnections) * random())
            # add a new node to replace allConnections[changeIndex] here

    # make one random connection weight in the neural network
    def mutateWeight(self):
        allConnections = list()
        baseConnections = self.connections.values()
        if (len(baseConnections) == 0):
            return
        while (len(baseConnections) > 0):
            c = baseConnections.pop(0)
            allConnections.append(c)
            while (c.nextConnection):
                c = c.nextConnection
                allConnections.append(c)

        changeIndex = floor(len(allConnections) * random())
        # change the weight of allConnections[changeIndex] here


a = Brain()
a.initNewBrain()
a.addNewConnection(1, 4, 0.5)
a.addNewConnection(1, 5, -2)
a.addNewConnection(2, 4, 1)
a.addNewConnection(2, 5, 1)
a.addNewConnection(3, 4, 2)
a.addNewConnection(3, 5, -0.5)
print(a.think((1,2,2)))
