##testing with current
from Experiment_GPIB import *

channel = "B"
delay = 10
#in sec
runtime = 20
timestep = 1.0
current = 100 #in muA

KE = KeithleyExperiment ()
KE.testing_sourcecurrent(channel, delay, runtime, timestep, potential)
