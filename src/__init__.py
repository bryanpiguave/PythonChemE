"""
Chemical Engineering Thermodynamics Toolkit

A comprehensive collection of interactive tools for chemical engineering 
thermodynamics calculations, featuring both Python modules and a modern web application.

Author: Bryan Piguave Llano
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Bryan Piguave Llano"
__email__ = "bryan.piguave@example.com"

# Lazy imports to avoid dependency issues
def get_thermodynamics_toolkit():
    """Get ThermodynamicsToolkit class when needed."""
    from .core import ThermodynamicsToolkit
    return ThermodynamicsToolkit

def get_phase_equilibrium():
    """Get PhaseEquilibrium class when needed."""
    from .core import PhaseEquilibrium
    return PhaseEquilibrium

__all__ = [
    "get_thermodynamics_toolkit",
    "get_phase_equilibrium"
] 