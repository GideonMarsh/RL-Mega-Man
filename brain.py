# Gideon Marsh
# github.com/GideonMarsh

import constants
from random import random
from math import floor

#from time import time

input_nodes = constants.XPIXELS * constants.YPIXELS
output_nodes = constants.CONTROLLER_OUTPUTS

'''
Nodes with innovation numbers 1 through input_nodes are the input nodes
Nodes with innovation numbers 1 + input_nodes through output_nodes + input_nodes are the output nodes
Nodes with any other innovation number are hidden nodes
'''

nodeCount = input_nodes + output_nodes
connectionCount = 0

class ConnectionGene:
    def __init__(self, inNode, outNode, weight=0, innovationNumber=None, enabled=True):
        if (innovationNumber):
            self.inum = innovationNumber
        else:
            global connectionCount
            connectionCount = connectionCount + 1
            self.inum = connectionCount
        self.weight = weight
        self.enabled = enabled
        self.inNode = inNode
        self.outNode = outNode
        self.nextConnection = None

    def addNewConnection(self, newConnection):
        if (self.nextConnection == None):
            self.nextConnection = newConnection
        else:
            self.nextConnection.addNewConnection(newConnection)

    def calculateValue(self, nodes):
        if (self.enabled):
            if (self.outNode in nodes):
                nodes[self.outNode] = nodes[self.outNode] + nodes[self.inNode] * self.weight
            else:
                nodes[self.outNode] = nodes[self.inNode] * self.weight
        if (self.nextConnection):
            self.nextConnection.calculateValue(nodes)

    def getTopologicalOrder(self, nodeIndex, futureNodes):
        n = nodeIndex
        if (self.outNode in futureNodes):
            if (self.outNode in futureNodes[:nodeIndex]):
                n = n - 1
            futureNodes.remove(self.outNode)
        futureNodes.append(self.outNode)
        if (self.nextConnection):
            n = self.nextConnection.getTopologicalOrder(n, futureNodes)
        return n

class Brain:
    def __init__(self):
        self.fitness = 0
        self.connections = {}
        self.nodeOrder = list()
        self.species = -1

    # make this brain from scratch
    # should only be used when creating the initial population
    def initNewBrain(self):
        self.mutateStructure()

    # make this brain the offspring of two parents
    def crossover(self, parentA, parentB):

        def inumSort(i):
            return i.inum

        parentAGenes = parentA.getAllConnections()
        parentAGenes.sort(key=inumSort)
        parentBGenes = parentB.getAllConnections()
        parentBGenes.sort(key=inumSort)

        ia = ib = 0
        while (ia < len(parentAGenes) and ib < len(parentBGenes)):
            if (parentAGenes[ia].inum == parentBGenes[ib].inum):
                # matching gene, choose randomly between them
                if (random() < 0.5):
                    self.addNewConnection(parentAGenes[ia].inNode, parentAGenes[ia].outNode, parentAGenes[ia].weight, parentAGenes[ia].inum, parentAGenes[ia].enabled)
                else:
                    self.addNewConnection(parentBGenes[ib].inNode, parentBGenes[ib].outNode, parentBGenes[ib].weight, parentBGenes[ib].inum, parentBGenes[ib].enabled)
                ia = ia + 1
                ib = ib + 1
            else:
                # not matching gene, carry over the gene with smaller inum
                # do not carry it over if it creates a cycle
                if (parentAGenes[ia].inum > parentBGenes[ib].inum):
                    # carry over parent B gene
                    if (not self.isNodeLaterOnPath(parentBGenes[ib].outNode, parentBGenes[ib].inNode)):
                        self.addNewConnection(parentBGenes[ib].inNode, parentBGenes[ib].outNode, parentBGenes[ib].weight, parentBGenes[ib].inum, parentBGenes[ib].enabled)
                    ib = ib + 1
                else:
                    # carry over parent A gene
                    if (not self.isNodeLaterOnPath(parentAGenes[ia].outNode, parentAGenes[ia].inNode)):
                        self.addNewConnection(parentAGenes[ia].inNode, parentAGenes[ia].outNode, parentAGenes[ia].weight, parentAGenes[ia].inum, parentAGenes[ia].enabled)
                    ia = ia + 1

        # carry over all remaining unseen genes
        while (ia < len(parentAGenes)):
            self.addNewConnection(parentAGenes[ia].inNode, parentAGenes[ia].outNode, parentAGenes[ia].weight, parentAGenes[ia].inum, parentAGenes[ia].enabled)
            ia = ia + 1

        while (ib < len(parentBGenes)):
            self.addNewConnection(parentBGenes[ib].inNode, parentBGenes[ib].outNode, parentBGenes[ib].weight, parentBGenes[ib].inum, parentBGenes[ib].enabled)
            ib = ib + 1

        # check to see if any duplicate connections exist
        for k in self.connections.keys():
            c1 = self.connections[k]
            c1Parent = None
            matchFound = False
            while c1 and not matchFound:
                c2 = c1.nextConnection
                c2Parent = c1
                while c2:
                    if (c1.outNode == c2.outNode):
                        # duplicate connection
                        # choose one at random to keep, delete the other
                        matchFound = True
                        if (random() < 0.5):
                            c2Parent.nextConnection = c2.nextConnection
                            break
                        else:
                            if c1Parent:
                                c1Parent.nextConnection = c1.nextConnection
                            else:
                                self.connections[k] = c1.nextConnection
                            break
                    c2Parent = c2
                    c2 = c2.nextConnection
                c1Parent = c1
                c1 = c1.nextConnection



    # check how similar this brain is to another
    def compare(self, otherBrain):
        # compare the connection genome of both genes using the following function
        # d = (c1 * D) / N + c2 * W
        # c1, c2 = importance coefficients
        # d = compatibility distance
        # D = number of excess and disjoint genes
        # W = average weight differences of matching genes
        # N = number of genes in the larger genome

        c1 = 10
        c2 = 5

        allGenes1 = self.getAllConnections()
        allGenes2 = otherBrain.getAllConnections()

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

        D = len(mismatchedGenes)

        d = (c1 * D) / N + c2 * W
        return d

    # calculate the outputs based on given inputs
    def think(self, inputs):

        nodes = {}
        # set inputs
        for i in range(input_nodes):
            nodes[i + 1] = inputs[i]

        # calculate values
        for i in self.nodeOrder:
            if (i in self.connections):
                self.connections[i].calculateValue(nodes)

        # return outputs
        outputs = list()
        for i in range(output_nodes):
            if (i + 1 + input_nodes in nodes):
                outputs.append(nodes[i + 1 + input_nodes])
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
    def addNewConnection(self, inNode, outNode, weight=0, innovationNumber=None, enabled=True):
        # return false if the end of the connection is an input node
        if (outNode <= input_nodes):
            raise ValueError('Connections cannot end at an input node!')
        # return false if the beginning of the connection is an output node
        if (inNode > input_nodes and inNode <= input_nodes + output_nodes):
            raise ValueError('Connections cannot start at an output node!')
        # return false if this connection will create a cycle
        if (self.isNodeLaterOnPath(outNode, inNode)):
            raise ValueError('Connections cannot create cycles!')

        # create the connection
        newConnection = ConnectionGene(inNode, outNode, weight, innovationNumber, enabled)
        if (inNode in self.connections):
            self.connections[inNode].addNewConnection(newConnection)
        else:
            self.connections[inNode] = newConnection

    # adds a new node in the middle of an existing connection, modifying connections as necessary
    def addNewNode(self, oldConnection):
        global nodeCount
        nodeCount = nodeCount + 1

        oldConnection.enabled = False

        try:
            self.addNewConnection(oldConnection.inNode, nodeCount, oldConnection.weight)
            self.addNewConnection(nodeCount, oldConnection.outNode, oldConnection.weight)
        except ValueError:
            for c in self.getAllConnections():
                print(str(c.inum) + ': ' + str(c.inNode) + ' ' + str(c.outNode), end='; ')
            print('')
            print('Trying to make node ' + str(nodeCount) + ' at ' + str(oldConnection.inum) + ': ' + str(oldConnection.inNode) + ' ' + str(oldConnection.outNode))
            raise

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
        for i in range(input_nodes + output_nodes):
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
        if (len(allConnections) == 0 or random() < 0.6):
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
            iList = list()
            for i in range(len(allConnections)):
                iList.append(i)
            while len(iList) > 0:
                changeIndex = floor(len(iList) * random())
                if (allConnections[changeIndex].enabled):
                    self.addNewNode(allConnections[changeIndex])
                    break
                else:
                    iList.pop(changeIndex)

    # modify the weights of each connection in the neural network with a certain probability
    # there is a chance that each connection will be modified equal to 1 / number of connections or 1%, whichever is higher
    # this means that if there is only one connection, it is guaranteed to be modified
    def mutateWeights(self):
        allConnections = self.getAllConnections()

        for c in allConnections:
            if (random() * min(len(allConnections), 100) < 1):
                c.weight + round(2 * (random() - 0.5), 2)

    # creates a list of nodes in topological order
    # this should be called after all modifications to the network structure, but before think()
    def prepareNodeTopology(self):
        self.nodeOrder = list()
        nodeIndex = 0
        for i in range(input_nodes):
            self.nodeOrder.append(i + 1)

        while (nodeIndex < len(self.nodeOrder)):
            if (self.nodeOrder[nodeIndex] in self.connections):
                nodeIndex = self.connections[self.nodeOrder[nodeIndex]].getTopologicalOrder(nodeIndex, self.nodeOrder)
            nodeIndex = nodeIndex + 1

    # splits node topology into 2d list where each list only contains nodes connected to nodes from the previous list or earlier
    # used for displaying topology
    def getNodeLayers(self):
        nodeLayers = list()
        nodeLayers.append(self.nodeOrder.copy())
        layerIndex = 0
        usedOutputNodes = list()

        while layerIndex < len(nodeLayers):
            i = 0
            while i < len(nodeLayers[layerIndex]):
                if nodeLayers[layerIndex][i] in self.connections:
                    c = self.connections[nodeLayers[layerIndex][i]]
                    while c:
                        for j in range(layerIndex + 1):
                            if c.outNode in nodeLayers[j]:
                                nodeLayers[j].remove(c.outNode)
                        if (layerIndex == len(nodeLayers) - 1):
                            nodeLayers.append(list())
                        if c.outNode not in nodeLayers[layerIndex + 1] and c.outNode not in usedOutputNodes:
                            nodeLayers[layerIndex + 1].append(c.outNode)
                        c = c.nextConnection
                    i = i + 1
                else:
                    if nodeLayers[layerIndex][i] > input_nodes and nodeLayers[layerIndex][i] <= input_nodes + output_nodes:
                        usedOutputNodes.append(nodeLayers[layerIndex][i])
                    nodeLayers[layerIndex].remove(nodeLayers[layerIndex][i])
            layerIndex = layerIndex + 1
        nodeLayers[-1] = usedOutputNodes
        return nodeLayers


'''
inputs = list()
for i in range(input_nodes):
    inputs.append(round(random() * 255))


a = Brain()
b = Brain()
a.initNewBrain()
a.prepareNodeTopology()
b.initNewBrain()
b.prepareNodeTopology()

print(len(a.getAllNodes()))
print(len(a.getAllConnections()))
print(a.think(inputs))

a.mutateStructure()
a.prepareNodeTopology()

print(len(a.getAllNodes()))
print(len(a.getAllConnections()))
print(a.think(inputs))

for i in range(15):
    a.mutateStructure()
    b.mutateStructure()
a.prepareNodeTopology()
b.prepareNodeTopology()

print(len(a.getAllNodes()))
print(len(a.getAllConnections()))
print(len(b.getAllNodes()))
print(len(b.getAllConnections()))
print('comparison')
print(a.compare(b))

c = Brain()

c.crossover(a, b)
c.prepareNodeTopology()
print(len(c.getAllNodes()))
print(len(c.getAllConnections()))

print(a.think(inputs))
print(b.think(inputs))
print(c.think(inputs))

d = c.getAllConnections()
for i in d:
    print(str(i.inNode) + ' ' + str(i.outNode))
'''
'''
a = Brain()
a.initNewBrain()
for i in range(15):
    a.mutateStructure()
c = a.getAllConnections()
for i in c:
    print(str(i.inNode) + ' ' + str(i.outNode))
a.prepareNodeTopology()
print(a.nodeOrder)

print(a.think((1,1,1,1,1,1)))
'''
'''
a = Brain()
a.initNewBrain()

b = Brain()
c = Brain()
b.crossover(a, a)
c.crossover(a, a)

print(b.compare(c))
for i in range(10):
    b.mutateStructure()
    b.mutateWeights()
    c.mutateStructure()
    c.mutateWeights()
    print(b.compare(c))

for i in range(10):
    b.mutateStructure()
    b.mutateWeights()
    print(b.compare(c))
'''
'''
a = Brain()
a.initNewBrain()
for i in range(3):
    a.mutateStructure()
a.prepareNodeTopology()
for c in a.getAllConnections():
    print(str(c.inNode) + ' ' + str(c.outNode), end='; ')
print('')
l = a.getNodeLayers()
for c in l:
    for n in c:
        print(str(n), end=' ')
    print('')
'''
