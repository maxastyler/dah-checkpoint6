#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
data = np.loadtxt("upsilons-mass-pt-xaa.txt").flatten()

#Range to take x from = [8.5 -> 10.99]
#Take away data from 9.17 -> 9.66 and 9.84 -> 10.55

histed=np.histogram(data, bins=1000, range=[8.5, 10.99])
frequencies=histed[0]
xvalues=histed[1]

background_freqs=[]
background_xs=[]
sifted_freqs = []
sifted_xs = []

for i in range(len(xvalues)):
    if xvalues[i]>8.5 and xvalues[i]<10.99:
        sifted_freqs.append(frequencies[i])
        sifted_xs.append(xvalues[i])
        if not ((xvalues[i]>9.17 and xvalues[i]<9.66) or (xvalues[i]>9.84 and xvalues[i]<10.55)):
            background_freqs.append(frequencies[i])
            background_xs.append(xvalues[i])

def exp(x, a, b, c):
    return a*np.exp(-b*x)+c

def gaussian(x, a, b, c):
    return a*np.exp(-(x-b)**2/2*c**2)


result = scipy.optimize.curve_fit(exp, background_xs, background_freqs, p0=[0, 1, 0])

new_exp=lambda x: result[0][0]*np.exp(-result[0][1]*x)+result[0][2]


no_background = []
for i in range(len(sifted_xs)):
    no_background.append(sifted_freqs[i] - new_exp(sifted_xs[i]))

peaks=[[[], []], [[], []], [[],[]]]
for i in range(len(no_background)):
    x=sifted_xs[i]
    if x>9.25 and x<9.75:
        peaks[0][0].append(x)
        peaks[0][1].append(no_background[i])
    if x>9.75 and x<10.25:
        peaks[1][0].append(x)
        peaks[1][1].append(no_background[i])
    if x>10.25 and x<10.5:
        peaks[2][0].append(x)
        peaks[2][1].append(no_background[i])
results = []
for i in range(3):
    results.append(scipy.optimize.curve_fit(gaussian, peaks[i][0], peaks[i][1], p0=[10, 10, 10]))

plt.plot(sifted_xs, sifted_freqs)
plt.plot(sifted_xs, no_background)
calculated=[[], [], []]
for i in range(len(peaks)):
    for j in range(len(peaks[i][0])):
        calculated[i].append(gaussian(peaks[i][0][j], results[i][0][0], results[i][0][1], results[i][0][2]))

for i in range(len(peaks)):
    for j in range(len(peaks[i])):
        plt.plot(peaks[i][0], calculated[i])

plt.show()
