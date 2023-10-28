#define function to compute Rf and Lf from a .csv file of measured data
#input: .csv file of measured data
#output: plot, tau, USteadySate, ISteadyState, t0, t5, Rf and Lf
#example: Rf, Lf = computeFieldCaracteristic('data.csv')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def computeFieldCharacteristic(data, axs):
    #read data
    measurements = pd.read_csv(data)

    #compute time column
    increment = measurements['Increment'][0]
    time = np.linspace(0, increment*(len(measurements)-2), len(measurements)-1)

    #remove line 0 of measurements_1
    measurements = measurements.drop(0)
    #remove coloum X, Start, Increment and Unnamed: 5
    measurements = measurements.drop(columns=['X', 'Start', 'Increment', 'Unnamed: 5'])

    #add time column
    measurements['Time'] = time

    #colum CH1 and CH1 to float
    measurements['CH1'] = measurements['CH1'].astype(float)
    measurements['CH2'] = measurements['CH2'].astype(float) 

    #compute Rf
    meanUSteadyState = measurements[measurements['Time'] >= 5.95]['CH1'].mean()
    meanISteadyState = measurements[measurements['Time'] >= 5.95]['CH2'].mean()

    #plot CH1 and CH2 in function of time
    ax2 = axs.twinx()
    axs.plot(measurements['Time'], measurements['CH1'], label='CH1', color='blue')
    ax2.plot(measurements['Time'], measurements['CH2'], label='CH2', color='red')
    axs.set_xlabel('Time (s)')
    axs.set_ylabel('Voltage (V)', color='blue')
    ax2.set_ylabel('Current (A)', color='red')
    axs.set_title('Field characteristic U = ' + str(round(meanUSteadyState,2)) + 'V')
    ax2.set_ylim(-meanISteadyState/6, meanISteadyState*1.5)

    Rf = meanUSteadyState/meanISteadyState

    #compute Lf

    #t0 is when CH1 is turn on
    t0 = measurements[(measurements['CH1'] >= 2.5)].iloc[0]['Time']

    #t5 is when CH2 is bigger than meanISteadyState - 0.7%
    t5 = measurements[(measurements['CH2'] >= meanISteadyState*(1 - 0.007))].iloc[0]['Time']

    tau = (t5 - t0)/5

    Lf = Rf*tau

    return tau, meanUSteadyState, meanISteadyState, t0, t5, Rf, Lf

fig, axs = plt.subplots(1, 1)

tau, meanUSteadyState, meanISteadyState, t0, t5, Rf, Lf = computeFieldCharacteristic('Data/FieldMeasure_1.csv', axs)

print('tau = ', tau)
