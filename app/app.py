# -*- coding: utf-8 -*-
"""
Flask Backend for Chemical Engineering Thermodynamics Toolkit
@author: Bryan Piguave Llano
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
from iapws import IAPWS97
import json

app = Flask(__name__)
CORS(app)

class ThermodynamicsAPI:
    """API class for thermodynamic calculations"""
    
    def __init__(self):
        self.R = 8.314  # J/mol·K
    
    def steam_properties(self, P=None, T=None, x=None, h=None, s=None):
        """Calculate steam properties using IAPWS-IF97"""
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
            return {'error': str(e)}
    
    def rankine_cycle_analysis(self, P_boiler, T_boiler, P_condenser, efficiency_pump=0.85, efficiency_turbine=0.85):
        """Analyze Rankine cycle"""
        try:
            # State 1: Condenser exit (saturated liquid)
            state_1 = self.steam_properties(P=P_condenser, x=0)
            if 'error' in state_1:
                return state_1
            
            # State 2: Pump exit (compressed liquid)
            s_2s = state_1['s']  # Isentropic compression
            state_2s = self.steam_properties(P=P_boiler, s=s_2s)
            if 'error' in state_2s:
                return state_2s
            
            h_2s = state_2s['h']
            h_1 = state_1['h']
            
            # Actual pump work considering efficiency
            w_pump_isentropic = state_1['v'] * (P_boiler - P_condenser) * 1000  # kJ/kg
            w_pump_actual = w_pump_isentropic / efficiency_pump
            h_2 = h_1 + w_pump_actual
            
            # State 3: Boiler exit (superheated steam)
            state_3 = self.steam_properties(P=P_boiler, T=T_boiler)
            if 'error' in state_3:
                return state_3
            
            # State 4: Turbine exit
            s_4s = state_3['s']  # Isentropic expansion
            state_4s = self.steam_properties(P=P_condenser, s=s_4s)
            if 'error' in state_4s:
                return state_4s
            
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
        except Exception as e:
            return {'error': str(e)}
    
    def brayton_cycle_analysis(self, P_compressor_in, T_compressor_in, P_compressor_out, T_turbine_in, 
                               efficiency_compressor=0.85, efficiency_turbine=0.85, gamma=1.4):
        """Analyze Brayton cycle"""
        try:
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
        except Exception as e:
            return {'error': str(e)}
    
    def vle_calculation(self, T, P_sat_1, P_sat_2, x1, model='ideal', A12=None, A21=None):
        """Calculate VLE for binary mixture"""
        try:
            x2 = 1 - x1
            
            # Calculate activity coefficients
            if model == 'wilson' and A12 is not None and A21 is not None:
                # Wilson equation
                ln_gamma1 = -np.log(x1 + A12 * x2) + x2 * (A12 / (x1 + A12 * x2) - A21 / (x2 + A21 * x1))
                ln_gamma2 = -np.log(x2 + A21 * x1) - x1 * (A12 / (x1 + A12 * x2) - A21 / (x2 + A21 * x1))
                gamma1 = np.exp(ln_gamma1)
                gamma2 = np.exp(ln_gamma2)
            else:
                # Ideal solution
                gamma1 = 1.0
                gamma2 = 1.0
            
            # Total pressure
            P_total = x1 * gamma1 * P_sat_1 + x2 * gamma2 * P_sat_2
            
            # Vapor mole fractions
            y1 = x1 * gamma1 * P_sat_1 / P_total
            y2 = 1 - y1
            
            return {
                'P_total': P_total,
                'y1': y1,
                'y2': y2,
                'gamma1': gamma1,
                'gamma2': gamma2,
                'x1': x1,
                'x2': x2,
                'T': T
            }
        except Exception as e:
            return {'error': str(e)}

# Initialize API
thermo_api = ThermodynamicsAPI()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/steam-properties', methods=['POST'])
def api_steam_properties():
    """API endpoint for steam properties"""
    try:
        data = request.get_json()
        P = data.get('P')
        T = data.get('T')
        x = data.get('x')
        h = data.get('h')
        s = data.get('s')
        
        result = thermo_api.steam_properties(P=P, T=T, x=x, h=h, s=s)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rankine-cycle', methods=['POST'])
def api_rankine_cycle():
    """API endpoint for Rankine cycle analysis"""
    try:
        data = request.get_json()
        result = thermo_api.rankine_cycle_analysis(
            P_boiler=data['P_boiler'],
            T_boiler=data['T_boiler'],
            P_condenser=data['P_condenser'],
            efficiency_pump=data.get('efficiency_pump', 0.85),
            efficiency_turbine=data.get('efficiency_turbine', 0.85)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/brayton-cycle', methods=['POST'])
def api_brayton_cycle():
    """API endpoint for Brayton cycle analysis"""
    try:
        data = request.get_json()
        result = thermo_api.brayton_cycle_analysis(
            P_compressor_in=data['P_compressor_in'],
            T_compressor_in=data['T_compressor_in'],
            P_compressor_out=data['P_compressor_out'],
            T_turbine_in=data['T_turbine_in'],
            efficiency_compressor=data.get('efficiency_compressor', 0.85),
            efficiency_turbine=data.get('efficiency_turbine', 0.85)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vle-calculation', methods=['POST'])
def api_vle_calculation():
    """API endpoint for VLE calculations"""
    try:
        data = request.get_json()
        result = thermo_api.vle_calculation(
            T=data['T'],
            P_sat_1=data['P_sat_1'],
            P_sat_2=data['P_sat_2'],
            x1=data['x1'],
            model=data.get('model', 'ideal'),
            A12=data.get('A12'),
            A21=data.get('A21')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 