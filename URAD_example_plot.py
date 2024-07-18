import uRAD_USB_SDK11 # import uRAD library
import serial
from time import time, sleep
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, fftshift, fftfreq
import datetime
import time
# import timeit


# type "ls /dev/tty*" in terminal to find com port
# True if USB, False if UART
usb_communication = True

# # input parameters
# mode = 2 # sawtooth mode
# f0 = 5 # starting at 24.005 GHz
# BW = 10 # using all the BW available = 240 MHz
# Ns = 200 # 200 samples
# Ntar = 3 # 3 target of interest
# 19
# Rmax = 10 # searching along the full distance range
# MTI = 0 # MTI mode disable because we want information of static and moving targets
# Mth = 0 # parameter not used because "movement" is not requested
# Alpha = 10 # signal has to be 10 dB higher than its surrounding
# distance_true = True # Request distance information
# velocity_true = False # mode 2 does not provide velocity information
# SNR_true = True # Signal-to-Noise-Ratio information requested
# I_true = True # In-Phase Component (RAW data) not requested
# Q_true = True # Quadrature Component (RAW data) not requested
# movement_true = False # Not interested in boolean movement detection

# input parameters
mode = 1 # sawtooth mode
f0 = 5 # starting at 24.005 GHz
BW = 240 # using all the BW available = 240 MHz
Ns = 200 # 200 samples
Ntar = 3 # 3 target of interest


Rmax = 10 # searching along the full distance range
MTI = 0 # MTI mode disable because we want information of static and moving targets
Mth = 0 # parameter not used because "movement" is not requested
Alpha = 10 # signal has to be 10 dB higher than its surrounding
distance_true = False # Request distance information
velocity_true = False # mode 2 does not provide velocity information
SNR_true = False # Signal-to-Noise-Ratio information requested
I_true = True # In-Phase Component (RAW data) not requested
Q_true = True # Quadrature Component (RAW data) not requested
movement_true = False # Not interested in boolean movement detection

Fs = 200000 # Infineon microcontroller
Fs_CW = 25000
max_voltage = 3.3
ADC_bits = 12
ADC_intervals = 2**ADC_bits

Nm_CW = 200
f_0 = 24.005
SpeedUnits_Selected = 1


N_FFT = 4096
c = 299792458
max_velocity = c/(2*f_0*1000000000) * (Fs_CW/2)
# SpeedUnits_Selected = self.SpeedUnits_CW.currentIndex()
if (SpeedUnits_Selected == 1):
    SpeedFactor = 3.6
    max_velocity *= SpeedFactor
    x_axis_label = 'Velocity (km/h)'
    # self.label_MaximumSpeed.setText('Maximum Velocity (km/h)')
elif (SpeedUnits_Selected == 2):
    SpeedFactor = 2.23694
    max_velocity *= SpeedFactor
    x_axis_label = 'Velocity (mph)'
    # self.label_MaximumSpeed.setText('Maximum Velocity (mph)')
else:
    SpeedFactor = 1
    x_axis_label = 'Velocity (m/s)'
    # self.label_MaximumSpeed.setText('Maximum Velocity (m/s)')


# Serial Port configuration
ser = serial.Serial()
if (usb_communication):
    # ser.port = 'COM8'
    ser.port='/dev/tty.usbmodem1101'

    ser.baudrate = 1e6
else:
    ser.port='/dev/tty.usbmodem1101'
    ser.baudrate = 115200
# Sleep Time (seconds) between iterations
timeSleep = 5e-3

# Other serial parameters
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE

# Method to correctly turn OFF and close uRAD
def closeProgram():
    # switch OFF uRAD
    return_code = uRAD_USB_SDK11.turnOFF(ser)
    if (return_code != 0):
        print(return_code)
        exit()

# Open serial port
try:
    ser.open()
except:
    closeProgram()

# switch ON uRAD
return_code = uRAD_USB_SDK11.turnON(ser)
if (return_code != 0):
    closeProgram()
if (not usb_communication):
    sleep(timeSleep)
# loadConfiguration uRAD
# def loadConfiguration(ser, mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth, Alpha, distance_true, velocity_true, SNR_true, I_true, Q_true, movement_true):
return_code = uRAD_USB_SDK11.loadConfiguration(ser, mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth, Alpha, distance_true, velocity_true, SNR_true, I_true, Q_true, movement_true)
if (return_code != 0):
    closeProgram()
if (not usb_communication):
    sleep(timeSleep)

plt.ion()

figure, ax = plt.subplots(figsize=(10, 8))

line1, = ax.plot([], [])
# line2, = ax.plot(np.empty(200),np.empty(200))
ax.set_ylim(-150, 0)
ax.set_xlim(0, 100)

time_per_readings = []
# while True:
for i in range(1000):

    # read I and Q values from the URAD
    start_time = time.time()
    return_code, results, raw_results = uRAD_USB_SDK11.detection(ser)
    end_time = time.time()
    time_per_readings.append(end_time-start_time)

    # print(end_time-start_time)

    #extract the raw data      
    I = raw_results[0]
    Q = raw_results[1]

    # Offset and scale data
    I = np.subtract(np.multiply(I, 1/ADC_intervals), np.multiply(2048, 1/ADC_intervals))
    Q = np.subtract(np.multiply(Q, 1/ADC_intervals), np.multiply(2048, 1/ADC_intervals))

    # I = np.subtract(np.multiply(I, max_voltage/ADC_intervals), 2048)
    # Q = np.subtract(np.multiply(Q, max_voltage/ADC_intervals), 2048)

    # Clear the graph and plot I and Q signals
    x_axis = np.linspace(1, len(I), num = len(I))
    
    ComplexVector = I + 1j*Q

    # Apply the selected window to the complex vector previous to the FFT calculation
    ComplexVector = ComplexVector * np.hanning(Nm_CW) * 2 / 3.3

    FrequencyDomain = 2*np.absolute(fftshift(fft(ComplexVector/Nm_CW, N_FFT)))

    f_axis = fftshift(np.fft.fftfreq(N_FFT, d=1/Fs_CW))
    x_axis = c/(2*f_0*1e9)*f_axis

    FrequencyDomain[int(N_FFT/2)] = FrequencyDomain[int(N_FFT/2) - 1]
    FrequencyDomain = 20 * np.log10(FrequencyDomain)

    line1.set_data(x_axis, FrequencyDomain)

    figure.canvas.draw()
    figure.canvas.flush_events()
    
    try:
        pass

    except KeyboardInterrupt:
        plt.close()
        closeProgram()

print(np.mean(time_per_readings))
print(np.min(time_per_readings))
print(np.max(time_per_readings))

