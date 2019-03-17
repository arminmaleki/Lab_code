import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
table=pd.read_csv('a66_l2_4.csv',skiprows=1)
print(table.head())
crop=200
values=table.values[crop:-crop,:2]
res=4
deltat=(len(values)-1)/1000*res
#deltat=(table.values[-crop,0]-table.values[crop,0])*1e6

print(values[:25,:])
#print("delta t real:",deltat/(len(table.values[:,0]-2*crop)))
print(values.shape)

#plt.plot(values[:100])
#plt.title('Does the beginning look good?')
#plt.show()

#plt.plot(values[-100:])
#plt.title('Does the end look good?')
#plt.show()
val=values[:,1]

def hamming(n,L):
    return 0.54-0.46*np.cos(2*np.pi*n/(L-1))

vall_eff=val*hamming(np.arange(0,len(val)),len(val))
#plt.plot(val[1000:1200])
print(np.sum(val[1000:1200]))
#plt.show()

f=np.fft.fft(vall_eff)
w=np.arange(0,len(f))/deltat
    
    
f=f*hamming(np.arange(0,len(f)),len(f))
spec=np.abs(f)
plt.plot(spec)
plt.title('ful spec')
plt.show()
tc=np.fft.fft(spec**2)
center=int(len(f)/2)
print("len(f)/2:",center)
ind=np.argmax(spec[1000:300000])+1000
maxim=np.max(spec[1000:300000])
print(ind,w[ind],spec[ind],maxim)
d=int(np.sqrt(len(f))/40)

plt.scatter(w[ind-d:ind+d],spec[ind-d:ind+d],label="Data")
plt.grid()


def gauss(x,x0,sig,a):
    #return a*np.exp(-(x-x0)**2/2/sig**2)
    return a*sig**2/((x-x0)**2+sig**2)

w2=np.linspace(w[ind-d],w[ind+d],101)

gauss0=gauss(w2,w[ind]-0.05,0.05,maxim)
plt.plot(w2,gauss0,label="guessed")
param=curve_fit(gauss,w[ind-d:ind+d],spec[ind-d:ind+d],[w[ind],0.05,maxim])
gauss1=gauss(w2,*param[0])
print(type(gauss1))
print(param[0])
plt.plot(w2,gauss1,label="fitted")

plt.legend(loc="best")
plt.show()

#plt.plot(tc)
#plt.show()


