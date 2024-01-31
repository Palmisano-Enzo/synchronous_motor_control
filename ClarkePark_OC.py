#define function to compute OC vds and vqs from a .csv file of measured data
#input: .csv file of measured data, windows size, rpm, current field, wt and delta
#output: v1, v2, v3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def clarkePark (data, rpm, currentField, windowSize, wt, delta):
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

    #we need to find wt and delta 
    measurements['vfit'] = measurements.apply(lambda row: measurements['CH1_filter'].max()*math.cos(wt*row['Time']+delta), axis=1)

    measurements[['Valpha', 'Vbeta', 'V0']] = measurements.apply(lambda row: abc_to_alphaBeta0(row['CH1_filter'], row['CH2_filter'], row['CH3_filter']), axis=1,result_type='expand')

    measurements['Vds'] = measurements.apply(lambda row: row['Valpha']*math.cos(wt*row['Time']+delta) + row['Vbeta']*math.sin(wt*row['Time']+delta), axis=1, result_type='expand')
    measurements['Vqs'] = measurements.apply(lambda row: -row['Valpha']*math.sin(wt*row['Time']+delta) + row['Vbeta']*math.cos(wt*row['Time']+delta), axis=1, result_type='expand')

    #3 subplots
    fig, axs = plt.subplots(3, 1, figsize=(15, 8))
    
    # 1 plot vfit and CH1 vs time
    axs[0].plot(measurements['Time'], measurements['vfit'], label='vfit')
    axs[0].plot(measurements['Time'], measurements['CH1_filter'], label='CH1 filter')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Voltage (V)')
    axs[0].legend()

    # 2 plot Valpha, Vbeta and V0 vs time
    axs[1].plot(measurements['Time'], measurements['Valpha'], label='Valpha')
    axs[1].plot(measurements['Time'], measurements['Vbeta'], label='Vbeta')
    axs[1].plot(measurements['Time'], measurements['V0'], label='V0')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Voltage (V)')
    axs[1].legend()

    # 3 plot Vds and Vqs vs time
    axs[2].plot(measurements['Time'], measurements['Vds'], label='Vqs')
    axs[2].plot(measurements['Time'], measurements['Vqs'], label='Vds')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Voltage (V)')
    axs[2].legend()

    #set title
    fig.suptitle('Clarke-Park transform, rotor drive at ' + str(rpm) + 'rpm and If = ' + str(currentField) + 'A')

    #figure rescale
    fig.tight_layout()

    #return Vds mean and Vqs mean
    return measurements['Vds'].mean(), measurements['Vqs'].mean()
    


def abc_to_alphaBeta0(a, b, c):
  alpha = (2/3)*(a - b/2 - c/2)
  beta  = (2/3)*(np.sqrt(3)*(b-c)/2)
  z     = (2/3)*((a+b+c)/2)
  return alpha, beta, z