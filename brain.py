# Gideon Marsh
# github.com/GideonMarsh

INPUT_NODES = 3
OUTPUT_NODES = 2

nodeCount = INPUT_NODES + OUTPUT_NODES
connectionCount = 0

class NodeGene:
    def __init__(self, minLayer, maxLayer, innovationNumber=None):
        if (innovationNumber):
            self.inum = innovationNumber
        else:
            global nodeCount
            nodeCount = nodeCount + 1
            self.inum = nodeCount
        self.maxLayer = maxLayer
        self.minLayer = minLayer
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
        nodes[self.outNode].value = nodes[self.outNode].value + nodes[self.inNode].value * self.weight
        futureNodes.append(self.outNode)
        if (self.nextConnection):
            self.nextConnection.calculateValue(nodes, futureNodes)

class Brain:
    def __init__(self):
        self.fitness = 0
        self.nodes = {}
        self.connections = {}

    def initNewBrain(self):
        # make this brain from scratch
        for i in range(INPUT_NODES):
            self.nodes[i + 1] = NodeGene(0, 0, i + 1)
        for i in range(OUTPUT_NODES):
            self.nodes[i + 1 + INPUT_NODES] = NodeGene(1, None, i + 1 + INPUT_NODES)

    def crossover(self, parentA, parentB):
        # make this brain the offspring of two parents
        pass

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

    def addNewConnection(self, newConnection):
        if (newConnection.inNode in self.connections):
            self.connections[newConnection.inNode].addNewConnection(newConnection)
        else:
            self.connections[newConnection.inNode] = newConnection

a = Brain()
a.initNewBrain()
a.addNewConnection(ConnectionGene(1, 4, 0.5))
a.addNewConnection(ConnectionGene(1, 5, -2))
a.addNewConnection(ConnectionGene(2, 4, 1))
a.addNewConnection(ConnectionGene(2, 5, 1))
a.addNewConnection(ConnectionGene(3, 4, 2))
a.addNewConnection(ConnectionGene(3, 5, -0.5))
print(a.think((1,2,2)))
