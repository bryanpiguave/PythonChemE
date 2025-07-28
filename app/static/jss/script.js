// Global variables
let currentTool = 'rankine';
let charts = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeVLEModelSelector();
    showMessage('Welcome to the Chemical Engineering Thermodynamics Toolkit!', 'success');
});

// Navigation functionality
function initializeNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const toolSections = document.querySelectorAll('.tool-section');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tool = this.getAttribute('data-tool');
            
            // Update active button
            navButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Show selected tool section
            toolSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === tool) {
                    section.classList.add('active');
                }
            });
            
            currentTool = tool;
            
            // Initialize charts for the new tool
            initializeCharts(tool);
        });
    });
}

// Initialize VLE model selector
function initializeVLEModelSelector() {
    const modelSelect = document.getElementById('vle-model');
    const wilsonParams = document.querySelectorAll('.wilson-params');
    
    modelSelect.addEventListener('change', function() {
        if (this.value === 'wilson') {
            wilsonParams.forEach(param => param.style.display = 'block');
        } else {
            wilsonParams.forEach(param => param.style.display = 'none');
        }
    });
}

// Initialize charts for different tools
function initializeCharts(tool) {
    if (charts[tool]) {
        charts[tool].destroy();
    }
    
    const ctx = document.getElementById(`${tool}-chart`);
    if (!ctx) return;
    
    switch(tool) {
        case 'rankine':
            createRankineChart(ctx);
            break;
        case 'brayton':
            createBraytonChart(ctx);
            break;
        case 'vle':
            createVLEChart(ctx);
            break;
        case 'refrigeration':
            createRefrigerationChart(ctx);
            break;
    }
}

// Rankine Cycle Calculations
function calculateRankine() {
    const P_boiler = parseFloat(document.getElementById('rankine-boiler-p').value);
    const T_boiler = parseFloat(document.getElementById('rankine-boiler-t').value);
    const P_condenser = parseFloat(document.getElementById('rankine-condenser-p').value);
    const efficiency_pump = parseFloat(document.getElementById('rankine-pump-eff').value);
    const efficiency_turbine = parseFloat(document.getElementById('rankine-turbine-eff').value);
    
    try {
        // Simplified Rankine cycle calculations
        const results = performRankineCalculations(P_boiler, T_boiler, P_condenser, efficiency_pump, efficiency_turbine);
        
        // Update results
        document.getElementById('rankine-efficiency').textContent = (results.efficiency_thermal * 100).toFixed(2) + '%';
        document.getElementById('rankine-net-work').textContent = results.work_net.toFixed(2);
        document.getElementById('rankine-heat-input').textContent = results.heat_input.toFixed(2);
        document.getElementById('rankine-pump-work').textContent = results.work_pump.toFixed(2);
        document.getElementById('rankine-turbine-work').textContent = results.work_turbine.toFixed(2);
        document.getElementById('rankine-back-work').textContent = results.back_work_ratio.toFixed(3);
        
        // Update chart
        updateRankineChart(results);
        
        showMessage('Rankine cycle calculation completed successfully!', 'success');
    } catch (error) {
        showMessage('Error in Rankine cycle calculation: ' + error.message, 'error');
    }
}

function performRankineCalculations(P_boiler, T_boiler, P_condenser, efficiency_pump, efficiency_turbine) {
    // Simplified calculations (in a real implementation, you'd use the IAPWS library)
    const R = 8.314; // J/mol·K
    const M_water = 0.018; // kg/mol
    
    // State 1: Condenser exit (saturated liquid)
    const T_1 = 273.15 + 40; // Approximate condenser temperature
    const h_1 = 167.5; // kJ/kg (approximate)
    const s_1 = 0.572; // kJ/kg·K (approximate)
    const v_1 = 0.001; // m³/kg (approximate)
    
    // State 2: Pump exit
    const w_pump_isentropic = v_1 * (P_boiler - P_condenser) * 1000; // kJ/kg
    const w_pump_actual = w_pump_isentropic / efficiency_pump;
    const h_2 = h_1 + w_pump_actual;
    
    // State 3: Boiler exit
    const h_3 = 3000; // kJ/kg (approximate superheated steam)
    const s_3 = 6.5; // kJ/kg·K (approximate)
    
    // State 4: Turbine exit
    const h_4s = 2200; // kJ/kg (approximate isentropic expansion)
    const w_turbine_isentropic = h_3 - h_4s;
    const w_turbine_actual = w_turbine_isentropic * efficiency_turbine;
    const h_4 = h_3 - w_turbine_actual;
    
    // Heat input and output
    const q_in = h_3 - h_2;
    const q_out = h_4 - h_1;
    
    // Cycle efficiency
    const w_net = w_turbine_actual - w_pump_actual;
    const efficiency_thermal = w_net / q_in;
    const efficiency_carnot = 1 - (T_1 / T_boiler);
    const back_work_ratio = w_pump_actual / w_turbine_actual;
    
    return {
        work_pump: w_pump_actual,
        work_turbine: w_turbine_actual,
        work_net: w_net,
        heat_input: q_in,
        heat_output: q_out,
        efficiency_thermal: efficiency_thermal,
        efficiency_carnot: efficiency_carnot,
        back_work_ratio: back_work_ratio,
        states: {
            state_1: { h: h_1, s: s_1, T: T_1, P: P_condenser },
            state_2: { h: h_2, s: s_1, P: P_boiler },
            state_3: { h: h_3, s: s_3, T: T_boiler, P: P_boiler },
            state_4: { h: h_4, s: s_3, P: P_condenser }
        }
    };
}

// Brayton Cycle Calculations
function calculateBrayton() {
    const P_compressor_in = parseFloat(document.getElementById('brayton-compressor-in-p').value);
    const T_compressor_in = parseFloat(document.getElementById('brayton-compressor-in-t').value);
    const P_compressor_out = parseFloat(document.getElementById('brayton-compressor-out-p').value);
    const T_turbine_in = parseFloat(document.getElementById('brayton-turbine-in-t').value);
    const efficiency_compressor = parseFloat(document.getElementById('brayton-compressor-eff').value);
    const efficiency_turbine = parseFloat(document.getElementById('brayton-turbine-eff').value);
    
    try {
        const results = performBraytonCalculations(P_compressor_in, T_compressor_in, P_compressor_out, T_turbine_in, efficiency_compressor, efficiency_turbine);
        
        // Update results
        document.getElementById('brayton-efficiency').textContent = (results.efficiency_thermal * 100).toFixed(2) + '%';
        document.getElementById('brayton-net-work').textContent = results.work_net.toFixed(0);
        document.getElementById('brayton-compressor-work').textContent = results.work_compressor.toFixed(0);
        document.getElementById('brayton-turbine-work').textContent = results.work_turbine.toFixed(0);
        document.getElementById('brayton-back-work').textContent = results.back_work_ratio.toFixed(3);
        
        // Update chart
        updateBraytonChart(results);
        
        showMessage('Brayton cycle calculation completed successfully!', 'success');
    } catch (error) {
        showMessage('Error in Brayton cycle calculation: ' + error.message, 'error');
    }
}

function performBraytonCalculations(P_compressor_in, T_compressor_in, P_compressor_out, T_turbine_in, efficiency_compressor, efficiency_turbine) {
    const R = 8.314; // J/mol·K
    const gamma = 1.4; // Specific heat ratio for air
    
    // State 1: Compressor inlet
    const T_1 = T_compressor_in;
    const P_1 = P_compressor_in;
    
    // State 2: Compressor outlet (isentropic)
    const P_2 = P_compressor_out;
    const T_2s = T_1 * Math.pow(P_2 / P_1, (gamma - 1) / gamma);
    
    // Actual compressor work
    const w_compressor_isentropic = R * (T_2s - T_1) / (gamma - 1);
    const w_compressor_actual = w_compressor_isentropic / efficiency_compressor;
    const T_2 = T_1 + w_compressor_actual * (gamma - 1) / R;
    
    // State 3: Turbine inlet
    const T_3 = T_turbine_in;
    const P_3 = P_2;
    
    // State 4: Turbine outlet (isentropic)
    const P_4 = P_1;
    const T_4s = T_3 * Math.pow(P_4 / P_3, (gamma - 1) / gamma);
    
    // Actual turbine work
    const w_turbine_isentropic = R * (T_3 - T_4s) / (gamma - 1);
    const w_turbine_actual = w_turbine_isentropic * efficiency_turbine;
    const T_4 = T_3 - w_turbine_actual * (gamma - 1) / R;
    
    // Heat input and output
    const q_in = R * (T_3 - T_2) / (gamma - 1);
    const q_out = R * (T_4 - T_1) / (gamma - 1);
    
    // Cycle efficiency
    const w_net = w_turbine_actual - w_compressor_actual;
    const efficiency_thermal = w_net / q_in;
    const efficiency_carnot = 1 - (T_1 / T_3);
    const back_work_ratio = w_compressor_actual / w_turbine_actual;
    
    return {
        work_compressor: w_compressor_actual,
        work_turbine: w_turbine_actual,
        work_net: w_net,
        heat_input: q_in,
        heat_output: q_out,
        efficiency_thermal: efficiency_thermal,
        efficiency_carnot: efficiency_carnot,
        back_work_ratio: back_work_ratio,
        states: {
            state_1: { T: T_1, P: P_1 },
            state_2: { T: T_2, P: P_2 },
            state_3: { T: T_3, P: P_3 },
            state_4: { T: T_4, P: P_4 }
        }
    };
}

// Steam Properties Calculations
function calculateSteam() {
    const P = parseFloat(document.getElementById('steam-p').value);
    const T = parseFloat(document.getElementById('steam-t').value);
    const x = parseFloat(document.getElementById('steam-x').value);
    const propertyType = document.getElementById('steam-property-type').value;
    
    try {
        const results = performSteamCalculations(P, T, x, propertyType);
        
        // Update results
        document.getElementById('steam-result-p').textContent = results.P.toFixed(3);
        document.getElementById('steam-result-t').textContent = results.T.toFixed(2);
        document.getElementById('steam-result-v').textContent = results.v.toFixed(6);
        document.getElementById('steam-result-h').textContent = results.h.toFixed(2);
        document.getElementById('steam-result-s').textContent = results.s.toFixed(3);
        document.getElementById('steam-result-u').textContent = results.u.toFixed(2);
        document.getElementById('steam-result-x').textContent = results.x !== null ? results.x.toFixed(3) : 'N/A';
        document.getElementById('steam-result-phase').textContent = results.phase;
        
        showMessage('Steam properties calculated successfully!', 'success');
    } catch (error) {
        showMessage('Error in steam properties calculation: ' + error.message, 'error');
    }
}

function performSteamCalculations(P, T, x, propertyType) {
    // Simplified steam properties (in a real implementation, you'd use the IAPWS library)
    let properties = {};
    
    switch(propertyType) {
        case 'PT':
            // Pressure and Temperature
            properties = {
                P: P,
                T: T,
                v: 0.001 + (T - 273.15) * 0.0001, // Simplified
                h: 2500 + (T - 273.15) * 2.0, // Simplified
                s: 1.0 + (T - 273.15) * 0.01, // Simplified
                u: 2300 + (T - 273.15) * 1.8, // Simplified
                x: null,
                phase: T > 373.15 ? 'Superheated' : 'Subcooled'
            };
            break;
        case 'Px':
            // Pressure and Quality
            properties = {
                P: P,
                T: 273.15 + 100, // Simplified
                v: 0.001 + x * 1.5, // Simplified
                h: 167.5 + x * 2400, // Simplified
                s: 0.572 + x * 7.0, // Simplified
                u: 167.5 + x * 2200, // Simplified
                x: x,
                phase: x === 0 ? 'Saturated Liquid' : x === 1 ? 'Saturated Vapor' : 'Two-Phase'
            };
            break;
        default:
            throw new Error('Property type not implemented');
    }
    
    return properties;
}

// VLE Calculations
function calculateVLE() {
    const T = parseFloat(document.getElementById('vle-t').value);
    const P_sat_1 = parseFloat(document.getElementById('vle-p-sat-1').value);
    const P_sat_2 = parseFloat(document.getElementById('vle-p-sat-2').value);
    const x1 = parseFloat(document.getElementById('vle-x1').value);
    const model = document.getElementById('vle-model').value;
    const A12 = parseFloat(document.getElementById('vle-a12').value);
    const A21 = parseFloat(document.getElementById('vle-a21').value);
    
    try {
        const results = performVLECalculations(T, P_sat_1, P_sat_2, x1, model, A12, A21);
        
        // Update results
        document.getElementById('vle-p-total').textContent = results.P_total.toFixed(0);
        document.getElementById('vle-y1').textContent = results.y1.toFixed(3);
        document.getElementById('vle-y2').textContent = results.y2.toFixed(3);
        document.getElementById('vle-gamma1').textContent = results.gamma1.toFixed(3);
        document.getElementById('vle-gamma2').textContent = results.gamma2.toFixed(3);
        
        // Update chart
        updateVLEChart(results);
        
        showMessage('VLE calculation completed successfully!', 'success');
    } catch (error) {
        showMessage('Error in VLE calculation: ' + error.message, 'error');
    }
}

function performVLECalculations(T, P_sat_1, P_sat_2, x1, model, A12, A21) {
    const x2 = 1 - x1;
    
    let gamma1, gamma2;
    
    // Calculate activity coefficients
    if (model === 'wilson') {
        // Wilson equation
        const ln_gamma1 = -Math.log(x1 + A12 * x2) + x2 * (A12 / (x1 + A12 * x2) - A21 / (x2 + A21 * x1));
        const ln_gamma2 = -Math.log(x2 + A21 * x1) - x1 * (A12 / (x1 + A12 * x2) - A21 / (x2 + A21 * x1));
        gamma1 = Math.exp(ln_gamma1);
        gamma2 = Math.exp(ln_gamma2);
    } else {
        // Ideal solution
        gamma1 = 1.0;
        gamma2 = 1.0;
    }
    
    // Total pressure
    const P_total = x1 * gamma1 * P_sat_1 + x2 * gamma2 * P_sat_2;
    
    // Vapor mole fractions
    const y1 = x1 * gamma1 * P_sat_1 / P_total;
    const y2 = 1 - y1;
    
    return {
        P_total: P_total,
        y1: y1,
        y2: y2,
        gamma1: gamma1,
        gamma2: gamma2,
        x1: x1,
        x2: x2,
        T: T
    };
}

// Refrigeration Cycle Calculations
function calculateRefrigeration() {
    const T_evaporator = parseFloat(document.getElementById('refrig-evap-t').value);
    const T_condenser = parseFloat(document.getElementById('refrig-cond-t').value);
    const refrigerant = document.getElementById('refrig-refrigerant').value;
    
    try {
        const results = performRefrigerationCalculations(T_evaporator, T_condenser, refrigerant);
        
        // Update results
        document.getElementById('refrig-cop').textContent = results.cop.toFixed(2);
        document.getElementById('refrig-compressor-work').textContent = results.work_compressor.toFixed(2);
        document.getElementById('refrig-evaporator-heat').textContent = results.heat_evaporator.toFixed(2);
        document.getElementById('refrig-condenser-heat').textContent = results.heat_condenser.toFixed(2);
        
        // Update chart
        updateRefrigerationChart(results);
        
        showMessage('Refrigeration cycle calculation completed successfully!', 'success');
    } catch (error) {
        showMessage('Error in refrigeration cycle calculation: ' + error.message, 'error');
    }
}

function performRefrigerationCalculations(T_evaporator, T_condenser, refrigerant) {
    // Simplified refrigeration cycle calculations
    const h_1 = 400; // kJ/kg (evaporator exit)
    const h_2 = 430; // kJ/kg (compressor exit)
    const h_3 = 250; // kJ/kg (condenser exit)
    const h_4 = h_3; // Isenthalpic expansion
    
    const work_compressor = h_2 - h_1;
    const heat_evaporator = h_1 - h_4;
    const heat_condenser = h_2 - h_3;
    const cop = heat_evaporator / work_compressor;
    
    return {
        work_compressor: work_compressor,
        heat_evaporator: heat_evaporator,
        heat_condenser: heat_condenser,
        cop: cop
    };
}

// Chart creation functions
function createRankineChart(ctx) {
    charts.rankine = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['State 1', 'State 2', 'State 3', 'State 4'],
            datasets: [{
                label: 'Enthalpy (kJ/kg)',
                data: [0, 0, 0, 0],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Rankine Cycle - Enthalpy vs State'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createBraytonChart(ctx) {
    charts.brayton = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['State 1', 'State 2', 'State 3', 'State 4'],
            datasets: [{
                label: 'Temperature (K)',
                data: [0, 0, 0, 0],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Brayton Cycle - Temperature vs State'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createVLEChart(ctx) {
    charts.vle = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Liquid',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgb(75, 192, 192)'
            }, {
                label: 'Vapor',
                data: [],
                backgroundColor: 'rgba(255, 99, 132, 0.6)',
                borderColor: 'rgb(255, 99, 132)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Pxy Diagram'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Mole Fraction Component 1'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Pressure (Pa)'
                    }
                }
            }
        }
    });
}

function createRefrigerationChart(ctx) {
    charts.refrigeration = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Compressor Work', 'Evaporator Heat', 'Condenser Heat'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(255, 205, 86, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Refrigeration Cycle Energy Distribution'
                }
            }
        }
    });
}

// Chart update functions
function updateRankineChart(results) {
    if (charts.rankine) {
        const h_values = [
            results.states.state_1.h,
            results.states.state_2.h,
            results.states.state_3.h,
            results.states.state_4.h
        ];
        
        charts.rankine.data.datasets[0].data = h_values;
        charts.rankine.update();
    }
}

function updateBraytonChart(results) {
    if (charts.brayton) {
        const T_values = [
            results.states.state_1.T,
            results.states.state_2.T,
            results.states.state_3.T,
            results.states.state_4.T
        ];
        
        charts.brayton.data.datasets[0].data = T_values;
        charts.brayton.update();
    }
}

function updateVLEChart(results) {
    if (charts.vle) {
        // Generate Pxy data points
        const x_values = [];
        const P_liquid = [];
        const P_vapor = [];
        
        for (let i = 0; i <= 10; i++) {
            const x = i / 10;
            const P_total = x * results.gamma1 * results.P_sat_1 + (1 - x) * results.gamma2 * results.P_sat_2;
            const y = x * results.gamma1 * results.P_sat_1 / P_total;
            
            x_values.push(x);
            P_liquid.push(P_total);
            P_vapor.push(P_total);
        }
        
        charts.vle.data.datasets[0].data = x_values.map((x, i) => ({x: x, y: P_liquid[i]}));
        charts.vle.data.datasets[1].data = x_values.map((x, i) => ({x: x, y: P_vapor[i]}));
        charts.vle.update();
    }
}

function updateRefrigerationChart(results) {
    if (charts.refrigeration) {
        charts.refrigeration.data.datasets[0].data = [
            results.work_compressor,
            results.heat_evaporator,
            results.heat_condenser
        ];
        charts.refrigeration.update();
    }
}

// Utility functions
function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert at the top of main content
    const mainContent = document.querySelector('.main-content');
    mainContent.insertBefore(messageDiv, mainContent.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}

// Initialize charts on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts('rankine');
}); 