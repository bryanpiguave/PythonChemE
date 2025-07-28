"""
Core thermodynamics modules for Chemical Engineering calculations.

This package contains the main thermodynamics functionality including:
- Steam properties calculations
- Rankine cycle analysis
- Brayton cycle analysis
- Phase equilibrium calculations
- VLE (Vapor-Liquid Equilibrium) analysis
"""

__version__ = "1.0.0"
__author__ = "Bryan Piguave Llano"

# Lazy imports to avoid dependency issues
def get_thermodynamics_toolkit():
    """Get ThermodynamicsToolkit class when needed."""
    from .thermodynamics_toolkit import ThermodynamicsToolkit
    return ThermodynamicsToolkit

def get_phase_equilibrium():
    """Get PhaseEquilibrium class when needed."""
    from .phase_equilibrium import PhaseEquilibrium
    return PhaseEquilibrium

__all__ = [
    "get_thermodynamics_toolkit",
    "get_phase_equilibrium"
] 