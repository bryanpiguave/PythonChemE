"""
Web application package for Chemical Engineering Thermodynamics Toolkit.

This package contains the Flask web application and related components.
"""

__version__ = "1.0.0"
__author__ = "Bryan Piguave Llano"

# Import the Flask app
from .app import app

__all__ = ["app"] 