from scipy.signal import find_peaks_cwt
from scipy.signal import find_peaks

import numpy as np
from matplotlib import pyplot as plt
np.set_printoptions(precision=4)
T=100
delta=0.1
totalN=10000

normal_period=np.concatenate((np.ones(T//2),np.ones(T//2)*(-1)))
pos_period=np.concatenate((np.ones(T//2+1),np.ones(T//2)*(-1)))
neg_period=np.concatenate((np.ones(T//2),np.ones(T//2+1)*(-1)))
mul=np.int(1/delta)

large_period=np.concatenate((np.tile(normal_period,mul-1),pos_period,np.tile(normal_period,mul-1),neg_period))
print(normal_period)
#print(large_period)

signal=[]
len_beat=len(large_period)
print("beat length: ",len_beat)

while (len(signal)+len_beat<=totalN):
    signal=np.concatenate((signal,large_period))

#signal=signal[:len(signal)/1.564]

realN=len(signal)
print("total signal legnth: ",realN)

signal_placeb=[]
while (len(signal_placeb)+T<=realN):
    signal_placeb=np.concatenate((signal_placeb,normal_period))

#plt.plot(signal)
#plt.plot(signal_placeb)
#plt.grid()
#plt.show()

F=np.fft.fft(signal)/len(signal)
F=20*np.log10(np.abs(F))
F_placeb=np.fft.fft(signal_placeb)/len(signal_placeb)
F_placeb=20*np.log10(np.abs(F_placeb))
F_placeb[F_placeb<-200]=-200
F[F<-200]=-200
f_min=0.1
f_max=2.0

f=np.arange(0,len(F))/len(F)*T+delta/(T+delta)
f_placeb=np.arange(0,len(F_placeb))*T/len(F_placeb)


indices=np.argwhere((f>f_min)&(f<f_max)).flatten()

#print(F_placeb[indices])
fi=f[indices]
Fi=F[indices]
#peaks=find_peaks_cwt(Fi,1+np.zeros(len(Fi)))
peaks=find_peaks(Fi)[0]
plt.plot(f[indices],F[indices])
plt.plot(fi[peaks],Fi[peaks],'*')
for i in range(0,len(peaks)):
    print('{:8.3}'.format(fi[peaks[i]]),'{:8.3}'.format(np.max(Fi[peaks])-Fi[peaks[i]]))
plt.plot(f_placeb[indices[:-3]],F_placeb[indices[:-3]])
plt.grid()
plt.show()




