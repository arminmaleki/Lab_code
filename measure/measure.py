import numpy as np
import pandas as pd
import usbtmc
from matplotlib import pyplot as plt
import struct
import time
from scipy.signal import find_peaks

class Rigol:
    """manages rigol oscilloscope"""
    def __init__(self):
         self.instr=usbtmc.Instrument(6833,1416)
         print(self.instr.ask("*IDN?"))
         print(self.instr.ask(":CHAN1:MEMD?"))

    def  retrieve(self,channel=1):
           self.instr.ask(":STOP",wait_reply=False)
           self.sample_rate=np.float(self.instr.ask(':ACQ:SAMP?'))
           print('Sample rate %f'%self.sample_rate)
           time.sleep(0.1)
           self.volt_scale=np.float(self.instr.ask(':CHAN'+str(channel)+':SCAL?'))
           print('Voltage scale is %f'%self.volt_scale)
           time.sleep(2.0)
           # for some strange reasons we are better of if we :RUN first!
           self.instr.ask(":RUN",wait_reply=False)
           raw_data=self.instr.ask_raw(bytes(":WAV:DATA? CHAN"+str(channel),'utf-8'))
           self.data=struct.unpack("B"*len(raw_data),raw_data)
           #getteing rid of meta-data
           self.data=self.data[20:-1]
           #taking caring of Rigole craziness!
           self.data=(255-np.array(self.data))*self.volt_scale/25
     

      
class Spectrum:
    """Manages spectrum data"""
    def __init__(self,data=[],sample_rate=1.0,max_freq=-1,peak_distance=0,file_name='spec_default',from_file=False):
        if (not from_file):
            self.sample_rate=sample_rate
            self.total_acq_time=len(data)/sample_rate
            #self.freq is the frequenct mesh
            self.freq=np.arange(0,len(data))/self.total_acq_time
            print ("min freq(precision): %f"%(self.freq[1]))
            self.min_freq=self.freq[1]
            print ("max freq: %f"%(self.freq[-1]))
            if (max_freq>0):
                self.n_max=np.int(max_freq/self.freq[1])
                self.max_freq=self.freq[self.n_max]            
            else:
                self.n_max=len(self.freq)
                self.max_freq=self.freq[-1]
            print("n_max %f"%self.n_max)
            print("max_freq %f"%self.max_freq)
            ham_mask=hamming(np.arange(0,len(data)),len(data))
            self.spec=np.fft.fft(data*ham_mask)/len(data)
            self.spec=np.abs(self.spec[2:self.n_max])
            self.freq=self.freq[2:self.n_max]
            to_file=pd.DataFrame(np.array([self.freq,self.spec*2]).T,columns=['freq(Hz)','voltage'])
            to_file.to_csv(file_name+'.csv')
        else:
            from_file=pd.read_csv(file_name+'.csv')
            self.spec=from_file['voltage'].values/2
            self.freq=from_file['freq(Hz)'].values
            self.min_freq=self.freq[1]-self.freq[0]
            self.sample_rate=1.0/self.min_freq
            self.n_max=len(self.freq)
            self.max_freq=self.freq[-1]
            
        if (peak_distance>0):
            n_distance=np.int(peak_distance/self.min_freq)+1
            print(n_distance)
            self.peaks=find_peaks(self.spec,distance=n_distance)[0]
        
            real_v=self.spec[self.peaks]*0
            for i in range(-n_distance//2-1,n_distance//2+1):
                ind=self.peaks+i
                ind[ind<0]=0
                ind[ind>len(self.spec)-1]=len(self.spec)-1
                real_v+= self.spec[ind]**2
            real_v=2*np.sqrt(real_v)
            V0=np.sqrt(0.001*50.0*2)
            self.peaks_frame=pd.DataFrame(np.array([self.freq[self.peaks],self.spec
                                   [self.peaks]*2,real_v,
                                       20*np.log10(real_v/V0)]
                                     ).T,columns=['freq(Hz)','strength','real_v','dBmW'])
            self.peaks_frame=self.peaks_frame.sort_values(by=['real_v'],ascending=False)
            self.peaks_frame['rel_freq']=self.peaks_frame['freq(Hz)']/self.peaks_frame['freq(Hz)'].iloc[0]
            self.no_peaks=False
        else:
            self.no_peaks=True
    
        self.plot()
    def plot(self,output='spec_default.png',min_freq=-1,max_freq=-1):
        if (min_freq>=0 and max_freq>=0):
            freq=self.freq[np.logical_and((self.freq>=min_freq) , (self.freq<=max_freq))]
            spec=self.spec[np.logical_and((self.freq>=min_freq) , (self.freq<=max_freq))]
        else:
            freq=self.freq
            spec=self.spec
            
        plt.plot(freq,spec*2) #*2 because we want "peak" voltages,sum of two + - freq components
        plt.xlabel('freq')
        plt.ylabel('Volt-p')
        plt.grid()
        if (not self.no_peaks):
            some_peaks=self.peaks_frame[:min(20,np.shape(self.peaks_frame)[0])]
            if (min_freq>=0 and max_freq>=0):
                some_peaks=some_peaks.loc[np.logical_and((some_peaks['freq(Hz)']>=min_freq), (some_peaks['freq(Hz)']
                                                                                  <=max_freq))]
                
            plt.plot(some_peaks['freq(Hz)'],some_peaks['strength'],'*')
        plt.savefig(output)
    
    def optimize_peak(self,width,ind=0,plot=True):
        peak=self.peaks_frame.iloc[ind]
        ind_peak=np.int(peak['freq(Hz)']//self.min_freq-2)
        ind_begin=np.int(max(0,ind_peak-width//self.min_freq-2))
        ind_end=np.int(min(ind_peak+width//self.min_freq+1-2,len(self.freq)-1))
        w=self.freq[ind_begin:ind_end]
        spd=self.spec[ind_begin:ind_end]**2
        
        
        #lorenz0=lorenz(w2,w[len(w)//2],10*self.min_freq,spd[len(spd)//2]/2)
        #plt.plot(w2/np.pi/2,np.sqrt(lorenz0),label="guessed",color='orange')
        param=curve_fit(lorenz,w,spd,[w[len(w)//2],2*self.min_freq,spd[len(spd)//2]/2],maxfev=10000)
        if (plot):
            w2=np.linspace(w[0],w[-1],101)
            lorenz2=lorenz(w2,*param[0])
            plt.bar(self.freq[ind_begin:ind_end],self.spec[ind_begin:ind_end],color='grey')
            plt.grid()
            plt.plot(w2,np.sqrt(lorenz2),label="guessed",color='red')
        out=pd.Series([param[0][0],param[0][1]],index=['freq(Hz)','width'])
        print(param[0][0],param[0][1])
        return out
    
    def optimize(self,width,number=10):
        self.opt_peak=self.peaks_frame[:number]
        for i in range(0,number):
            s=self.optimize_peak(width,i,plot=False)
            
            self.opt_peak.iloc[i]['freq(Hz)']=s['freq(Hz)']
            self.opt_peak.iloc[i]['width']=s['width']
        for i in range(0,number):
            self.opt_peak.iloc[i]['rel_freq']=self.opt_peak.iloc[i]['freq(Hz)']/self.opt_peak.iloc[0]['freq(Hz)']
                                
        return self.opt_peak    
    
    



def hamming(n,L):
    return 0.54-0.46*np.cos(2*np.pi*n/(L-1))

instr=Rigol()
instr.retrieve()
print(len(instr.data))
spec=Spectrum(instr.data,instr.sample_rate,10000.0,10)
print (spec.peaks_frame[:20])




