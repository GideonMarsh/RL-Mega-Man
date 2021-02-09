# Gideon Marsh
# github.com/GideonMarsh

# code from https://stackoverflow.com/questions/29888233/how-to-visualize-a-neural-network

from matplotlib import pyplot
from math import cos, sin, atan
import brain

neuron_radius = 0.5

def line_between_two_neurons(neuron1, neuron2):
    try:
        angle = atan((neuron2.x - neuron1.x) / float(neuron2.y - neuron1.y))
    except ZeroDivisionError:
        angle = 0
    x_adjustment = neuron_radius * sin(angle)
    y_adjustment = neuron_radius * cos(angle)
    line = pyplot.Line2D((neuron1.x - x_adjustment, neuron2.x + x_adjustment), (neuron1.y - y_adjustment, neuron2.y + y_adjustment))
    pyplot.gca().add_line(line)

class Neuron():
    def __init__(self, x, y, inum):
        self.x = x
        self.y = y
        self.inum = inum

    def draw(self, neuron_radius):
        circle = pyplot.Circle((self.x, self.y), radius=neuron_radius, fill=False)
        pyplot.gca().add_patch(circle)
        pyplot.text(self.x, self.y, str(self.inum))


class Layer():
    def __init__(self, network, number_of_neurons, number_of_neurons_in_widest_layer, nodeLayer):
        self.vertical_distance_between_layers = 6
        self.horizontal_distance_between_neurons = 2
        self.number_of_neurons_in_widest_layer = number_of_neurons_in_widest_layer
        self.previous_layer = self.__get_previous_layer(network)
        self.y = self.__calculate_layer_y_position()
        self.neurons = self.__intialise_neurons(number_of_neurons, nodeLayer)

    def __intialise_neurons(self, number_of_neurons, nodeLayer):
        neurons = []
        x = self.__calculate_left_margin_so_layer_is_centered(number_of_neurons)
        for iteration in range(number_of_neurons):
            neuron = Neuron(x, self.y, nodeLayer[iteration])
            neurons.append(neuron)
            x += self.horizontal_distance_between_neurons
        return neurons

    def __calculate_left_margin_so_layer_is_centered(self, number_of_neurons):
        return self.horizontal_distance_between_neurons * (self.number_of_neurons_in_widest_layer - number_of_neurons) / 2

    def __calculate_layer_y_position(self):
        if self.previous_layer:
            return self.previous_layer.y + self.vertical_distance_between_layers
        else:
            return 0

    def __get_previous_layer(self, network):
        if len(network.layers) > 0:
            return network.layers[-1]
        else:
            return None

    def draw(self, layerType=0):
        for neuron in self.neurons:
            neuron.draw( neuron_radius )
            '''
            if self.previous_layer:
                for previous_layer_neuron in self.previous_layer.neurons:
                    line_between_two_neurons(neuron, previous_layer_neuron)
            '''

class NeuralNetwork():
    def __init__(self, number_of_neurons_in_widest_layer):
        self.number_of_neurons_in_widest_layer = number_of_neurons_in_widest_layer
        self.layers = []
        self.layertype = 0

    def add_layer(self, number_of_neurons, nodeLayer):
        layer = Layer(self, number_of_neurons, self.number_of_neurons_in_widest_layer, nodeLayer)
        self.layers.append(layer)

    def draw(self, connections):
        neurons = list()
        pyplot.figure()
        for i in range( len(self.layers) ):
            layer = self.layers[i]
            if i == len(self.layers)-1:
                i = -1
            layer.draw( i )
            for n in layer.neurons:
                neurons.append(n)
        for c in connections:
            if c.enabled:
                neuron1 = None
                for j in neurons:
                    if c.inNode == j.inum:
                        neuron1 = j
                        break
                neuron2 = None
                for j in neurons:
                    if c.outNode == j.inum:
                        neuron2 = j
                        break
                line_between_two_neurons(neuron2, neuron1)

        pyplot.axis('scaled')
        pyplot.axis('off')
        pyplot.title( 'Neural Network architecture', fontsize=15 )
        pyplot.show()

class DrawNN():
    def __init__( self, neural_network ):
        self.connections = neural_network.getAllConnections()
        self.layers = neural_network.getNodeLayers()

    def draw( self ):
        layers = list()
        for l in self.layers:
            layers.append(len(l))
        widest_layer = max( layers )

        network = NeuralNetwork( widest_layer )
        for l in range(len(layers)):
            network.add_layer(layers[l], self.layers[l])
        network.draw(self.connections)

b = brain.Brain()
b.initNewBrain()
for i in range(5):
    b.mutateStructure()
b.prepareNodeTopology()

for c in b.getAllConnections():
    if c.enabled:
        print(str(c.inNode) + ' ' + str(c.outNode), end='; ')
print('')
for c in b.getAllConnections():
    if not c.enabled:
        print(str(c.inNode) + ' ' + str(c.outNode), end='; ')
print('')
nl = b.getNodeLayers()
for l in nl:
    for n in l:
        print(str(n), end=' ')
    print('')
network = DrawNN( b )
network.draw()
