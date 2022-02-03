
#date: 2010-10-21 author: susi
#Pulsing voltage and measuring current

import pyvisa as visa

class InstrumentUtils:
    """Instrument utilities to control Keithley2602"""

    portID = u'GPIB0::26::INSTR'

    def __init__(self):
        self.portID = InstrumentUtils.portID
        self.keithley = self.connectToKeithley()
        self.reset()
        self.resetStatus()

    def connectToKeithley(self):
        rm = visa.ResourceManager()
        keithley = rm.open_resource(self.portID)
        print(keithley.query("*IDN?"))
        return(keithley)

    def reset(self):
        self.keithley.write("reset()")
        self.keithley.write("waitcomplete()")

    def resetStatus(self):
        self.keithley.write("status.reset()")
        self.keithley.write("waitcomplete()")

    def selectChannel(self, channel):
        if channel == "B":
            smu = "smub"
        elif channel == "A":
            smu = "smua"
        else:
            smu = "smua"
            print("using channel A")
        return smu

    def resetWorkingChannel(self, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".reset()")
        self.keithley.write("waitcomplete()")

    def configBuffers(self, channel):
        smu = self.selectChannel(channel)
        for buffer in (1, 2):
            self.keithley.write("rb" + str(channel) + str(buffer) + " = " + smu + ".nvbuffer" + str(buffer))
            self.keithley.write("waitcomplete()")
            self.keithley.write("rb" + str(channel) + str(buffer) + ".clear()")
            self.keithley.write("waitcomplete()")
            self.keithley.write("rb" + str(channel) + str(buffer) + ".appendmode = 1")
            self.keithley.write("waitcomplete()")
            self.keithley.write("rb" + str(channel) + str(buffer) + ".collecttimestamps = 1")
            self.keithley.write("waitcomplete()")
            self.keithley.write("rb" + str(channel) + str(buffer) + ".collectsourcevalues = 1")
            self.keithley.write("waitcomplete()")

    def clearBuffer(self, channel, buffer):
        smu = self.selectChannel(channel)
        self.keithley.write("rb" + str(channel) + str(buffer) + ".clear()")
        self.keithley.write("waitcomplete()")

    def configMeasurement(self, channel):
        smu = self.selectChannel(channel)
        if smu == "smub":
            s = "SMUB"
        else:
            s = "SMUA"
        #self.keithley.write("status.measurement.reading_overflow.enable = status.measurement.reading_overflow." + s)
        #self.keithley.write("waitcomplete()")
        self.keithley.write("status.measurement.enable = status.measurement.OUTPUT_ENABLE")
        self.keithley.write("waitcomplete()")
        #self.keithley.write("status.request_enable = status.OSB")
        #self.keithley.write("waitcomplete()")
        self.keithley.write(smu + ".measure.autorangei = " + smu + ".AUTORANGE_ON")
        self.keithley.write("waitcomplete()")
        self.keithley.write(smu + ".measure.autorangev = " + smu + ".AUTORANGE_ON")
        self.keithley.write("waitcomplete()")
        #self.keithley.write(smu + ".measure.count =" + str(buffer_n+1))
        #self.keithley.write("waitcomplete()")
        self.keithley.write(smu + ".measure.count =" + str(1))
        self.keithley.write("waitcomplete()")
        #self.keithley.write(smu + ".measure.interval =" + str(timestep))
        #self.keithley.write("waitcomplete()")
        self.keithley.write(smu + ".measure.nplc =" + str(1))
        self.keithley.write("waitcomplete()")

    def configVoltageSource(self, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".source.func = " + smu + ".OUTPUT_DCVOLTS")
        self.keithley.write("waitcomplete()")
        self.keithley.write(smu + ".source.autorangev = " + smu + ".AUTORANGE_ON")
        self.keithley.write("waitcomplete()")

    def configCurrentSource(self, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".source.func = " + smu + ".OUTPUT_DCAMPS")
        self.keithley.write("waitcomplete()")
        self.keithley.write(smu + ".source.autorangei = " + smu + ".AUTORANGE_ON")
        self.keithley.write("waitcomplete()")

    def setVoltageLevel(self, voltage, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".source.levelv = " + str(voltage))
        self.keithley.write("waitcomplete()")

    def setCurrentLevel(self, current, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".source.leveli = " + str(current))
        self.keithley.write("waitcomplete()")

    def measureCurrent(self, buffernum, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".measure.i(" + "rb" + str(channel) + str(buffernum) + ")")
        self.keithley.write("waitcomplete()")
        data = self.keithley.ask_for_values("printbuffer(1, " + str(1) + ", rb" + str(channel) + str(buffernum)+ ")")
        self.keithley.write("waitcomplete()")
        self.clearBuffer(channel, buffernum)
        return(data)

    def measureVoltage(self, buffernum, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".measure.v(" + "rb" + str(channel) + str(buffernum) + ")")
        #self.keithley.write("waitcomplete()")
        data = self.keithley.ask_for_values("printbuffer(1, " + str(1) + ", rb" + str(channel) + str(buffernum)+ ")")
        #self.keithley.write("waitcomplete()")
        self.clearBuffer(channel, buffernum)
        return(data)

    def outputON(self, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".source.output = " + smu + ".OUTPUT_ON")
        self.keithley.write("waitcomplete()")

    def outputOFF(self, channel):
        smu = self.selectChannel(channel)
        self.keithley.write(smu + ".source.output = " + smu + ".OUTPUT_OFF")
        self.keithley.write("waitcomplete()")
