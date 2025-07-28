# -*- coding: utf-8 -*-
"""
Thermodynamics Toolkit for Chemical Engineers
A comprehensive collection of thermodynamic calculations and analysis tools
@author: Bryan Piguave Llano
"""

import numpy as np
import matplotlib.pyplot as plt
from iapws import IAPWS97

class ThermodynamicsToolkit:
    """
    A comprehensive toolkit for thermodynamic calculations
    """
    
    def __init__(self):
        self.R = 8.314  # Universal gas constant (J/mol·K)
        self.g = 9.81   # Gravitational acceleration (m/s²)
    
    def steam_properties(self, P=None, T=None, x=None, h=None, s=None):
        """
        Calculate steam properties using IAPWS-IF97 formulation
        
        Parameters:
        P: Pressure (MPa)
        T: Temperature (K)
        x: Quality (0-1)
        h: Enthalpy (kJ/kg)
        s: Entropy (kJ/kg·K)
        
        Returns:
        dict: Dictionary containing all thermodynamic properties
        """
        try:
            if P is not None and T is not None:
                state = IAPWS97(P=P, T=T)
            elif P is not None and x is not None:
                state = IAPWS97(P=P, x=x)
            elif P is not None and h is not None:
                state = IAPWS97(P=P, h=h)
            elif P is not None and s is not None:
                state = IAPWS97(P=P, s=s)
            else:
                raise ValueError("Insufficient parameters provided")
            
            return {
                'P': state.P,      # MPa
                'T': state.T,      # K
                'v': state.v,      # m³/kg
                'h': state.h,      # kJ/kg
                's': state.s,      # kJ/kg·K
                'u': state.u,      # kJ/kg
                'x': getattr(state, 'x', None),  # Quality
                'phase': state.phase
            }
        except Exception as e:
            print(f"Error calculating steam properties: {e}")
            return None
    
    def rankine_cycle_analysis(self, P_boiler, T_boiler, P_condenser, efficiency_pump=0.85, efficiency_turbine=0.85):
        """
        Analyze a Rankine cycle with given parameters
        
        Parameters:
        P_boiler: Boiler pressure (MPa)
        T_boiler: Boiler temperature (K)
        P_condenser: Condenser pressure (MPa)
        efficiency_pump: Pump isentropic efficiency
        efficiency_turbine: Turbine isentropic efficiency
        
        Returns:
        dict: Cycle analysis results
        """
        # State 1: Condenser exit (saturated liquid)
        state_1 = self.steam_properties(P=P_condenser, x=0)
        
        # State 2: Pump exit (compressed liquid)
        s_2s = state_1['s']  # Isentropic compression
        state_2s = self.steam_properties(P=P_boiler, s=s_2s)
        h_2s = state_2s['h']
        h_1 = state_1['h']
        
        # Actual pump work considering efficiency
        w_pump_isentropic = state_1['v'] * (P_boiler - P_condenser) * 1000  # kJ/kg
        w_pump_actual = w_pump_isentropic / efficiency_pump
        h_2 = h_1 + w_pump_actual
        
        # State 3: Boiler exit (superheated steam)
        state_3 = self.steam_properties(P=P_boiler, T=T_boiler)
        
        # State 4: Turbine exit
        s_4s = state_3['s']  # Isentropic expansion
        state_4s = self.steam_properties(P=P_condenser, s=s_4s)
        h_4s = state_4s['h']
        
        # Actual turbine work considering efficiency
        w_turbine_isentropic = state_3['h'] - h_4s
        w_turbine_actual = w_turbine_isentropic * efficiency_turbine
        h_4 = state_3['h'] - w_turbine_actual
        
        # Heat input and output
        q_in = state_3['h'] - h_2
        q_out = h_4 - h_1
        
        # Cycle efficiency
        w_net = w_turbine_actual - w_pump_actual
        efficiency_thermal = w_net / q_in
        efficiency_carnot = 1 - (state_1['T'] / state_3['T'])
        
        return {
            'states': {
                'state_1': state_1,
                'state_2': {'h': h_2, 'P': P_boiler, 's': state_1['s']},
                'state_3': state_3,
                'state_4': {'h': h_4, 'P': P_condenser, 's': state_3['s']}
            },
            'work_pump': w_pump_actual,
            'work_turbine': w_turbine_actual,
            'work_net': w_net,
            'heat_input': q_in,
            'heat_output': q_out,
            'efficiency_thermal': efficiency_thermal,
            'efficiency_carnot': efficiency_carnot,
            'back_work_ratio': w_pump_actual / w_turbine_actual
        }
    
    def brayton_cycle_analysis(self, P_compressor_in, T_compressor_in, P_compressor_out, T_turbine_in, 
                               efficiency_compressor=0.85, efficiency_turbine=0.85, gamma=1.4):
        """
        Analyze a Brayton cycle (gas turbine cycle)
        
        Parameters:
        P_compressor_in: Compressor inlet pressure (kPa)
        T_compressor_in: Compressor inlet temperature (K)
        P_compressor_out: Compressor outlet pressure (kPa)
        T_turbine_in: Turbine inlet temperature (K)
        efficiency_compressor: Compressor isentropic efficiency
        efficiency_turbine: Turbine isentropic efficiency
        gamma: Specific heat ratio
        
        Returns:
        dict: Cycle analysis results
        """
        # State 1: Compressor inlet
        T_1 = T_compressor_in
        P_1 = P_compressor_in
        
        # State 2: Compressor outlet (isentropic)
        P_2 = P_compressor_out
        T_2s = T_1 * (P_2 / P_1) ** ((gamma - 1) / gamma)
        
        # Actual compressor work
        w_compressor_isentropic = self.R * (T_2s - T_1) / (gamma - 1)
        w_compressor_actual = w_compressor_isentropic / efficiency_compressor
        T_2 = T_1 + w_compressor_actual * (gamma - 1) / self.R
        
        # State 3: Turbine inlet
        T_3 = T_turbine_in
        P_3 = P_2
        
        # State 4: Turbine outlet (isentropic)
        P_4 = P_1
        T_4s = T_3 * (P_4 / P_3) ** ((gamma - 1) / gamma)
        
        # Actual turbine work
        w_turbine_isentropic = self.R * (T_3 - T_4s) / (gamma - 1)
        w_turbine_actual = w_turbine_isentropic * efficiency_turbine
        T_4 = T_3 - w_turbine_actual * (gamma - 1) / self.R
        
        # Heat input and output
        q_in = self.R * (T_3 - T_2) / (gamma - 1)
        q_out = self.R * (T_4 - T_1) / (gamma - 1)
        
        # Cycle efficiency
        w_net = w_turbine_actual - w_compressor_actual
        efficiency_thermal = w_net / q_in
        efficiency_carnot = 1 - (T_1 / T_3)
        
        return {
            'states': {
                'state_1': {'T': T_1, 'P': P_1},
                'state_2': {'T': T_2, 'P': P_2},
                'state_3': {'T': T_3, 'P': P_3},
                'state_4': {'T': T_4, 'P': P_4}
            },
            'work_compressor': w_compressor_actual,
            'work_turbine': w_turbine_actual,
            'work_net': w_net,
            'heat_input': q_in,
            'heat_output': q_out,
            'efficiency_thermal': efficiency_thermal,
            'efficiency_carnot': efficiency_carnot,
            'back_work_ratio': w_compressor_actual / w_turbine_actual
        }
    
    def refrigeration_cycle_analysis(self, T_evaporator, T_condenser, refrigerant='R134a'):
        """
        Analyze a vapor compression refrigeration cycle
        
        Parameters:
        T_evaporator: Evaporator temperature (K)
        T_condenser: Condenser temperature (K)
        refrigerant: Refrigerant type (simplified model)
        
        Returns:
        dict: Cycle analysis results
        """
        # Simplified refrigeration cycle analysis
        # For a real implementation, you'd need refrigerant property tables
        
        # State 1: Evaporator exit (saturated vapor)
        h_1 = 400  # kJ/kg (typical for R134a)
        s_1 = 1.7  # kJ/kg·K
        
        # State 2: Compressor exit (superheated vapor)
        P_2 = 1.0  # MPa
        h_2 = 430  # kJ/kg
        s_2 = 1.8  # kJ/kg·K
        
        # State 3: Condenser exit (saturated liquid)
        h_3 = 250  # kJ/kg
        s_3 = 1.2  # kJ/kg·K
        
        # State 4: Expansion valve exit (two-phase)
        h_4 = h_3  # Isenthalpic expansion
        s_4 = 1.3  # kJ/kg·K
        
        # Cycle analysis
        w_compressor = h_2 - h_1
        q_evaporator = h_1 - h_4
        q_condenser = h_2 - h_3
        cop = q_evaporator / w_compressor
        
        return {
            'states': {
                'state_1': {'h': h_1, 's': s_1, 'T': T_evaporator},
                'state_2': {'h': h_2, 's': s_2, 'T': T_condenser + 20},
                'state_3': {'h': h_3, 's': s_3, 'T': T_condenser},
                'state_4': {'h': h_4, 's': s_4, 'T': T_evaporator}
            },
            'work_compressor': w_compressor,
            'heat_evaporator': q_evaporator,
            'heat_condenser': q_condenser,
            'cop': cop
        }
    
    def plot_cycle_diagram(self, cycle_data, cycle_type='rankine'):
        """
        Plot thermodynamic cycle diagrams
        
        Parameters:
        cycle_data: Dictionary containing cycle analysis results
        cycle_type: Type of cycle ('rankine', 'brayton', 'refrigeration')
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        if cycle_type == 'rankine':
            # T-s diagram
            states = cycle_data['states']
            s_values = [states['state_1']['s'], states['state_2']['s'], 
                       states['state_3']['s'], states['state_4']['s']]
            T_values = [states['state_1']['T'], states['state_2']['T'], 
                       states['state_3']['T'], states['state_4']['T']]
            
            ax1.plot(s_values, T_values, 'bo-', linewidth=2, markersize=8)
            ax1.set_xlabel('Entropy (kJ/kg·K)')
            ax1.set_ylabel('Temperature (K)')
            ax1.set_title('Rankine Cycle T-s Diagram')
            ax1.grid(True, alpha=0.3)
            
            # P-h diagram
            h_values = [states['state_1']['h'], states['state_2']['h'], 
                       states['state_3']['h'], states['state_4']['h']]
            P_values = [states['state_1']['P'], states['state_2']['P'], 
                       states['state_3']['P'], states['state_4']['P']]
            
            ax2.plot(h_values, P_values, 'ro-', linewidth=2, markersize=8)
            ax2.set_xlabel('Enthalpy (kJ/kg)')
            ax2.set_ylabel('Pressure (MPa)')
            ax2.set_title('Rankine Cycle P-h Diagram')
            ax2.grid(True, alpha=0.3)
            ax2.set_yscale('log')
        
        plt.tight_layout()
        plt.show()
    
    def calculate_entropy_change(self, T1, T2, P1, P2, cp, R):
        """
        Calculate entropy change for an ideal gas
        
        Parameters:
        T1, T2: Initial and final temperatures (K)
        P1, P2: Initial and final pressures (Pa)
        cp: Specific heat at constant pressure (J/kg·K)
        R: Gas constant (J/kg·K)
        
        Returns:
        float: Entropy change (J/kg·K)
        """
        return cp * np.log(T2/T1) - R * np.log(P2/P1)
    
    def calculate_enthalpy_change(self, T1, T2, cp):
        """
        Calculate enthalpy change for constant specific heat
        
        Parameters:
        T1, T2: Initial and final temperatures (K)
        cp: Specific heat at constant pressure (J/kg·K)
        
        Returns:
        float: Enthalpy change (J/kg)
        """
        return cp * (T2 - T1)
    
    def isentropic_efficiency(self, actual_work, isentropic_work):
        """
        Calculate isentropic efficiency
        
        Parameters:
        actual_work: Actual work (J/kg)
        isentropic_work: Isentropic work (J/kg)
        
        Returns:
        float: Isentropic efficiency
        """
        return actual_work / isentropic_work

# Example usage and testing
if __name__ == "__main__":
    # Create toolkit instance
    thermo = ThermodynamicsToolkit()
    
    # Test steam properties
    print("=== Steam Properties Test ===")
    steam_props = thermo.steam_properties(P=1.0, T=400)
    if steam_props:
        print(f"P = {steam_props['P']} MPa")
        print(f"T = {steam_props['T']} K")
        print(f"h = {steam_props['h']} kJ/kg")
        print(f"s = {steam_props['s']} kJ/kg·K")
    
    # Test Rankine cycle
    print("\n=== Rankine Cycle Analysis ===")
    rankine_results = thermo.rankine_cycle_analysis(
        P_boiler=3.0, T_boiler=623.15, P_condenser=0.075
    )
    print(f"Thermal Efficiency: {rankine_results['efficiency_thermal']:.3f}")
    print(f"Carnot Efficiency: {rankine_results['efficiency_carnot']:.3f}")
    print(f"Net Work: {rankine_results['work_net']:.2f} kJ/kg")
    
    # Test Brayton cycle
    print("\n=== Brayton Cycle Analysis ===")
    brayton_results = thermo.brayton_cycle_analysis(
        P_compressor_in=100, T_compressor_in=300,
        P_compressor_out=1000, T_turbine_in=1200
    )
    print(f"Thermal Efficiency: {brayton_results['efficiency_thermal']:.3f}")
    print(f"Net Work: {brayton_results['work_net']:.2f} J/kg")
    
    # Plot cycle diagrams
    thermo.plot_cycle_diagram(rankine_results, 'rankine') 