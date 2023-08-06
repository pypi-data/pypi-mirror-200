"""
Provides the top-level load function to users without having to import the loader explicitly.
Additionally, this hides internal functions of the loader.
"""
from .formatter import box, colorize, colorize_bg, heading, highlight, indent, pretty  # NOQA: F401
