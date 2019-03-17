from math import *
def Zperp(Vtot=-1,V=-1,R0=-1,f=-1,silent=False,describe=False):
    if (describe):
        print('Calculating unknown value of perp impedance\n')
        print(' + ---/\\/\\/\\---| |--- g\n')
        print('Inputs: \n Vtot=total voltage\n V=voltage of unknown imp\n R0=series resistance\n f=Frequency(mhZ)\n silent=True if only data wanted\n')
        print('Units: kOhm,Mhz,pF,uH')
        return
        
    a=V/Vtot
    zperp=R0*a/sqrt(1-a*a)
    omega=f*2*pi
    c=1000.0/omega/zperp
    l=zperp/omega*1000.0
    if (not silent):
        print()
        print('Frequency {:<.3} MHz'.format(f*1.0))
        print()
        print('{:10}{:10}{:10}'.format('Z(kOhm)','C(pF)','L(uH)'))
        print('{:<10.3}{:<10.3}{:<10.3}'.format(zperp,c,l))
        print()
        
    
    return (zperp,c,l)

def LCF(L=-1,C=-1,F=-1,R=-1,describe=False):
    if (describe):
        print ('calculating, L or C or F for a resonant circuit.if all provided calculates impedance\n')
        print('inputs:')
        print('L in uH \n C in pF \n F in Mhz')
        return
    omega=F*2*pi
    if (L>0 and C>0 and F>0):
        Rlc_series= (1.0-omega**2*L*C*1e-6)/(omega*C*1e-6)
        print ('Rlc series = {:<8.7} Ohm\n'.format(Rlc_series))
        Rlc_paral=omega*L/(omega**2*L*C*1e-6-1.0)
        print ('Rlc parallel = {:<8.7} Ohm \n'.format(Rlc_paral))
        print ('R0 = {:<8.7} KOhm \n'.format(sqrt(L/C)))
        return (sqrt(L/C),Rlc_series,Rlc_paral) 
    if (L<0):
        L=1.0/omega**2/C*1e6
        print('\nL = {:<6.4} uH\n'.format(L))
        if (R>0):
            print ('for R = {:<6.4} Ohm Q = {:<8.6}'.format(R*1.0,omega*L/R))
            return L
    else:
        if (R>0 and F>0):
            print ('for R = {:<6.4} Ohm Q = {:<8.6}'.format(R*1.0,omega*L/R))
        
            
    if (C<0):
        C=1.0/omega**2/L*1e6
        print('\nC = {:<6.4} pF\n'.format(C))
        return C
    if (F<0):
        F=1.0/2/pi/sqrt(L*C)*1e3
        omega=2*pi*F
        print('\nF = {:<6.4} MHz\n'.format(F))
        if (R>0):
            print ('for R = {:<6.4} Ohm Q = {:<8.6}'.format(R*1.0,omega*L/R))
        
        return F
    
    
        
    return
