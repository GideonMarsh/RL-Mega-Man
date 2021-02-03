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
            if (self.outNode in nodes):
                nodes[self.outNode] = nodes[self.outNode] + nodes[self.inNode] * self.weight
            else:
                nodes[self.outNode] = nodes[self.inNode] * self.weight
        futureNodes.append(self.outNode)
        if (self.nextConnection):
            self.nextConnection.calculateValue(nodes, futureNodes)

class Brain:
    def __init__(self):
        self.fitness = 0
        self.connections = {}

    # make this brain from scratch, with only input and output nodes and no connections
    # should only be used when creating the initial population
    def initNewBrain(self):
        pass

    # make this brain the offspring of two parents
    def crossover(self, parentA, parentB):
        pass

    # check how similar this brain is to another
    def compare(self, otherBrain):
        # compare the connection genome of both genes using the following function
        # d = (c1 * E) / N + (c2 * D) / N + c3 * W
        # c1, c2, c3 = importance coefficients
        # d = compatibility distance
        # E = number of excess genes
        # D = number of disjoint genes
        # W = average weight differences of matching genes
        # N = number of genes in the larger genome

        c1 = c2 = c3 = 1

        allGenes1 = self.getAllConnections()
        allGenes2 = otherBrain.getAllConnections()

        lastGene1 = lastGene2 = 0

        for g in allGenes1:
            if (g.inum > lastGene1):
                lastGene1 = g.inum

        for h in allGenes2:
            if (h.inum > lastGene2):
                lastGene2 = h.inum

        mismatchedGenes = list()
        matchedWeights = list()

        N = len(allGenes1)
        if (len(allGenes2) > N):
            N = len(allGenes2)

        # for every gene in allGenes1, try to find a match in allGenes2
        while len(allGenes1) > 0:
            g = allGenes1.pop(0)
            for h in allGenes2:
                if (g.inum == h.inum):
                    # genes matched
                    matchedWeights.append(abs(g.weight - h.weight))
                    allGenes2.remove(h)
                    break
            # no matching gene
            mismatchedGenes.append(g.inum)

        # all remaining genes in allGenes2 have no match in allGenes1
        for h in allGenes2:
            mismatchedGenes.append(h.inum)

        W = 0
        if (len(matchedWeights) > 0):
            for w in matchedWeights:
                W = W + w
            W = W / len(matchedWeights)

        D = 0
        E = 0

        for m in mismatchedGenes:
            if (m > lastGene1 or m > lastGene2):
                E = E + 1
            else:
                D = D + 1

        d = (c1 * E) / N + (c2 * D) / N + c3 * W
        return d

    # calculate the outputs based on given inputs
    def think(self, inputs):

        nodes = {}
        # set inputs
        nodesToCalculate = list()
        for i in range(INPUT_NODES):
            nodes[i + 1] = inputs[i]
            nodesToCalculate.append(i + 1)

        # calculate values
        while (len(nodesToCalculate) > 0):
            nextNode = nodesToCalculate.pop(0)
            if (nextNode in self.connections):
                self.connections[nextNode].calculateValue(nodes, nodesToCalculate)

        # return outputs
        outputs = list()
        for i in range(OUTPUT_NODES):
            if (i + 1 + INPUT_NODES in nodes):
                outputs.append(nodes[i + 1 + INPUT_NODES])
            else:
                outputs.append(0)
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
        if (outNode <= INPUT_NODES):
            raise ValueError('Connections cannot end at an input node!')
        # return false if the beginning of the connection is an output node
        if (inNode > INPUT_NODES and inNode <= INPUT_NODES + OUTPUT_NODES):
            raise ValueError('Connections cannot start at an output node!')
        # return false if this connection will create a cycle
        if (self.isNodeLaterOnPath(outNode, inNode)):
            raise ValueError('Connections cannot create cycles!')

        # create the connection
        newConnection = ConnectionGene(inNode, outNode, weight, innovationNumber)
        if (inNode in self.connections):
            self.connections[inNode].addNewConnection(newConnection)
        else:
            self.connections[inNode] = newConnection

    # adds a new node in the middle of an existing connection, modifying connections as necessary
    def addNewNode(self, oldConnection):
        global nodeCount
        nodeCount = nodeCount + 1

        oldConnection.enabled = False

        self.addNewConnection(oldConnection.inNode, nodeCount, oldConnection.weight)
        self.addNewConnection(nodeCount, oldConnection.outNode, oldConnection.weight)

    # returns a list of all connections
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

    # returns a list of all nodes, which is inferred from all connections
    def getAllNodes(self):
        allConnections = self.getAllConnections()
        nodes = list()
        for i in range(INPUT_NODES + OUTPUT_NODES):
            nodes.append(i+1)
        for c in allConnections:
            if c.inNode not in nodes:
                nodes.append(c.inNode)
            if c.outNode not in nodes:
                nodes.append(c.outNode)
        return nodes

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
            startNodes = self.getAllNodes()
            while (len(startNodes) > 0):
                # step 1
                startIndex = floor(len(startNodes) * random())
                s = startNodes.pop(startIndex)
                endNodes = self.getAllNodes()
                while (len(endNodes) > 0):
                    # step 2
                    endIndex = floor(len(endNodes) * random())
                    e = endNodes.pop(endIndex)
                    try:
                        # step 3
                        for c in allConnections:
                            if (c.inNode == s and c.outNode == e):
                                if (c.enabled):
                                    raise ValueError('Connection already exists!')
                                else:
                                    # step 3a
                                    c.enabled = True
                                    return
                        # step 4
                        self.addNewConnection(s, e, w)
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
b = Brain()
a.initNewBrain()
b.initNewBrain()

print(len(a.getAllNodes()))
print(len(a.getAllConnections()))
print(a.think((1,2,2)))

a.mutateStructure()

print(len(a.getAllNodes()))
print(len(a.getAllConnections()))
print(a.think((1,2,2)))

b.mutateStructure()
a.mutateStructure()
b.mutateStructure()
a.mutateStructure()
b.mutateStructure()
print(len(a.getAllNodes()))
print(len(a.getAllConnections()))
print(len(b.getAllNodes()))
print(len(b.getAllConnections()))
print('comparison')
print(a.compare(b))
