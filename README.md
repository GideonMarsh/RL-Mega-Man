# RL-Mega-Man
Reinforcement learning in Mega Man Legacy Collection

The goal of this project is to make a framework that can perform reinforcement learning using the NEAT algorithm on the game Mega Man Legacy Collection (on Steam). The project does not have any access to the code of the game, using only information available to a typical player. 

### Program input
The program takes regular screenshots of the game window using the pyautogui library and uses the pixel values of the screenshots as inputs for the program. The screenshots are taken at full resolution, but only a small number of the pixels are used. These pixels are regularly spaced, which results in the program perceiving a lower quality picture than what is shown in the normal game display. Additionally, the screenshots are converted to greyscale to simplify the inputs. The size of the game window is set programmatically for consistent inputs. The screenshots can only be taken if the game window is in the foreground; if at any point the game window is no longer in the foreground, the program ends.

### Program output
The program controls the game using keyboard inputs. These are simulated using the pynput library. The game menus are navigated using input scripts which rely on the consistency of the game behavior. Because of this, the program will not function properly if there are any user inputs to the game during run time. 

### Genetic algorithm
The process of reinforcement learning is handled by the NEAT algorithm. A population of 100 "brains" are created and allowed to play the game. After a given brain's run terminates, the fitness of that run is determined and the next brain is selected to play. After all 100 brains are done playing, a new population of 100 brains is created using the previous generation as the parents. Brains that score higher fitness values are more likely to be selected as parents for the new generation. This program follows the implementation of the NEAT algorithm as specified in the original NEAT paper, which can be found here: (http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf). Please read this paper for additional details that are not covered below.

*Brains*

Each brain consists of a collection of nodes and connections that form a simple neural network. The number of input nodes is set at the number of pixels read from the input screenshots, and the number of output nodes is set at the number of controller outputs. Each brain stores its connections and determines its nodes implicitely from the connections. Each connection has a real number weight which is determined at its creation (but can be modified by mutation).

Calculating the output of the brains follows these steps. First, the values of the input nodes are set based on the inputs screenshots. Each node has an associated pixel position on the screenshot (which is greyscale), and the node is set to \[the pixel value - 128\]. The values are then propogated forward using the connections. The order of the calcuations is determined by topological order (calculations are performed only after all prerequisite calculations are complete). Each connection takes the value of its input node, multiplies that value by the weight of the connection, then adds the resulting value to the output node. After these calculations are complete, the values of the output nodes are used to determine the controller inputs to the game. If the value of a node is greater than 0, the associated button is pressed. If the value is 0 or less, the button is not pressed (or released). Using this method, the brains can programmatically control the game using only the visual information of the game as input.

New nodes and connections are added by mutation, and new brains are created using "reproduction". 
* New nodes are added by selecting an existing connection and bisecting it, creating a new (implicit) node with two new connections: one from the original connection's input node to the new node, and one from the new node to the original connection's output node. The original connection is then disabled. All brains are created with one default connection, so this process always succeeds.
* New connections are added by selecting two nodes at random and attempting to make a connection between them. If an enabled connection between the nodes already exists, the new connection is invalid. If a disabled connection exists, it is enabled. There are three additional situations in which a new connection can be invalid: if it starts at an output node, if it ends at an input node, or if it creates a cycle. Cycles are not allowed as they prevent calculations from ever completing when values are propogated forward. If the new connection is invalid, a different pair of nodes is selected and the process repeats. If all node combinations have been tried, no new connections are available in this brain.
* Reproduction is the combining of two brains to create a new brain. The connections of both brains are examined to determine if they should be included in the new brain (nodes don't need to be considered since they are implicit). If the connection exists in one brain but not the other and it doesn't create a cycle, the connection is added to the new brain. If it exists in both brains, the connection is added and uses the weight from the brain with the higher fitness.

*Species*

The population of brains is split into categories called species based on their similarities to each other (see the NEAT paper for more information). The species are used to preserve innovation among the population, allowing for lots of different strategies to be considered.

*Fitness*

The ideal fitness function of the program would award fitness based on the following priority:
1. Completing the level quickly with efficient use of button presses
2. Completing the level quickly with excessive button presses
3. Completing the level slowly with efficient use of button presses
4. Completing the level slowly with excessive button presses
5. Completing most of the level before dying
6. Completing very little of the level before dying
7. Not moving at all

To match these requirements as closely as possible, fitness is determined like this:

The fitness of each brain is determined primarily by time survived (tracked down to a tenth of a second), with several caveats. There are 5 situations that cause a brain's run to end, each with different fitness calculations.
* If the brain completes the level, fitness is awarded based on completion time with lower times providing higher values. These values dominate the fitness function, such that completing the level with the slowest possible time still results in higher fitness than any run that does not complete the level. 
* If the brain loses a life, fitness is awarded based on the time survived.
* If the brain stops changing its controller inputs, the program considers ending the run. A screenshot is taken two seconds after the brain stops changing its inputs. 4 seconds later (if inputs still have not changed) the program starts comparing this screenshot to all incoming screenshots. If there is a match, it is determined that by ceasing to control the game the brain has ceased making progress, and the run ends. Fitness is awarded based on the time survived up to the last change in inputs. If there is a change in inputs at any point, the process repeats. If the comparison screenshot doesn't match incoming screenshots, it is determined that the run is still progressing.
* At regular intervals the program will save one of the input screenshots, then compare it to several other input screenshots a short while later. If there is a match then it is determined that the brain stopped progressing, and the run ends. Fitness is awarded based on time survived up to when the comparison screenshot was taken. If there isn't a match a new screenshot is saved and the process repeats.
* If a run exceeds 10 minutes without triggering any of the previous conditions, the run ends and no fitness is awarded.

Additionally, there is a small fitness penalty for each change in inputs, penalizing excessive button pressing. This rewards runs with optimal controller inputs, and penalizes jittery behavior.

With all of the above conditions, fitness is awarded with the following priorities:
1. Completing the level quickly with efficient use of button presses
2. Completing the level quickly with excessive button presses
3. Completing the level slowly with efficient use of button presses
4. Completing the level slowly with excessive button presses
5. Suriviving as long as possible (attempting to cheat the timer by making no progress counts as failing to survive)
6. Not moving at all

This fitness function closely (but not perfectly) captures the preferred behavior of the program. In particular, it is difficult to determine how much progress has been made through a level. This system functions on the premise that keeping track of the time survived and checking to see that progress is being made can substitute for checking the explicit progress through any given level. 

Better fitness calcuation would require access to the game's code or complex screenshot analysis, both of which are outside the current scope of this project.

## Problems
Right now fitness is not being awarded consistently. The same brain can receive different fitness values when run multiple times. Some brains are selected as parents for having good traits, then their children do poorly despite having those traits. This results in the algorithm not making any progress past a few seconds into a level, once required inputs become more complicated than just holding right.

The cause of this problem is likely the slight time variation between when screenshots are taken. Screenshots are not taken at regular intervals, with an average of 1/300th of a second variation. Even though this variation is less than a single frame of gameplay, the cumulative variation over many frames results in very slight variations in the timing of future screenshots. It is unknown why this variation is occurring, or whether this is the only cause of the problem. 

One solution I attempted was running each brain multiple times and only storing the lowest earned fitness, rewarding genes that can consistently perform well. The problem still occurred even when each brain was run 3 times. It may be possible to eliminate the variation by running each brain more times, but this presents a new problem: the program requires many hours to run. By running each brain only once the program is currently able to process about 40-50 generations while running overnight. By running each brain more than once, the amount of time the program takes to run a single generation is increased dramatically. While it may be possible to sidestep the problem by running each brain 10 times each or more, the amount of time that would take makes it near infeasible for me to analyze and debug it. It would also not solve the underlying problem, which may arise again as the brains progress further into the game and the cumulative variance adds up even more.

I have not been able to find a solution to this problem that works with the framework I've created.

## Future plans
The initial scope of this project was to perform reinforcement learning without accessing the code of the game. I believed that by making the calculation time vary by less than a frame, the program would not need to be locked to the framerate of the game. However, without accessing the game's code and allowing the brains to perform calculations on a frame by frame basis, the cumulative error adds up before the program can make any meaningful progress through the game. 

This problem could be solved by writing a program that has access to the data of the game every frame and can more precisely control how the game runs, not just how it's played. This can be accomplished by using an emulator. The current program runs the game using Steam, by taking input from the game only using screenshots, and providing output to the game only by simulating the keyboard. By using an emulator I would have greater control to how the game is run and would be able to more closely couple my program with the code of the game. I have no experience working with emulators and would need to do some research to get this to work. Several similar programs already exist that I could draw inspiration from, such as MarI/O, which performs the NEAT algorithm on Super Mario games using an emulator.

I plan to start this project over with this in mind. The structures and concepts in my code can be reused in the new project, particularly the code for the intricate neural network brains and the systems used in speciation.

There are also some features that never made it into the current program that could be addressed in future projects:
1. A major part of the Mega Man games is obtaining and utilizing different weapons during gameplay. The current program never got to the point where this was relevant, and so no code was written to utilize these weapons.
2. Being able to visualize the neural network of each brain would be both interesting and useful for testing, especially if it were in real time during a run.
3. The current program saved the information of each run in a simple log file. Better data tracking/visualization would be good for testing.
4. The fitness function was never adapted for use during boss fights, and there were some exploits to the fitness function that were never addressed (see issues for details).
5. If the program was able to complete a single level, I had plans to have it continue to other levels to see how well the brains generalized. If time permitted, it would be cool to watch the program learn to play the entire game. 
