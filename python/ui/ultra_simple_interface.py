# python/ui/interface.py
"""
Ultra-Simple Heat Reuse Calculator Interface
Everything users need in one beautiful, intuitive interface
"""

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from typing import Dict, Any
import matplotlib.pyplot as plt

from python.data.loader import CSVDataManager
from python.core.system_analysis import get_complete_system_analysis
from python.config.constants import DROPDOWN_OPTIONS, VALIDATION_RULES
from python.utils.formatting import format_display_value
from python.testing.test_widgets import MiniDebugInterface


class HeatReuseCalculator:
    """
    The main calculator interface - beautifully simple for users
    """
    
    def __init__(self):
        self.data_manager = CSVDataManager()
        self.debug_interface = MiniDebugInterface()
        
        # Interface state
        self.current_analysis = None
        self.interface_displayed = False
        
        # Widgets
        self.power_widget = None
        self.t1_widget = None
        self.temp_diff_widget = None