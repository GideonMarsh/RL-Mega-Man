# RL-Mega-Man
Reinforcement learning in Mega Man Legacy Collection

The goal of this project is to make a framework that can perform reinforcement learning using the NEAT algorithm on the game Mega Man Legacy Collection (on Steam). The project does not have any access to the code of the game, using only information available to a typical player. 

### Program input
The program takes regular screenshots of the game window using the pyautogui library and uses the pixel values of the screenshots as inputs for the program. The screenshots are taken at full resolution, but only a small number of the pixels are used. These pixels are regularly spaced, which results in the program perceiving a low quality picture. Additionally, the screenshots are converted to greyscale to simplify the inputs. The size of the game window is set programmatically for consistent inputs. The screenshots can only be taken if the game window is in the foreground; if at any point the game window is no longer in the foreground, the program ends.

### Program output
The program controls the game using keyboard inputs. These are simulated using the pynput library. The game menus are navigated using input scripts which rely on the consistency of the game behavior. Because of this, the program will not function properly if there are any user inputs to the game during run time. 

### Genetic algorithm
The process of reinforcement learning is handled by the NEAT algorithm. A population of 100 "brains" are created and allowed to play the game. After a given brain's run terminates, the fitness of that run is determined and the next brain is selected to play. After all 100 brains are done playing, a new population of 100 brains is created using the previous generation as the parents. This program follows the implementation of the NEAT algorithm as specified in the original NEAT paper, which can be found here: (http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf). Please read this paper for additional details that are not covered below.

*Brains*

Each brain consists of a collection of nodes and connections that form a simple neural network. The number of input nodes is set at the number of pixels read from the input screenshots, and the number of output nodes is set at the number of controller outputs. Each brain stores its connections and determines its nodes implicitely from the connections. Each connection has a real number weight which is determined at its creation (but can be modified by mutation).

Calculating the output of the brains follows these steps. First, the values of the input nodes are set based on the inputs screenshots. Each node has an associated pixel position on the screenshot (which is greyscale), and the node is set to the pixel value - 128. The values are then propogated forward using the connections. The order of the calcuations is determined by topological order (calculations are performed only after all prerequisite calculations are complete). Each connection takes the value of its input node, multiplies that value by the weight of the connection, then adds the resulting value to the output node. After these calculations are complete, the values of the output nodes are used to determine the controller inputs to the game. If the value of a node is greater than 0, the associated button is pressed. If the value is 0 or less, the button is not pressed (or released). Using this method, the brains can programmatically control the game using only the visual information of the game is input.

New nodes and connections are added by mutation, and new brains are created using "reproduction". 
* New nodes are added by selecting an existing connection and bisecting it, creating a new (implicit) node with two new connections: one from the original connection's input node to the new node, and one from the new node to the original connection's output node. The original connection is then disabled. 
* New connections are added by selecting two nodes at random and attempting to make a connection between them. If an enabled connection between the nodes already exists, the connection is invalid. If a disabled connection exists, it is enabled. There are three situations in which an entirely new connection can be invalid: if it starts at an output node, if it ends at an input node, or if it creates a cycle. Cycles are not allowed as they prevent calculations from ever completing when values are propogated forward.
* Reproduction is the combining of two brains to create a new brain. The connections of both brains are examined to determine if they should be included in the new brain (nodes don't need to be considered since they are implicit). If the connection exists in one brain but not the other, the connection is added (unless it creates a cycle). If it exists in both brains, the connection is added and uses the weight from the brain with the higher fitness.

*Species*

The population of brains is split into categories called species based on their similarities to each other (see the NEAT paper for more information). The species are used to preserve innovation among the population, allowing for lots of different strategies to be considered.

*Fitness*

The fitness of each brain is determined primarily by time survived (tracked down to a tenth of a second), with several caveats. There are 5 situations that cause a brain's run to end, each with different fitness calculations.
* If the brain completes the level fitness is awarded based on completion time, with lower times providing higher values. These values dominate the fitness function, such that completing the level with the slowest possible time still results in higher fitness than any run that does not complete the level. 
* If the brain loses a life, fitness is awarded based on the time survived.
* If the brain stops changing its controller inputs, the program considers ending the run. A screenshot is taken two seconds after the brain stops changing its inputs. 4 seconds later, the program starts comparing this screenshot to all incoming screenshots. If there is a match, it is determined that by ceasing to control the game the brain has ceased making progress, and the run ends. Fitness is awarded based on the time survived up to the last change in inputs. If there is a change in inputs while waiting, the timers are reset. If the comparison screenshot doesn't match, it is determined that despite not changing inputs, the run is still progressing.
* At regular intervals the program will save one of the input screenshots, then compare it to several other input screenshots a short while later. If there is a match then it is determined that the brain stopped progressing, and the run ends. Fitness is awarded based on time survived up to when the comparison screenshot was taken. If there isn't a match a new screenshot is saved and the process repeats.
* If a run exceeds 10 minutes without triggering any of the previous conditions, the run ends and no fitness is awarded.
Additionally, there is a small fitness penalty for each change in inputs, penalizing excessive button pressing.

With all of the above conditions, fitness is awarded with the following priority:
1. Completing the level quickly with efficient controller inputs
2. Completing the level slowly without efficient controllr inputs
3. Suriviving as long as possible, with few but regular changes to controller inputs and without remaining in one place for too long

This fitness function closely (but not perfectly) captures the preferred behavior of the program. Better fitness calcuation would require access to the game's code (which is outside the scope of this project), or complex screenshot analysis.

## Current problems
Right now fitness is not being awarded consistently. The same brain can receive different fitness values when run multiple times. This results in some brains being selected as parents for having good traits, then their children doing poorly despite having those traits. This results in the algorithm not making any progress past a few seconds into a level, once required inputs become more complicated than just holding right.

The cause of this problem is likely the slight time variation between when screenshots are taken. Screenshots are not taken at regular intervals, with an average of 1/300th of a second variation. It is unknown why this variation is occurring, or whether this is the only cause of the problem. The current solution being tested is running each brain multiple times and only storing the lowest earned fitness, rewarding genes that can consistently perform well.

The program cannot function properly unless this is fixed. If a solution cannot be found, then the program will have to be majorly reworked (or scrapped and remade).
