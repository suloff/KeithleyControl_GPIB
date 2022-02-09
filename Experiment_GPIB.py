# -*- coding: utf-8 -*-
#date: 2010-10-21 author: susi
#Pulsing voltage and measuring current

from InstrumentControl_GPIB import *
import time
import datetime

class KeithleyExperiment(InstrumentControl):

    def __init__(self):
        InstrumentControl.__init__(self)
        self.timestring = str(datetime.datetime.now())[0:19].replace(":", "-").replace(" ", "_")
        self.filename = self.timestring + ".txt"

#########################################################
####TESTING
#########################################################
    def loginit_testing(self, channel):
        foo = open("Keithley_testing" + "_ch" + channel + "_" + self.filename, "a+")
        output = "t [sec]" + "\t" + "[muA]" + "\t" + "[V]" + "\t" + "\n"
        foo.write(output)
        foo.close()

        return(foo)

    def logdata_testing(self, foo, channel, timenow, data):
        foo = open("Keithley_testing" + "_ch" + channel + "_" + self.filename, "a+")


        #write data to file
        output = str(numpy.round(timenow,4)) + "\t" + str(numpy.round(data[0]*1e6, 4)) + "\t" + str(numpy.round(data[1], 4)) + "\n"
        foo.write(output)
        foo.close()

    def testing_sourcevoltage(self, channel, delay, runtime, timestep, potential):
        foo = self.loginit_testing(channel)
        #print("test")

        ch = self.selectChannel(channel)
        buffersize = 1

        #configure display
        #print("configure display")
        self.keithley.write("display." + ch + ".measure.func = display.MEASURE_DCAMPS")

        #create temporary reading buffer for current/voltage and specify buffersize
        self.keithley.write("buffer = " + ch + ".makebuffer( " + str(buffersize) + ")")
        self.keithley.write("buffer.appendmode = 1")
        self.keithley.write("buffer.collecttimestamps = 1")
        self.keithley.write("buffer.collectsourcevalues = 1")
        self.keithley.write("buffer.timestampresolution = 0.000001")


        #configure current/voltage measurement
        #print("configure sense/source ")
        self.keithley.write("format.data = format.ASCII")

        self.keithley.write(ch + ".measure.autorangei = " + ch + ".AUTORANGE_ON")
        self.keithley.write(ch + ".sense = " + ch + ".SENSE_LOCAL")
        self.keithley.write(ch + ".measure.count = 1")

        #configure source
        self.keithley.write(ch + ".source.func = " + ch + ".OUTPUT_DCVOLTS")
        self.keithley.write(ch + ".source.levelv = 0.0")

        self.outputON(channel)

        tzero = time.time()
        while time.time()-tzero < delay:
            self.keithley.write(ch + ".source.levelv = 0.0")
            self.keithley.write(ch + ".measure.i(buffer)")

            data = self.keithley.query_values("printbuffer(1, " + str(buffersize) + ", buffer.readings, buffer.sourcevalues, buffer.timestamps)")


            self.keithley.write("buffer.clear()")

            timenow=time.time()-tzero
            self.logdata_testing(foo, channel, timenow, data)

            time.sleep(timestep)

        while time.time()-tzero < delay+runtime:
            self.keithley.write(ch + ".source.levelv = " + str(potential))
            self.keithley.write(ch + ".measure.i(buffer)")

            data = self.keithley.ask_for_values("printbuffer(1, " + str(buffersize) + ", buffer.readings, buffer.sourcevalues, buffer.timestamps)")

            self.keithley.write("buffer.clear()")

            timenow=time.time()-tzero
            self.logdata_testing(foo, channel, timenow, data)

            time.sleep(timestep)

        #output off
        self.outputOFF(channel)

    ########################################################
    ###END TESTING
    ########################################################




    def configureKeithley_OECT(self):

        self.DrainSource = self.selectChannel("A")
        self.Gate = self.selectChannel("B")

        ##configure display
        self.keithley.write("display." + self.DrainSource + ".measure.func = display.MEASURE_DCAMPS")
        self.keithley.write("display." + self.Gate + ".measure.func = display.MEASURE_DCAMPS")

        ##define trigger timer
        self.keithley.write("timestep_timer = trigger.timer[1]")

        ##create temporary reading buffer for current/voltage and specify buffersize
        self.keithley.write("ds_buffer = " + self.DrainSource + ".makebuffer( " + str( 1 ) + ")")
        self.keithley.write("g_buffer = " + self.Gate + ".makebuffer( " + str( 1 ) + ")")

        self.keithley.write("ds_buffer.appendmode = 1")
        self.keithley.write("g_buffer.appendmode = 1")

        self.keithley.write("ds_buffer.collecttimestamps = 1")
        self.keithley.write("g_buffer.collecttimestamps = 1")

        self.keithley.write("ds_buffer.collectsourcevalues = 1")
        self.keithley.write("g_buffer.collectsourcevalues = 1")

        self.keithley.write("ds_buffer.timestampresolution = 0.000001")
        self.keithley.write("g_buffer.timestampresolution = 0.000001")

        ##configure current/voltage measurement
        self.keithley.write("format.data = format.ASCII")

        self.keithley.write(self.DrainSource + ".measure.nplc = 0.001")
        self.keithley.write(self.Gate + ".measure.nplc = 0.001")

        self.keithley.write(self.DrainSource + ".measure.autorangei = " + self.DrainSource + ".AUTORANGE_ON")
        self.keithley.write(self.Gate + ".measure.autorangei = " + self.Gate + ".AUTORANGE_ON")

        self.keithley.write(self.DrainSource + ".measure.count = 1")
        self.keithley.write(self.Gate + ".measure.count = 1")

        ##configure source
        self.keithley.write(self.DrainSource + ".source.func = " + self.DrainSource + ".OUTPUT_DCVOLTS")
        self.keithley.write(self.Gate + ".source.func = " + self.Gate + ".OUTPUT_DCVOLTS")

        self.keithley.write(self.DrainSource + ".source.levelv = 0.0")
        self.keithley.write(self.Gate + ".source.levelv = 0.0")

        ##output on
        self.outputON("A")
        self.outputON("B")

        return True

    def configureKeithley_OEIP_Sensor(self):

        self.ChanA = self.selectChannel("A")
        self.ChanB = self.selectChannel("B")

        ##configure display
        self.keithley.write("display." + self.ChanA + ".measure.func = display.MEASURE_DCVOLTS")
        self.keithley.write("display." + self.ChanB + ".measure.func = display.MEASURE_DCVOLTS")

        ##define trigger timer
        self.keithley.write("timestep_timer = trigger.timer[1]")

        ##create temporary reading buffer for current/voltage and specify buffersize
        self.keithley.write("chana_buffer = " + self.ChanA + ".makebuffer( " + str( 1 ) + ")")
        self.keithley.write("chanb_buffer = " + self.ChanB + ".makebuffer( " + str( 1 ) + ")")

        self.keithley.write("chana_buffer.appendmode = 1")
        self.keithley.write("chanb_buffer.appendmode = 1")

        self.keithley.write("chana_buffer.collecttimestamps = 1")
        self.keithley.write("chanb_buffer.collecttimestamps = 1")

        self.keithley.write("chana_buffer.collectsourcevalues = 1")
        self.keithley.write("chanb_buffer.collectsourcevalues = 1")

        self.keithley.write("chana_buffer.timestampresolution = 0.000001")
        self.keithley.write("chanb_buffer.timestampresolution = 0.000001")

        ##configure current/voltage measurement
        self.keithley.write("format.data = format.ASCII")

        self.keithley.write(self.ChanA + ".measure.nplc = 0.001")
        self.keithley.write(self.ChanB + ".measure.nplc = 0.001")

        self.keithley.write(self.ChanA + ".measure.autorangev = " + self.ChanA + ".AUTORANGE_ON")
        self.keithley.write(self.ChanB + ".measure.autorangev = " + self.ChanB + ".AUTORANGE_ON")

        self.keithley.write(self.ChanA + ".sense = " + self.ChanA + ".SENSE_LOCAL")
        self.keithley.write(self.ChanB + ".sense = " + self.ChanB + ".SENSE_LOCAL")


        self.keithley.write(self.ChanA + ".measure.count = 1")
        self.keithley.write(self.ChanB + ".measure.count = 1")

        ##configure source
        self.keithley.write(self.ChanA + ".source.func = " + self.ChanA + ".OUTPUT_DCAMPS")
        self.keithley.write(self.ChanB + ".source.func = " + self.ChanB + ".OUTPUT_DCAMPS")

        self.keithley.write(self.ChanA + ".source.leveli = 0.0")
        self.keithley.write(self.ChanB + ".source.leveli = 0.0")

        ##output on
        self.outputON("A")
        self.outputON("B")

        return True

    def runOECT(self, Vd, Vg):

        self.keithley.write(self.DrainSource + ".source.levelv = " + str(Vd))
        self.keithley.write(self.Gate + ".source.levelv = " + str(Vg))

        self.keithley.write(self.DrainSource + ".measure.i(ds_buffer)")
        self.keithley.write(self.Gate + ".measure.i(g_buffer)")

        ds_data = self.keithley.query("printbuffer(1, " +  str( 1 )  + ", ds_buffer.readings, ds_buffer.sourcevalues, ds_buffer.timestamps)")
        g_data = self.keithley.query("printbuffer(1, " +  str( 1 ) + ", g_buffer.readings, g_buffer.sourcevalues, g_buffer.timestamps)")

        self.keithley.write("ds_buffer.clear()")
        self.keithley.write("g_buffer.clear()")

        return (ds_data, g_data)

    def runOEIP_Sensor(self):

        self.keithley.write(self.ChanA + ".source.leveli = 0.0")
        self.keithley.write(self.ChanB + ".source.leveli = 0.0")

        self.keithley.write(self.ChanA + ".measure.v(chana_buffer)")
        self.keithley.write(self.ChanB + ".measure.v(chanb_buffer)")

        chana_data = self.keithley.query("printbuffer(1, " +  str( 1 )  + ", chana_buffer.readings, chana_buffer.sourcevalues, chana_buffer.timestamps)")
        chanb_data = self.keithley.query("printbuffer(1, " +  str( 1 ) + ", chanb_buffer.readings, chanb_buffer.sourcevalues, chanb_buffer.timestamps)")

        self.keithley.write("chana_buffer.clear()")
        self.keithley.write("chanb_buffer.clear()")

        return (chana_data, chanb_data)

    def stopKeithley(self):

        self.outputOFF("A")
        self.outputOFF("B")

        self.reset()
