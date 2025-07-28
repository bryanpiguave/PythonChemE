# Chemical Engineering Thermodynamics Toolkit 🥼🧪

A comprehensive collection of interactive tools for chemical engineering thermodynamics calculations, featuring both Python modules and a modern web application.

## Features

### 🔧 Thermodynamics Toolkit (`thermodynamics_toolkit.py`)
- **Steam Properties Calculator**: IAPWS-IF97 formulation for accurate steam properties
- **Rankine Cycle Analysis**: Complete cycle analysis with efficiency calculations
- **Brayton Cycle Analysis**: Gas turbine cycle analysis
- **Refrigeration Cycle Analysis**: Vapor compression refrigeration cycles
- **Interactive Charts**: T-s and P-h diagrams for cycle visualization

### ⚗️ Phase Equilibrium (`phase_equilibrium.py`)
- **VLE Calculations**: Vapor-Liquid Equilibrium for binary mixtures
- **Activity Coefficient Models**: Wilson and NRTL equations
- **Flash Calculations**: Isothermal flash for binary systems
- **Phase Diagrams**: Txy and Pxy diagram generation
- **Raoult's Law**: Ideal solution calculations

### 🌐 Interactive Web Application
- **Modern UI**: Responsive design with beautiful gradients and animations
- **Real-time Calculations**: Instant results with parameter adjustments
- **Interactive Charts**: Dynamic visualization using Chart.js
- **Multiple Tools**: Rankine, Brayton, Steam Properties, VLE, and Refrigeration calculators
- **API Backend**: Flask-based REST API for complex calculations

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/bryanpiguave/PythonChemE
cd PythonChemE
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the web application**:
```bash
python app.py
```

4. **Open your browser** and navigate to `http://localhost:5000`

## Usage

### Web Application
1. Choose a tool from the navigation menu
2. Enter your parameters in the input panel
3. Click "Calculate" to see results
4. View interactive charts and diagrams
5. Adjust parameters to see real-time updates

### Python Modules
```python
# Import the thermodynamics toolkit
from thermodynamics_toolkit import ThermodynamicsToolkit

# Create an instance
thermo = ThermodynamicsToolkit()

# Calculate steam properties
steam_props = thermo.steam_properties(P=1.0, T=400)

# Analyze Rankine cycle
rankine_results = thermo.rankine_cycle_analysis(
    P_boiler=3.0, 
    T_boiler=623.15, 
    P_condenser=0.075
)

# Plot cycle diagrams
thermo.plot_cycle_diagram(rankine_results, 'rankine')
```

## Available Tools

### 1. Rankine Cycle Analysis
- **Inputs**: Boiler pressure/temperature, condenser pressure, efficiencies
- **Outputs**: Thermal efficiency, work outputs, heat transfers, back work ratio
- **Features**: T-s and P-h diagrams, efficiency comparison with Carnot

### 2. Brayton Cycle Analysis
- **Inputs**: Compressor/turbine pressures and temperatures, efficiencies
- **Outputs**: Thermal efficiency, work outputs, heat transfers
- **Features**: Temperature-entropy analysis, efficiency optimization

### 3. Steam Properties Calculator
- **Inputs**: Pressure, temperature, quality, enthalpy, or entropy
- **Outputs**: Complete thermodynamic properties (h, s, v, u, x, phase)
- **Features**: IAPWS-IF97 formulation, phase identification

### 4. VLE Calculator
- **Inputs**: Temperature, saturation pressures, composition, activity coefficients
- **Outputs**: Vapor compositions, total pressure, activity coefficients
- **Features**: Wilson and NRTL models, ideal solution option

### 5. Refrigeration Cycle Analysis
- **Inputs**: Evaporator/condenser temperatures, refrigerant type
- **Outputs**: Coefficient of performance, work and heat transfers
- **Features**: Multiple refrigerant options, cycle optimization

## Technical Details

### Backend API Endpoints
- `POST /api/steam-properties`: Steam property calculations
- `POST /api/rankine-cycle`: Rankine cycle analysis
- `POST /api/brayton-cycle`: Brayton cycle analysis
- `POST /api/vle-calculation`: VLE calculations

### Dependencies
- **Flask**: Web framework for the API
- **IAPWS**: International Association for the Properties of Water and Steam
- **NumPy/SciPy**: Numerical computations
- **Chart.js**: Interactive charts and visualizations
- **Matplotlib**: Python plotting library

## Examples

### Rankine Cycle Example
```python
# Analyze a steam power cycle
results = thermo.rankine_cycle_analysis(
    P_boiler=3.0,      # MPa
    T_boiler=623.15,   # K
    P_condenser=0.075, # MPa
    efficiency_pump=0.85,
    efficiency_turbine=0.85
)

print(f"Thermal Efficiency: {results['efficiency_thermal']:.3f}")
print(f"Net Work: {results['work_net']:.2f} kJ/kg")
```

### VLE Example
```python
from phase_equilibrium import PhaseEquilibrium

pe = PhaseEquilibrium()

# Benzene-Toluene system
T = 373.15  # K
P_sat_benzene = 1.8e5  # Pa
P_sat_toluene = 7.4e4  # Pa
A12, A21 = 0.0952, 0.2713  # Wilson parameters

# Generate Pxy diagram
pxy_data = pe.generate_pxy_diagram(
    T, P_sat_benzene, P_sat_toluene,
    gamma_model='wilson', A12=A12, A21=A21
)

pe.plot_phase_diagrams(pxy_data=pxy_data)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## Author
**Bryan Piguave Llano**

## License
This project is open source and available under the MIT License.

## Future Enhancements

- [ ] Chemical reaction thermodynamics
- [ ] Distillation column design
- [ ] Heat exchanger analysis
- [ ] Process optimization tools
- [ ] 3D phase diagrams
- [ ] Mobile app version
- [ ] Database integration for property data
- [ ] Machine learning for property prediction
