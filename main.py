import time
import numpy as np
import pyvisa
import os
from scanf import scanf
import scipy.io

F_start = 3e4
F_step = 5e4
F_end = 50e5
count=1
FreqList = np.arange(F_start, F_end + 1, F_step)

# Detect the current working directory
Program_path = os.getcwd()
Exp_path = Program_path + "\\ExpData"
if not os.path.isdir(Exp_path):
    os.mkdir(Exp_path)

f = open(Exp_path+ ("\Frequency_list.txt"), "w")
f.write("%d  \n" % F_start)
f.write("%d  \n" % F_step)
f.write("%d  \n" % F_end)
f.close()
# Normal ossiloscope parameters

Transfer_size=70000
Memory_Depth=70000
Time_Scale = 0.0000015  # Time scale in seconds, 20us - gives 2G/S
Time_Offset = 0  # Time offset to fit in screen
Ch1_scale = 0.001  # Channel_1 scale
Ch2_scale = 1  # Channel_2 scale
# My Instruments ID
scope_ID = 'USB0::0x1AB1::0x04B1::DS4B141100076::INSTR'
generator_ID = 'USB0::0xF4ED::0xEE3A::SDG100E2150038::INSTR'
rm = pyvisa.ResourceManager()
scope = rm.open_resource(scope_ID)
generator = rm.open_resource(generator_ID)

#variables
#Reset the function generator and the ossiloscope
print('Resetting the devices')
scope.write('*RST')
generator.write('*RST')
time.sleep(2.0)

#OSSILOSCOPE SETTING

scope.write(":RUN")
time.sleep(0.1)
scope.write(":CHAN1:DISP 1")
time.sleep(0.1)
scope.write(":CHAN2:DISP 1")
time.sleep(0.1)
scope.write(":TIMebase:SCAL {0}".format(Time_Scale))
time.sleep(0.1)
scope.write(":TIMebase:OFFSet {0}".format(Time_Offset))
time.sleep(0.1)
scope.write(":ACQ:MDEP {0}".format(Memory_Depth))
time.sleep(0.1)
scope.write(":ACQ:TYPE NORM")
time.sleep(0.1)
scope.write(":CHAN1:COUP AC")
time.sleep(0.1)
scope.write(":CHAN1:PROB 10")
time.sleep(0.1)
scope.write(":CHAN1:IMP OMEG")  # Input impedance: 1Meg
time.sleep(0.1)
scope.write(":CHAN1:SCAL {0}".format(Ch1_scale))
time.sleep(0.1)
scope.write(":CHAN1:OFFS 0")
time.sleep(0.1)
scope.write(":CHAN2:COUP AC")
time.sleep(0.1)
scope.write(":CHAN2:PROB 0")
time.sleep(0.1)
scope.write(":CHAN2:SCAL {0}".format(Ch2_scale))
time.sleep(0.1)
scope.write(":CHAN2:IMP FIFTy")  # Input impedance: 50 Ohm
time.sleep(0.1)
scope.write('TRIG:MODE EDGE')
time.sleep(0.1)
scope.write('TRIG:EDGE:SOURCE CHAN1')
time.sleep(0.1)
scope.write('TRIG:EDGE:SLOPE POS')
time.sleep((0.1))
scope.write('TRIG:EDGE:LEVEL 0') # Considerable settings



#GENERATOR SETTING 1

generator.write("C1:BSWV WVTP,SINE")
time.sleep(0.1)
generator.write("C1:BSWV FRQ,{0}".format(F_start))
time.sleep(0.1)
generator.write("C1:BSWV AMP,0.3")
time.sleep(0.1)
generator.write("C1:BSWV OFST,0")
time.sleep(0.1)
generator.write('C1:OUTPUT ON')
time.sleep(0.1)

# Save scope parameter
# ====================================
Fs_scope = scope.query_ascii_values(':ACQ:SRAT?')[0]
time.sleep(0.1)
f = open(Exp_path + "\\ScopeVar.txt", "w")
f.write("%f \n" % Fs_scope)
f.write("%d \n" % Memory_Depth)
f.write("8 - Bits size\n")
f.write("2 - Vref\n")

f.write("%f- Time_Scale\n" % Time_Scale)
f.write("%f - Ch1_Scale\n" % Ch1_scale)
f.write("%f - Ch2_Scale\n" % Ch2_scale)
f.write("%d - Frequency count\n" % len(FreqList))
f.close()


for Freg in FreqList:
    generator.write("C1:BSWV FRQ,{0}".format(Freg))
    time.sleep(0.1)
    STAT = generator.query("C1:BSWV?")
    time.sleep(0.1)
    GenFreq = scanf("FRQ,%fHZ", STAT)[0]
    f = open(Exp_path+ ("\GenFrequencyList.txt"), "a")
    f.write("%f Frquency Range \n" % GenFreq)
    f.close()

    scope.write(":SING")
    time.sleep(2)
    # === Get channel_1 data
    scope.write(":WAV:SOUR CHAN1")
    time.sleep(0.1)
    scope.write(":WAV:MODE RAW")
    time.sleep(0.1)
    scope.write(":WAV:FORM BYTE")
    time.sleep(0.1)
    scope.write(":WAV:POIN {0}".format(Transfer_size))
    time.sleep(0.1)
    scope.write(":WAV:RES")
    time.sleep(0.1)
    scope.write(":WAV:BEG")
    time.sleep(0.1)
    ch1 = []
    while (True):
        STAT = scope.query(":WAV:STAT?")
        print(STAT)
        temp = scanf("%s,%d", STAT)
        status = temp[0]
        size = temp[1]
        time.sleep(0.1)
        if status == "READ":
            ch1.extend(scope.query_binary_values(":WAV:DATA?", datatype="B", container=np.ndarray))
            time.sleep(0.1)
        if status == "IDLE":
            if size > 0:
                ch1.extend(scope.query_binary_values(":WAV:DATA?", datatype="B", container=np.ndarray))
                time.sleep(0.1)
            scope.write(":WAV:END")
            time.sleep(0.1)
            break

    # === Get channel_2 data
    scope.write(":WAV:SOUR CHAN2")
    time.sleep(0.1)
    scope.write(":WAV:MODE RAW")
    time.sleep(0.1)
    scope.write(":WAV:FORM BYTE")
    time.sleep(0.1)
    scope.write(":WAV:POIN {0}".format(Transfer_size))
    time.sleep(0.1)
    scope.write(":WAV:RES")
    time.sleep(0.1)
    scope.write(":WAV:BEG")
    time.sleep(0.1)
    ch2 = []
    while (True):
        STAT = scope.query(":WAV:STAT?")
        temp = scanf("%s,%d", STAT)
        status = temp[0]
        size = temp[1]
        time.sleep(0.1)
        if status == "READ":
            ch2.extend(scope.query_binary_values(":WAV:DATA?", datatype="B", container=np.ndarray))
            time.sleep(0.1)
        if status == "IDLE":
            if size > 0:
                ch2.extend(scope.query_binary_values(":WAV:DATA?", datatype="B", container=np.ndarray))
                time.sleep(0.1)
            scope.write(":WAV:END")
            time.sleep(0.1)
            break
#Save as matlab compatable file
    #f = open(Exp_path + "\\ScopeVar.txt", "w")
    FN = 'E:\KTU\Sem3\Electronic measurement system\Lab1_attempt2\ExpData\Scope_data_a%d.mat' % count
    A = dict(ch1=ch1,ch2=ch2)
    scipy.io.savemat(FN, A)
    count=count+1
f = open(Exp_path+ ("\Frequency_count.txt"), "w")
f.write("%d  \n" % count)
f.close()
scope.close()
generator.close()