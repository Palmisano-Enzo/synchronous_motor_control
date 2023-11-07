#define function to compute OC v1, v2 and v3 from a .csv file of measured data
#input: .csv file of measured data, rpm, current field, windows size
#output: v1, v2, v3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def computeOC(data, rpm, currentField, windowSize):
    measurements = pd.read_csv(data)

    #compute time column
    increment = measurements['Increment'][0]
    time = np.linspace(0, increment*(len(measurements)-2), len(measurements)-1)

    #remove line 0 of measurements_1
    measurements = measurements.drop(0)
    #remove coloum X, Start, Increment and Unnamed: 5
    measurements = measurements.drop(columns=['X', 'Start', 'Increment', 'Unnamed: 6'])

    #add time column
    measurements['Time'] = time

    #transform column CH1, CH2 and CH3 to float
    measurements['CH1'] = measurements['CH1'].astype(float)
    measurements['CH2'] = measurements['CH2'].astype(float) 
    measurements['CH3'] = measurements['CH3'].astype(float)

    #apply a low pass filter to the CH1, CH2 and CH3
    measurements['CH1_filter'] = measurements['CH1'].rolling(window=windowSize).mean()
    measurements['CH2_filter'] = measurements['CH2'].rolling(window=windowSize).mean()
    measurements['CH3_filter'] = measurements['CH3'].rolling(window=windowSize).mean()

    #compute efficace value of sinusoidal signal CH1, CH2 and CH3 filter
    v1 = np.max(measurements['CH1_filter'])/math.sqrt(2)
    v2 = np.max(measurements['CH2_filter'])/math.sqrt(2)
    v3 = np.max(measurements['CH3_filter'])/math.sqrt(2)


    #Figure of 2 plots
    fig, axs = plt.subplots(1, 2, figsize=(15, 8))

    #plot the CH1, CH2 and CH3 in function of time
    axs[0].plot(measurements['Time'], measurements['CH1'], label='CH1')
    axs[0].plot(measurements['Time'], measurements['CH2'], label='CH2')
    axs[0].plot(measurements['Time'], measurements['CH3'], label='CH3')

    #set labels and title
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Voltage (V)')
    axs[0].set_title('Measurements of open-circuit voltage, rotor drive at ' + str(rpm) + 'rpm and If = ' + str(currentField) + 'A')

    #set legend and grid
    axs[0].legend()
    axs[0].grid()

    #plot the CH1, CH2 and CH3 filter in function of time
    axs[1].plot(measurements['Time'], measurements['CH1_filter'], label='CH1 filter')
    axs[1].plot(measurements['Time'], measurements['CH2_filter'], label='CH2 filter')
    axs[1].plot(measurements['Time'], measurements['CH3_filter'], label='CH3 filter')

    #set labels and title
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Voltage (V)')
    axs[1].set_title('Measurements of open-circuit voltage filter, rotor drive at '  + str(rpm) +  'rpm and If = ' + str(currentField) + 'A')

    #set legend and grid
    axs[1].legend()
    axs[1].grid()

    fig.tight_layout()

    #return data
    return v1, v2, v3


