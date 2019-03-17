import numpy as np
from scipy.integrate import quad
from matplotlib import pyplot as plt
def phi(x1,x2,y,z):
    return np.log(np.abs(  (x2+np.sqrt(x2**2+z**2+y**2))/(x1+np.sqrt(x1**2+z**2+y**2))  ))
    
def square_mag(X,Y,Z,x,y,z):
    int1= quad(lambda t:phi(-X/2+x,X/2+x,t+y,z-Z/2),-Y/2,Y/2)[0]
    int2= -quad(lambda t:phi(-X/2+x,X/2+x,t+y,z+Z/2),-Y/2,Y/2)[0]
  
    return int1+int2

dist=2.0
def total_phi(xx,yy,zz):
    total= square_mag(10.0,10.0,1.0,-xx,-yy,dist/2-zz)
    #total+=square_mag(10.0,10.0,1.0,-xx,-yy,-dist/2-zz)
    return total

eps=0.0001

def grad(x,y,z):
    delta=np.array([total_phi(x+eps,y,z)-total_phi(x-eps,y,z),
           total_phi(x,y+eps,z)-total_phi(x,y-eps,z),
           total_phi(x,y,z+eps)-total_phi(x,y,z-eps)])
    return delta/2.0/eps
#print(phi(-1,1,0,1))
print (square_mag(1.0,1.0,1.0,0,0,1.0))
print (total_phi(0.1,0,0))
print (grad(0,0,0))
print (grad(0,0,0.499))

x=np.linspace(-5,5,101)

#for j in range(-5,5):
def calc_plot_Bz():
    Bz=[]
    for i in range(0,101):
        Bz.append(grad(x[i],0,0)[2])
    Bz=np.array(Bz)
    Bz=Bz/np.max(np.abs(Bz))
    plt.plot(x,Bz,label=str(dist))

dist=1.2
calc_plot_Bz()
#dist= 7.5-0.5*5
#for j in range(0,11):
#    calc_plot_Bz()
#    dist+=0.5

#phi=total_phi(np.array([0,0]),np.array([0,0]),np.array([0,0]))
#phii=square_mag(1.0,1.0,1.0,np.array([0,0]),0,1.0)
#Bz=-grad(x,0,0)[3]
plt.legend()
plt.grid()
plt.show()
#print (square_mag(1.0,1.0,1.0,0,0,.001))
