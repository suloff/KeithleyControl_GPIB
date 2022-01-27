#date: 2010-10-21 author: susi
#Pulsing voltage and measuring current
import string
import numpy
import time
import datetime

from InstrumentUtils_GPIB import *

class InstrumentControl(InstrumentUtils):

    ivamplitude = 0

    def __init__(self):
        InstrumentUtils.__init__(self)
        self.ivamplitude = InstrumentControl.ivamplitude

    def initVoltageSourceing(self, channel):
        smu = self.selectChannel(channel)
        self.configBuffers(channel)
        self.configMeasurement(channel)
        self.configVoltageSource(channel)

    def initCurrentSourceing(self, channel):
        smu = self.selectChannel(channel)
        self.configBuffers(channel)
        self.configMeasurement(channel)
        self.configCurrentSource(channel)

    def runMeasurement(self, channel, file, t):
        start = time.clock()
        channelcounter = 0
        vdata = self.measureVoltage(1, channel)
        idata = self.measureCurrent(1, channel)
        line = string.strip(string.strip(str(numpy.hstack((t, vdata, idata))), "]"), "[")+"\n"
        file.write(line)
        channelcounter = channelcounter + 1
        end = time.clock()
        runtime = end-start
        #print(runtime)
        return(runtime)

    def startDevice(self, channel, sourcemode):
        if sourcemode == "current source":
            self.initCurrentSourceing(channel)
            self.outputON(channel)
        elif sourcemode == "voltage source":
                self.initVoltageSourceing(channel)
                self.outputON(channel)
        else:
            print("invalid sourcemode option")

    def stopChannel(self, channel):
        self.outputOFF(channel)
        self.resetWorkingChannel(channel)

    def stopDevice(self):
        self.outputOFF("smua")
        self.outputOFF("smub")
        self.resetWorkingChannel("smua")
        self.resetWorkingChannel("smub")

    def stopAll(self):
        self.resetStatus()
        self.reset()

    def initFile(self, channel):
        timestring = str(datetime.datetime.now())[0:19].replace(":", "-").replace(" ", "_")
        filename = "Keithley_" + channel + "_" + timestring + ".txt"
        file = open(filename, "a+")

        return(file, filename)

    def closeFile(self, file):
        file.close()

    def runOf(self, channel, file, offset, timestep, m_counter):
        offset_m = int(offset/timestep)
        for m in range(offset_m):
            t = m_counter*timestep
            runtime = self.runMeasurement(channel, file, t)
            if (timestep-runtime) < 0:
                time.sleep(0)
                print("Warning: execution time larger than timestep")
            else:
                time.sleep(timestep-runtime)
            m_counter = m_counter + 1
        return(m_counter)

    def runWaveformCycle(self, channel, file, offset, timestep, waveform, m_counter):
        offset_m = int(offset/timestep)
        for m in range(offset_m):
            t = m_counter*timestep
            runtime = self.runMeasurement(channels, files, t)
            if (timestep-runtime) < 0:
                time.sleep(0)
                print("Warning: execution time larger than timestep")
            else:
                time.sleep(timestep-runtime)
            m_counter = m_counter + 1
        return(m_counter)
