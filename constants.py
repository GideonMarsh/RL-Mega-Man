# Gideon Marsh
# github.com/GideonMarsh

# SCREENRATIO = 1.333
XPIXELS = 60
YPIXELS = 45

WINDOWNAME = 'Mega Man Legacy Collection'

SAVE_FILE_NAME = 'saves/recent.pkl'
SAVE_FOLDER = 'saves/air_man/'

#Time is measured in seconds
TOTAL_TIMEOUT = 600
PROGRESS_CHECK_EARLY_TIMEOUT = 3
PROGRESS_CHECK_TIMEOUT = 7
PROGRESS_CHECK_COMPARE_INTERVAL = 3
CONTROL_TIMEOUT = 6

#The percentage of a checkpoint image that is allowed to not match
IMAGE_ACCEPTABLE_ERROR = 0.01

CONTROL_FITNESS_PENALTY = 0.2

CONTROLLER_OUTPUTS = 6

POPULATION_SIZE = 100
WEIGHT_MUTATION_CHANCE = 0.4
STRUCTURAL_MUTATION_CHANCE = 0.2

STARTING_DELTA = 10

# The best percentage of each species that are qualified to breed
ACCEPTABLE_PARENTS_PERCENTAGE = 0.4

LOG_FILE_NAME = 'logs/Generation_Log.txt'
