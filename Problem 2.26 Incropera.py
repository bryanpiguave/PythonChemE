# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 10:29:39 2021

@author: Bryan Piguave
"""
"""
 One-dimensional, steady-state conduction with uniform
internal energy generation occurs in a plane wall with a
thickness of 50 mm and a constant thermal conductivity
of 5 W/m^2 K. For these conditions, the temperature distribution has the form
, T(x) = a+bx+cx^2.
The surface at x = 0 has a temperature of 120°C and
experiences convection with a fluid for which Tinf = 20°C 
and h = 500 W/m2K. . The surface at x = L is well insulated. 

Determine the coefficients a, b, and c.
Use the results to calculate and
plot the temperature distribution.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
k = 5 #W/mK
To = 120 #°C
Tinf = 20 #°C
h = 500 #W/m^2K
L_prob= 50 #mm

### Solve the problem#### 
def solver(k,To,Tinf,h,L_prob):
    L = L_prob/1000
    q_sol = -h*(Tinf-To)/L
    b = -h*(Tinf-To)/k
    c =-b/(2*L)
    a = To
    x = np.linspace(0,L_prob,100,endpoint=True)
    x_graph=np.linspace(0,L,100,endpoint=True)
    y = a + b*x_graph + c*x_graph**2   
    return y,x,q_sol


y,x=solver(k,To,Tinf,h,L_prob)
fig,ax= plt.subplots(nrows=1,ncols=1,dpi=150,figsize=(8,6))
plt.subplots_adjust(left=0.05,bottom=0.4,hspace=0.2,right=0.95)
ax.set_title("Temperature Profile $T(x) = a+b+cx^2$",loc="center")

p,=ax.plot(x, y,linewidth=2,color="blue",alpha=0.8)
### Initial plot####
t=ax.plot(x, y,linewidth=2,color="red",alpha=0.8)
####################
plt.axis([0,50,0,max(y)*1.1])
plt.legend(["Modified","Initial values"])
ax.grid(True,alpha=0.5)

### Setting up sliders###
to_axSlider1=plt.axes([0.1,0.25,0.2,0.05])
To_slider=Slider(to_axSlider1,"T(0) [°K]",valmin=90,valmax=150,valinit=120)
k_axSlider1=plt.axes([0.1,0.16,0.2,0.05])
k_slider=Slider(k_axSlider1,"K [W/m-K]",valmin=2,valmax=8,valinit=5,color="green")
#########################

fig.text(0.7,0.20,"Made by Bryan Piguave")

#### Update Values ##### 
def val_update(val):
    Toval= To_slider.val
    kval  = k_slider.val
    yval,x,q =solver(kval,Toval,Tinf,h,L_prob) 
    p.set_ydata(yval)
    ax.set(xlim=(0, 50), ylim=(min(min(yval),min(y))*0.9, max(max(yval),max(y))*1.1))
    plt.draw()
To_slider.on_changed(val_update)
k_slider.on_changed(val_update)
plt.show()


