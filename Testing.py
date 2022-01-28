##testing with current
from Experiment_GPIB import *

channel = "B"
delay = 10
#in sec
runtime = 20
timestep = 1.0
potential = 1 #in V

KE = KeithleyExperiment ()
KE.testing_sourcevoltage(channel, delay, runtime, timestep, potential)
