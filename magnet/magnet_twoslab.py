import numpy as np
from scipy.integrate import quad
from matplotlib import pyplot as plt

#potenital function for a charged finite bar, 1/4*pi factor not included!
def phi(x1,x2,y,z):
    return np.log(np.abs(  (x2+np.sqrt(x2**2+z**2+y**2))/(x1+np.sqrt(x1**2+z**2+y**2))  ))

# defines a square magnet (x,y,z) are "center" coordinates, X,Y,Z are the total size
def square_mag(X,Y,Z,x,y,z):
    int1= quad(lambda t:phi(-X/2+x,X/2+x,t+y,z-Z/2),-Y/2,Y/2)[0]
    int2= -quad(lambda t:phi(-X/2+x,X/2+x,t+y,z+Z/2),-Y/2,Y/2)[0]
  
    return int1+int2

dist=2.0

# defines the arrangement of the magnets, and transforms coordinates
# here: a single centralized cube
def total_phi(xx,yy,zz):
    total= square_mag(10.0,10.0,0.01,-xx,-yy,-zz)
#    total+=square_mag(10.0,10.0,1.0,-xx,-yy,-dist-zz)
    return total

eps=0.0001

# calculates the gradient of total_phi
def grad(x,y,z):
    delta=np.array([total_phi(x+eps,y,z)-total_phi(x-eps,y,z),
           total_phi(x,y+eps,z)-total_phi(x,y-eps,z),
           total_phi(x,y,z+eps)-total_phi(x,y,z-eps)])
    return delta/2.0/eps
# test: potential is identically zero in the center of a cube magnet:
print ("test: potential in center of a cube magnet:",square_mag(1.0,1.0,1.0,0,0,0))
print ("test: field in the center of a sheet of magnet is ",np.pi*4)
print (grad(0,0,0))


# defines the arrangement of the magnets, and transforms coordinates
# here:unit cubic magnet
def total_phi(xx,yy,zz):
    total= square_mag(1,1,1,-xx,-yy,-zz)
    
    return total
ref_B=grad(0,0,0.51)[2]
print("field on the surface of unit magnet",ref_B)

# defines the arrangement of the magnets, and transforms coordinates
# two slabs of magnet, equal distance from center
def total_phi(xx,yy,zz):
    total= square_mag(10.0,10.0,1,-xx,-yy,dist-zz)
    total+=square_mag(10.0,10.0,1.0,-xx,-yy,-dist-zz)
    return total


z=np.linspace(-2.2,2.2,31)


#plots filed for x and z, distance is fixed
def calc_plot_Bz(zz):
    Bz=[]
    for i in range(0,31):
        Bz.append(grad(xx,0,z[i])[2])
    Bz=np.array(Bz)
    #Bz=Bz/np.max(np.abs(Bz))
    #Bz=Bz/np.abs(Bz[10])
    print(np.max(np.abs(Bz)))
    plt.plot(z,Bz,label=str(xx))

#dist=0.001+0.05
#calc_plot_Bz()

# distance (from center!)  is fixed to minimum fluctuation value
dist= 2.75
xx=0.0
for j in range(0,6):
    calc_plot_Bz(xx)
    xx+=1.0

#phi=total_phi(np.array([0,0]),np.array([0,0]),np.array([0,0]))
#phii=square_mag(1.0,1.0,1.0,np.array([0,0]),0,1.0)
#Bz=-grad(x,0,0)[3]
plt.legend()
plt.grid()
plt.show()
#print (square_mag(1.0,1.0,1.0,0,0,.001))
