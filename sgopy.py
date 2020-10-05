# -*- coding: utf-8 -*-
"""
This script solves basic optical problems, considering the paraxial aproximation

Function optic system takes the following arguments:
    >>> sys ---> Kind of eq system to solve acording the optical system we are working in
    >>> Vars---> SymPy symbolic variables to use with the eq system
    
This function returns the SymPy system to solve acording sys value



Class geopetrical_optics takes the following aguments:
    
    >>> f ---> focal distance
    >>> f'---> focal image distance
    >>> n ---> refractive index of the first medium
    >>> n'---> refractive index of the second medium (if exists)
    >>> y ---> object height
    >>> y'---> image height
    >>> s ---> distance between the object and the optical system (X axis)
    >>> s'---> distance between the image and the optical system (X axis)
    >>> P ---> power of the lsen (if exists)
    >>> Ml---> lateral raise

For unknown arguments just don't pass them to the function
Using CMD set them blank (not yet)

This class has 3 functions:
   
    >>> __init__ ---> initializes variables
    >>> generate ---> 
    >>> Plot     --->

@author: Guillem
"""

from sympy import solve ,var, pprint, init_session, Integral, sqrt, Eq
import sys as SYS
import os
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np

    
def optic_system(sys, Vars):
    
    '''In this function we define the SymPy equation systems to solve, depending 
    which kind of problem are we working in
    '''
    
    f      = Vars[0]
    fprime = Vars[1]
    n      = Vars[2]
    nprime = Vars[3]
    y      = Vars[4]
    yprime = Vars[5]
    s      = Vars[6]
    sprime = Vars[7]
    R      = Vars[8]
    P      = Vars[9]
    Ml     = Vars[10]
    
    
    if sys == '@spherical_diopter':
        
        focal_ec             = R*(n/(nprime-n)) + f
        focal_prime_ec       = R*(nprime/(nprime-n)) - fprime
        gauss_ec             = fprime/sprime + f/s - 1
        lateral_raise        = yprime/y - Ml
        y_relation           = yprime/y - (n*sprime)/(nprime*s)
       
        return [focal_ec,
                focal_prime_ec,
                gauss_ec,
                lateral_raise,
                y_relation]
    
    
    elif sys == '@flat_diopter':
        
         y_relation = yprime - y
         fundamental_ec = nprime/sprime - n/s
         
         return [y_relation,
                 fundamental_ec]
     
        
    elif sys == '@flat_mirror':
        
        y_relation = yprime - y
        s_relation = sprime + s
        n_relation = nprime + n
        
        return [y_relation,
                s_relation, 
                n_relation]
    
    
    elif sys == '@curved_mirror':
        
        fundamental_eq = 1/sprime + 1/s - 2/R
        f_relation     = f - fprime
        f_equality     = f - R/2 
        lateral_raise  = Ml -yprime/y
        ys_relation    = yprime/y + sprime/s   
        
        return [fundamental_eq,
                f_relation,
                f_equality,
                lateral_raise,
                ys_relation]
    
    
    elif sys == '@thin_lens': 

        
        fundamental_eq = 1/s - 1/sprime - 1/f
        f_relation     = f + fprime
        lateral_raise  = Ml -yprime/y
        ys_relation    = yprime/y - sprime/s 
        power          = P -1/fprime
        
        return [fundamental_eq,
                f_relation,
                lateral_raise,
                ys_relation,
                power]
     
        
    else: print('Unexpected system')



class geometrical_optics():
    
    
    def __init__(self,
                f      = 'f'     ,
                fprime = 'fprime',
                n      = 'n'     ,
                nprime = 'nprime',
                y      = 'y'     ,
                yprime = 'yprime',
                s      = 's'     ,
                sprime = 'sprime',
                R      = 'R'     ,
                P      = 'P'     ,
                Ml     = 'Ml'): 


        self.variables = {'f'     :f     ,
                          'fprime':fprime,
                          'n'     :n     ,
                          'nprime':nprime,
                          'y'     :y     ,
                          'yprime':yprime,
                          's'     :s     ,
                          'sprime':sprime,
                          'R'     :R     ,
                          'P'     :P     ,
                          'Ml'    :Ml}
        
        for variable in self.variables:
            if self.variables[variable] == '':
                self.variables[variable] = variable
        
        self.data = {variable:float(self.variables[variable])
                    for variable in self.variables 
                    if type(self.variables[variable]) != str}
        
        self.Vars = [var('f')     ,
                     var('fprime'),
                     var('n')     ,
                     var('nprime'),
                     var('y')     ,
                     var('yprime'),
                     var('s')     ,
                     var('sprime'),
                     var('R')     ,
                     var('P')     ,
                     var('Ml')]
    
    
    
    def generate(self, sys):
        
        sysvars = [variable for variable in self.Vars if str(variable) in self.data]
        symvars = [variable for variable in self.Vars if str(variable) not in self.data]

          
        system = optic_system(sys, self.Vars)
        
        for i in range(len(system)):
            pprint(system[i], use_unicode=True) 
            pprint('\n')
        
        if sys == '@flat_diopter' or sys == '@flat_mirror': 
            self.variables['f']      = 1.416e32
            self.variables['fprime'] = 1.416e32
            self.variables['R']      = 1.416e32
            self.variables['Ml']     = 1
        
        for i in range(len(system)):
            for variable in sysvars:
                system[i] = system[i].subs(variable,self.data[str(variable)]) 
        
        sols = solve(system, symvars, dict = True)

        for i in range(len(system)):
            for j in range(len(symvars)):
                try:
                    system[i] = system[i].subs(symvars[j],sols[0][symvars[j]])
                except: pass
        
        for variable in sols[0]:
            self.variables[str(variable)] = sols[0][variable] 

        return self.variables, sys
        
    

    
    def Plot(self, sys):
        
        f, fprime, n, nprime, y, yprime, s, sprime, R, P, Ml = [
            self.variables[variable] for variable in self.variables]
        fig = plt.figure()
        ax = fig.add_subplot()#aspect = 'equal')

        def plot(sys):
            
            if sys == '@spherical_diopter':
                diopter = patches.Arc((0, 0), height=R, width=R, angle = 0, 
                                       theta1 = 135, theta2 = 225, 
                                      linewidth=2, fill=False)
                ax.add_patch(diopter)
    
                Xaxis = np.linspace(2*int(-f - R), 2*int(f + R))
    
                plt.plot(Xaxis, np.zeros((len(Xaxis))),'-.')
                plt.plot(f,y,'*')
                plt.plot(fprime,yprime,'*')
                plt.plot(0,0,'.')
                plt.plot((f,fprime),(y,yprime)) 
            
            if sys == '@flat_diopter':
                
                SYS.exit('function under development')
                
                
                plt.plot(s,0,'*')
                plt.plot(sprime,0,'*')
                plt.plot((s,sprime),(0,0))
        
        plot(sys)
        
    



# Esto es un ejemplo: 

sistema = geometrical_optics(R = 5.2, n = 1.1, nprime = 1.5, s = -25, y = 1)
dioptrio = sistema.generate('@spherical_diopter')[0]
print(dioptrio)
sistema.Plot('@spherical_diopter')