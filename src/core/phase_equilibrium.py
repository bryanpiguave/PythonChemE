# -*- coding: utf-8 -*-
"""
Phase Equilibrium Calculations for Chemical Engineers
VLE, LLE, and flash calculations for binary and multicomponent systems
@author: Bryan Piguave Llano
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, minimize
from scipy.integrate import quad
import pandas as pd

class PhaseEquilibrium:
    """
    Phase equilibrium calculations for chemical engineering applications
    """
    
    def __init__(self):
        self.R = 8.314  # J/mol·K
        
    def raoult_law_vle(self, P_sat_1, P_sat_2, x1, T):
        """
        Calculate VLE using Raoult's Law for ideal binary mixture
        
        Parameters:
        P_sat_1, P_sat_2: Saturation pressures of components 1 and 2 (Pa)
        x1: Liquid mole fraction of component 1
        T: Temperature (K)
        
        Returns:
        dict: VLE results including y1, P_total, and phase compositions
        """
        x2 = 1 - x1
        
        # Total pressure
        P_total = x1 * P_sat_1 + x2 * P_sat_2
        
        # Vapor mole fraction of component 1
        y1 = x1 * P_sat_1 / P_total
        
        return {
            'P_total': P_total,
            'y1': y1,
            'y2': 1 - y1,
            'x1': x1,
            'x2': x2,
            'T': T
        }
    
    def wilson_activity_coefficients(self, x1, A12, A21, T):
        """
        Calculate activity coefficients using Wilson equation
        
        Parameters:
        x1: Liquid mole fraction of component 1
        A12, A21: Wilson parameters
        T: Temperature (K)
        
        Returns:
        tuple: (gamma1, gamma2) activity coefficients
        """
        x2 = 1 - x1
        
        # Wilson equation
        ln_gamma1 = -np.log(x1 + A12 * x2) + x2 * (A12 / (x1 + A12 * x2) - A21 / (x2 + A21 * x1))
        ln_gamma2 = -np.log(x2 + A21 * x1) - x1 * (A12 / (x1 + A12 * x2) - A21 / (x2 + A21 * x1))
        
        return np.exp(ln_gamma1), np.exp(ln_gamma2)
    
    def nrtl_activity_coefficients(self, x1, tau12, tau21, alpha12, T):
        """
        Calculate activity coefficients using NRTL equation
        
        Parameters:
        x1: Liquid mole fraction of component 1
        tau12, tau21: NRTL parameters
        alpha12: Non-randomness parameter
        T: Temperature (K)
        
        Returns:
        tuple: (gamma1, gamma2) activity coefficients
        """
        x2 = 1 - x1
        
        # NRTL equation
        G12 = np.exp(-alpha12 * tau12)
        G21 = np.exp(-alpha12 * tau21)
        
        ln_gamma1 = x2**2 * (tau21 * G21**2 / (x1 + x2 * G21)**2 + tau12 * G12 / (x2 + x1 * G12)**2)
        ln_gamma2 = x1**2 * (tau12 * G12**2 / (x2 + x1 * G12)**2 + tau21 * G21 / (x1 + x2 * G21)**2)
        
        return np.exp(ln_gamma1), np.exp(ln_gamma2)
    
    def flash_calculation(self, z1, P, T, P_sat_1, P_sat_2, gamma_model='wilson', 
                         A12=None, A21=None, tau12=None, tau21=None, alpha12=None):
        """
        Perform flash calculation for binary mixture
        
        Parameters:
        z1: Feed mole fraction of component 1
        P: System pressure (Pa)
        T: Temperature (K)
        P_sat_1, P_sat_2: Saturation pressures (Pa)
        gamma_model: Activity coefficient model ('wilson' or 'nrtl')
        A12, A21: Wilson parameters
        tau12, tau21, alpha12: NRTL parameters
        
        Returns:
        dict: Flash calculation results
        """
        def objective_function(V):
            """Objective function for flash calculation"""
            V = V[0]  # Vapor fraction
            if V < 0 or V > 1:
                return 1e6
            
            # Initial guess for x1
            x1 = z1
            
            # Iterative solution for x1 and y1
            for _ in range(10):
                x2 = 1 - x1
                
                # Calculate activity coefficients
                if gamma_model == 'wilson':
                    gamma1, gamma2 = self.wilson_activity_coefficients(x1, A12, A21, T)
                elif gamma_model == 'nrtl':
                    gamma1, gamma2 = self.nrtl_activity_coefficients(x1, tau12, tau21, alpha12, T)
                else:
                    gamma1, gamma2 = 1.0, 1.0  # Ideal solution
                
                # Calculate K-values
                K1 = gamma1 * P_sat_1 / P
                K2 = gamma2 * P_sat_2 / P
                
                # Rachford-Rice equation
                f = z1 * (K1 - 1) / (1 + V * (K1 - 1)) + (1 - z1) * (K2 - 1) / (1 + V * (K2 - 1))
                
                # Update x1
                x1_new = z1 / (1 + V * (K1 - 1))
                
                if abs(x1_new - x1) < 1e-6:
                    break
                x1 = x1_new
            
            return abs(f)
        
        # Solve for vapor fraction
        V_guess = 0.5
        result = minimize(objective_function, [V_guess], method='L-BFGS-B', 
                        bounds=[(0, 1)])
        
        V = result.x[0]
        
        # Calculate final compositions
        x1 = z1 / (1 + V * (K1 - 1))
        x2 = 1 - x1
        y1 = K1 * x1
        y2 = 1 - y1
        
        return {
            'V': V,  # Vapor fraction
            'x1': x1, 'x2': x2,  # Liquid compositions
            'y1': y1, 'y2': y2,  # Vapor compositions
            'K1': K1, 'K2': K2,  # K-values
            'P': P, 'T': T
        }
    
    def generate_txy_diagram(self, P_sat_1_func, P_sat_2_func, P_total, 
                            gamma_model='wilson', A12=None, A21=None, 
                            tau12=None, tau21=None, alpha12=None, T_range=None):
        """
        Generate Txy diagram for binary mixture
        
        Parameters:
        P_sat_1_func, P_sat_2_func: Functions that return saturation pressure vs T
        P_total: Total system pressure (Pa)
        gamma_model: Activity coefficient model
        A12, A21: Wilson parameters
        tau12, tau21, alpha12: NRTL parameters
        T_range: Temperature range (K) [T_min, T_max]
        
        Returns:
        dict: Txy diagram data
        """
        if T_range is None:
            T_range = [273.15, 373.15]  # Default range
        
        T_values = np.linspace(T_range[0], T_range[1], 100)
        x1_values = np.linspace(0.01, 0.99, 50)
        
        T_bubble = []
        T_dew = []
        x1_bubble = []
        y1_dew = []
        
        for x1 in x1_values:
            # Bubble point calculation
            def bubble_objective(T):
                P_sat_1 = P_sat_1_func(T)
                P_sat_2 = P_sat_2_func(T)
                
                if gamma_model == 'wilson':
                    gamma1, gamma2 = self.wilson_activity_coefficients(x1, A12, A21, T)
                elif gamma_model == 'nrtl':
                    gamma1, gamma2 = self.nrtl_activity_coefficients(x1, tau12, tau21, alpha12, T)
                else:
                    gamma1, gamma2 = 1.0, 1.0
                
                P_calc = x1 * gamma1 * P_sat_1 + (1 - x1) * gamma2 * P_sat_2
                return P_calc - P_total
            
            # Solve for bubble point temperature
            T_bubble_sol = fsolve(bubble_objective, T_range[0] + (T_range[1] - T_range[0]) / 2)
            
            if 0 < T_bubble_sol[0] < T_range[1]:
                T_bubble.append(T_bubble_sol[0])
                x1_bubble.append(x1)
                
                # Calculate y1 at bubble point
                P_sat_1 = P_sat_1_func(T_bubble_sol[0])
                P_sat_2 = P_sat_2_func(T_bubble_sol[0])
                
                if gamma_model == 'wilson':
                    gamma1, gamma2 = self.wilson_activity_coefficients(x1, A12, A21, T_bubble_sol[0])
                elif gamma_model == 'nrtl':
                    gamma1, gamma2 = self.nrtl_activity_coefficients(x1, tau12, tau21, alpha12, T_bubble_sol[0])
                else:
                    gamma1, gamma2 = 1.0, 1.0
                
                y1 = x1 * gamma1 * P_sat_1 / P_total
                T_dew.append(T_bubble_sol[0])
                y1_dew.append(y1)
        
        return {
            'T_bubble': T_bubble,
            'T_dew': T_dew,
            'x1_bubble': x1_bubble,
            'y1_dew': y1_dew,
            'P_total': P_total
        }
    
    def generate_pxy_diagram(self, T, P_sat_1, P_sat_2, gamma_model='wilson',
                           A12=None, A21=None, tau12=None, tau21=None, alpha12=None):
        """
        Generate Pxy diagram for binary mixture at constant temperature
        
        Parameters:
        T: Temperature (K)
        P_sat_1, P_sat_2: Saturation pressures at temperature T (Pa)
        gamma_model: Activity coefficient model
        A12, A21: Wilson parameters
        tau12, tau21, alpha12: NRTL parameters
        
        Returns:
        dict: Pxy diagram data
        """
        x1_values = np.linspace(0.01, 0.99, 100)
        P_values = []
        y1_values = []
        
        for x1 in x1_values:
            if gamma_model == 'wilson':
                gamma1, gamma2 = self.wilson_activity_coefficients(x1, A12, A21, T)
            elif gamma_model == 'nrtl':
                gamma1, gamma2 = self.nrtl_activity_coefficients(x1, tau12, tau21, alpha12, T)
            else:
                gamma1, gamma2 = 1.0, 1.0
            
            P_total = x1 * gamma1 * P_sat_1 + (1 - x1) * gamma2 * P_sat_2
            y1 = x1 * gamma1 * P_sat_1 / P_total
            
            P_values.append(P_total)
            y1_values.append(y1)
        
        return {
            'x1': x1_values,
            'y1': y1_values,
            'P': P_values,
            'T': T
        }
    
    def plot_phase_diagrams(self, txy_data=None, pxy_data=None):
        """
        Plot Txy and/or Pxy diagrams
        
        Parameters:
        txy_data: Txy diagram data from generate_txy_diagram
        pxy_data: Pxy diagram data from generate_pxy_diagram
        """
        if txy_data and pxy_data:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Txy diagram
            ax1.plot(txy_data['x1_bubble'], txy_data['T_bubble'], 'b-', label='Bubble Point')
            ax1.plot(txy_data['y1_dew'], txy_data['T_dew'], 'r-', label='Dew Point')
            ax1.set_xlabel('Mole Fraction Component 1')
            ax1.set_ylabel('Temperature (K)')
            ax1.set_title('Txy Diagram')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Pxy diagram
            ax2.plot(pxy_data['x1'], pxy_data['P'], 'b-', label='Liquid')
            ax2.plot(pxy_data['y1'], pxy_data['P'], 'r-', label='Vapor')
            ax2.set_xlabel('Mole Fraction Component 1')
            ax2.set_ylabel('Pressure (Pa)')
            ax2.set_title('Pxy Diagram')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
        elif txy_data:
            plt.figure(figsize=(8, 6))
            plt.plot(txy_data['x1_bubble'], txy_data['T_bubble'], 'b-', label='Bubble Point')
            plt.plot(txy_data['y1_dew'], txy_data['T_dew'], 'r-', label='Dew Point')
            plt.xlabel('Mole Fraction Component 1')
            plt.ylabel('Temperature (K)')
            plt.title('Txy Diagram')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
        elif pxy_data:
            plt.figure(figsize=(8, 6))
            plt.plot(pxy_data['x1'], pxy_data['P'], 'b-', label='Liquid')
            plt.plot(pxy_data['y1'], pxy_data['P'], 'r-', label='Vapor')
            plt.xlabel('Mole Fraction Component 1')
            plt.ylabel('Pressure (Pa)')
            plt.title('Pxy Diagram')
            plt.legend()
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Create phase equilibrium instance
    pe = PhaseEquilibrium()
    
    # Example: Benzene-Toluene system at 1 atm
    T = 373.15  # K
    P_sat_benzene = 1.8e5  # Pa (approximate at 100°C)
    P_sat_toluene = 7.4e4  # Pa (approximate at 100°C)
    
    # Wilson parameters for Benzene-Toluene
    A12 = 0.0952
    A21 = 0.2713
    
    # Generate Pxy diagram
    pxy_data = pe.generate_pxy_diagram(T, P_sat_benzene, P_sat_toluene, 
                                      gamma_model='wilson', A12=A12, A21=A21)
    
    # Flash calculation example
    z1 = 0.5  # Feed composition
    P = 1.013e5  # 1 atm
    
    flash_result = pe.flash_calculation(z1, P, T, P_sat_benzene, P_sat_toluene,
                                       gamma_model='wilson', A12=A12, A21=A21)
    
    print("=== Flash Calculation Results ===")
    print(f"Vapor fraction: {flash_result['V']:.3f}")
    print(f"Liquid composition (x1): {flash_result['x1']:.3f}")
    print(f"Vapor composition (y1): {flash_result['y1']:.3f}")
    print(f"K-values: K1={flash_result['K1']:.3f}, K2={flash_result['K2']:.3f}")
    
    # Plot phase diagram
    pe.plot_phase_diagrams(pxy_data=pxy_data) 