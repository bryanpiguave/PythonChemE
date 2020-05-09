# -*- coding: utf-8 -*-
"""
Created on Sun May  3 21:53:18 2020
Youtube link: https://youtu.be/oMxMkROfBZk
@author: Bryan Piguave Llano
"""

from iapws import IAPWS97


P_1 = 0.075 #MPa
X_1 = 0

estado_1 = IAPWS97(P=P_1,x=X_1)

v1= estado_1.v  #m^3/kg
h1= estado_1.h  #KJ/kg
s1= estado_1.s  #KJ/kg-K

P_2 = 3 #MPa
estado_2 = IAPWS97(P = P_2,s=s1)
h2=estado_2.h

W_bomba = v1*(P_2 - P_1)*1000 #KJ/Kg

P_3 = 3 #Mpa
T_3 = 350 + 273.15 #K

estado_3 =IAPWS97(P=P_3,T=T_3) 
h3 = estado_3.h
s3 = estado_3.s

estado_4 = IAPWS97(P=P_1,s = s3)
h4 = estado_4.h

W_bomba = v1*(P_2 - P_1)*1000 #KJ/Kg
Q_entrada = h3-h2 
Q_salida  = h1-h4
W_turbina = h4-h3

eficiencia = 1 -  abs(Q_salida)/ Q_entrada 

print("Trabajo de la bomba= {0} {1}" .format(round(W_bomba,2), 'KJ/Kg')) 
print('Trabajo de la turbina =  {0} {1}'.format(round(W_turbina,2), 'KJ/Kg'))
print("Q de entrada = {0} {1}".format(round(Q_entrada,2), 'KJ/Kg'))
print("Q de salida =  {0} {1}".format(round(Q_salida,2), 'KJ/Kg'))
print("Eficiencia = ", round(eficiencia,2))








