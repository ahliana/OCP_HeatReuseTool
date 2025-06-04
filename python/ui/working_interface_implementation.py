# python/ui/interface.py
"""
Heat Reuse Calculator - Main Interface
This is the working implementation that your notebook can import
"""

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import numpy as np


class HeatReuseCalculator:
    """
    Professional Heat Reuse System Calculator
    
    This class provides a beautiful, simple interface for heat recovery analysis.
    It automatically loads data, creates the interface, and performs calculations.
    """
    
    def __init__(self):
        print("🔧 Heat Reuse Calculator initializing...")
        
        # Initialize state
        self.csv_data = {}
        self.current_analysis = None
        
        # Load data
        self._load_csv_data()
        
        # Create interface components
        self._create_widgets()
        
        print("✅ Calculator ready!")
    
    def _load_csv_data(self):
        """Load all CSV files from the Data directory"""
        try:
            data_dir = "Data"  # Your Data directory
            if not os.path.exists(data_dir):
                print(f"⚠️ Data directory '{data_dir}' not found")
                return
            
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            
            for file in csv_files:
                df_name = os.path.splitext(file)[0].upper()
                file_path = os.path.join(data_dir, file)
                
                try:
                    self.csv_data[df_name] = pd.read_csv(file_path)
                    print(f"📁 Loaded: {file}")
                except Exception as e:
                    print(f"❌ Failed to load {file}: {e}")
            
            print(f"📊 Total CSV files loaded: {len(self.csv_data)}")
            
        except Exception as e:
            print(f"❌ Error loading CSV data: {e}")
    
    def _create_widgets(self):
        """Create the user interface widgets"""
        # Shared styling
        style = {'description_width': '140px'}
        layout = widgets.Layout(width='300px', margin='5px')
        
        # Input widgets
        self.power_widget = widgets.Dropdown(
            options=[1, 2, 3, 4, 5],
            value=1,
            description='System Power:',
            tooltip='Heat recovery system capacity (MW)',
            style=style,
            layout=layout
        )
        
        self.t1_widget = widgets.Dropdown(
            options=[20, 30, 45],
            value=20,
            description='Target Temp:',
            tooltip='Target outlet temperature (°C)',
            style=style,
            layout=layout
        )
        
        self.temp_diff_widget = widgets.Dropdown(
            options=[10, 12, 14],
            value=10,
            description='Temperature Rise:',
            tooltip='Temperature increase across system (°C)',
            style=style,
            layout=layout
        )
        
        self.approach_widget = widgets.Dropdown(
            options=[2, 3, 5],
            value=2,
            description='Approach:',
            tooltip='Heat exchanger approach temperature',
            style=style,
            layout=layout
        )
        
        # Calculate button
        self.calculate_button = widgets.Button(
            description='🚀 Calculate System',
            button_style='success',
            tooltip='Calculate complete system analysis',
            icon='calculator',
            layout=widgets.Layout(
                width='250px', 
                height='50px', 
                margin='20px auto'
            ),
            style={'font_size': '16px', 'font_weight': 'bold'}
        )
        
        # Output areas
        self.system_output = widgets.Output()
        self.cost_output = widgets.Output()
        self.chart_output = widgets.Output()
        self.status_output = widgets.Output()
        
        # Connect button to calculation
        self.calculate_button.on_click(self._on_calculate_click)
        
        # Auto-calculate on input change
        for widget in [self.power_widget, self.t1_widget, self.temp_diff_widget, self.approach_widget]:
            widget.observe(self._on_input_change, names='value')
    
    def _on_input_change(self, change):
        """Handle input changes - auto-calculate with small delay"""
        import time
        if not hasattr(self, '_last_change_time'):
            self._last_change_time = 0
        
        current_time = time.time()
        if current_time - self._last_change_time > 0.5:  # 500ms delay
            self._perform_calculation()
        self._last_change_time = current_time
    
    def _on_calculate_click(self, button):
        """Handle calculate button click"""
        self._perform_calculation()
    
    def _perform_calculation(self):
        """Perform the main calculation"""
        try:
            # Update button state
            self.calculate_button.description = '⏳ Calculating...'
            self.calculate_button.disabled = True
            
            # Get input values
            power = self.power_widget.value
            t1 = self.t1_widget.value
            temp_diff = self.temp_diff_widget.value
            approach = self.approach_widget.value
            t2 = t1 + temp_diff
            
            # Show current parameters
            with self.status_output:
                clear_output()
                display(HTML(f"""
                <div style="background: #e8f5e9; padding: 10px; border-radius: 5px; margin: 10px 0;">
                    <strong>🔧 Calculating:</strong> {power}MW, {t1}°C→{t2}°C, Approach {approach}
                </div>
                """))
            
            # Try to use existing calculation functions if available
            if self._try_existing_calculation(power, t1, temp_diff, approach):
                return
            
            # Otherwise, do basic calculation
            self._basic_calculation(power, t1, temp_diff, approach)
            
        except Exception as e:
            self._show_error(f"Calculation failed: {str(e)}")
        
        finally:
            # Reset button
            self.calculate_button.description = '🚀 Calculate System'
            self.calculate_button.disabled = False
    
    def _try_existing_calculation(self, power, t1, temp_diff, approach):
        """Try to use existing calculation functions from the notebook"""
        try:
            # Check if the main calculation function exists in the global namespace
            import __main__
            
            if hasattr(__main__, 'get_complete_system_analysis'):
                print("🔧 Using existing calculation functions...")
                analysis = __main__.get_complete_system_analysis(power, t1, temp_diff, approach)
                
                if analysis:
                    self.current_analysis = analysis
                    self._display_full_results()
                    return True
                else:
                    self._show_error("No data found for these parameters in ALLHX lookup")
                    return True
            
            # Try direct ALLHX lookup
            elif hasattr(__main__, 'lookup_allhx_data'):
                print("🔧 Using ALLHX lookup...")
                result = __main__.lookup_allhx_data(power, t1, temp_diff, approach)
                
                if result:
                    self._display_allhx_results(result)
                    return True
                else:
                    self._show_error("No ALLHX data found for these parameters")
                    return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Could not use existing functions: {e}")
            return False
    
    def _basic_calculation(self, power, t1, temp_diff, approach):
        """Perform basic calculation when existing functions aren't available"""
        t2 = t1 + temp_diff
        
        # Basic heat transfer calculation
        # Estimated flow rates (simplified)
        estimated_f1 = power * 1000 / (4.186 * temp_diff)  # Rough estimate in L/min
        estimated_f2 = estimated_f1 * 0.95  # Slightly less
        
        # Estimated temperatures for consumer side
        t3 = t1 + temp_diff - 2  # Approach temperature difference
        t4 = t1 - approach
        
        # Basic cost estimates
        pipe_cost = power * 1000  # €1000 per MW
        hx_cost = power * 10000   # €10000 per MW
        valve_cost = power * 500  # €500 per MW
        total_cost = pipe_cost + hx_cost + valve_cost
        
        # Create basic analysis structure
        self.current_analysis = {
            'system': {
                'power': power,
                'T1': t1,
                'T2': t2,
                'T3': t3,
                'T4': t4,
                'F1': estimated_f1,
                'F2': estimated_f2
            },
            'costs': {
                'total_pipe_cost': pipe_cost,
                'hx_cost': hx_cost,
                'total_valve_cost': valve_cost,
                'total_cost': total_cost
            },
            'sizing': {
                'room_size': 12.5,
                'primary_pipe_size': 100
            }
        }
        
        self._display_basic_results()
    
    def _display_full_results(self):
        """Display complete results using existing analysis"""
        if not self.current_analysis:
            return
        
        # Display system parameters
        self._display_system_parameters()
        
        # Display cost analysis
        self._display_cost_analysis()
        
        # Try to display charts
        self._display_charts()
    
    def _display_allhx_results(self, allhx_result):
        """Display results from ALLHX lookup"""
        with self.system_output:
            clear_output()
            
            html = f"""
            <div style="
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 20px;
                border-radius: 12px;
                margin: 15px 0;
                border: 2px solid #2196F3;
            ">
                <h3 style="color: #1976D2; margin-top: 0;">✅ ALLHX System Results</h3>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div style="background: white; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #1976D2; margin: 0 0 10px 0;">🌡️ Temperatures</h4>
                        <div style="font-family: monospace; line-height: 1.6;">
                            <div><strong>T1:</strong> {allhx_result.get('T1', 'N/A')}°C</div>
                            <div><strong>T2:</strong> {allhx_result.get('T2', 'N/A')}°C</div>
                            <div><strong>T3:</strong> {allhx_result.get('T3', 'N/A')}°C</div>
                            <div><strong>T4:</strong> {allhx_result.get('T4', 'N/A')}°C</div>
                        </div>
                    </div>
                    
                    <div style="background: white; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #1976D2; margin: 0 0 10px 0;">💧 Flow Rates</h4>
                        <div style="font-family: monospace; line-height: 1.6;">
                            <div><strong>F1:</strong> {allhx_result.get('F1', 'N/A')} L/min</div>
                            <div><strong>F2:</strong> {allhx_result.get('F2', 'N/A')} L/min</div>
                            <div><strong>HX Cost:</strong> €{allhx_result.get('hx_cost', 'N/A')}</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            
            display(HTML(html))
    
    def _display_basic_results(self):
        """Display basic calculation results"""
        system = self.current_analysis['system']
        costs = self.current_analysis['costs']
        
        with self.system_output:
            clear_output()
            
            system_html = f"""
            <div style="
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 20px;
                border-radius: 12px;
                margin: 15px 0;
                border: 2px solid #2196F3;
            ">
                <h3 style="color: #1976D2; margin-top: 0;">✅ System Parameters (Estimated)</h3>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div style="background: white; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #1976D2; margin: 0 0 10px 0;">🌡️ Temperatures</h4>
                        <div style="font-family: monospace; line-height: 1.6;">
                            <div><strong>T1 (Out to TCS):</strong> {system['T1']}°C</div>
                            <div><strong>T2 (In from TCS):</strong> {system['T2']}°C</div>
                            <div><strong>T3 (Out to Consumer):</strong> {system['T3']}°C</div>
                            <div><strong>T4 (In from Consumer):</strong> {system['T4']}°C</div>
                        </div>
                    </div>
                    
                    <div style="background: white; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #1976D2; margin: 0 0 10px 0;">💧 Flow Rates</h4>
                        <div style="font-family: monospace; line-height: 1.6;">
                            <div><strong>F1 (TCS Flow):</strong> {system['F1']:.0f} L/min</div>
                            <div><strong>F2 (FWS Flow):</strong> {system['F2']:.0f} L/min</div>
                            <div><strong>Power:</strong> {system['power']} MW</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            
            display(HTML(system_html))
        
        with self.cost_output:
            clear_output()
            
            cost_html = f"""
            <div style="
                background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%);
                padding: 20px;
                border-radius: 12px;
                margin: 15px 0;
                border: 2px solid #FF9800;
            ">
                <h3 style="color: #F57C00; margin-top: 0;">💰 Cost Analysis (Estimated)</h3>
                
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <div style="font-family: monospace; line-height: 1.8;">
                        <div><strong>Pipe Costs:</strong> €{costs['total_pipe_cost']:,.0f}</div>
                        <div><strong>Heat Exchanger:</strong> €{costs['hx_cost']:,.0f}</div>
                        <div><strong>Valve Costs:</strong> €{costs['total_valve_cost']:,.0f}</div>
                    </div>
                </div>
                
                <div style="
                    background: #4CAF50;
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                ">
                    <h2 style="margin: 0; font-size: 28px;">
                        💡 TOTAL COST: €{costs['total_cost']:,.0f}
                    </h2>
                </div>
                
                <div style="
                    background: #fff3cd;
                    padding: 10px;
                    border-radius: 5px;
                    margin-top: 15px;
                    font-size: 14px;
                ">
                    <strong>Note:</strong> These are estimated values. For precise calculations, 
                    run your existing calculation functions in the notebook first.
                </div>
            </div>
            """
            
            display(HTML(cost_html))
    
    def _display_system_parameters(self):
        """Display system parameters from full analysis"""
        # This would use your existing display code
        with self.system_output:
            clear_output()
            display(HTML("<h3>✅ Full system parameters would display here</h3>"))
    
    def _display_cost_analysis(self):
        """Display cost analysis from full analysis"""
        # This would use your existing cost display code
        with self.cost_output:
            clear_output()
            display(HTML("<h3>💰 Full cost analysis would display here</h3>"))
    
    def _display_charts(self):
        """Display charts"""
        with self.chart_output:
            clear_output()
            
            try:
                # Try to use existing chart function
                import __main__
                if hasattr(__main__, 'create_system_charts') and self.current_analysis:
                    __main__.create_system_charts(self.current_analysis)
                else:
                    # Create basic chart
                    self._create_basic_chart()
            except Exception as e:
                display(HTML(f"""
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px;">
                    <strong>📊 Charts:</strong> Chart generation not available ({str(e)})
                </div>
                """))
    
    def _create_basic_chart(self):
        """Create a basic chart when full charting isn't available"""
        if not self.current_analysis:
            return
        
        system = self.current_analysis['system']
        
        # Simple temperature chart
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        temps = [system['T1'], system['T2'], system['T3'], system['T4']]
        labels = ['T1\n(Out to TCS)', 'T2\n(In from TCS)', 'T3\n(Out to Consumer)', 'T4\n(In from Consumer)']
        colors = ['#ff9999', '#ff6666', '#66b3ff', '#3399ff']
        
        bars = ax.bar(labels, temps, color=colors)
        ax.set_title('System Temperatures', fontsize=14, fontweight='bold')
        ax.set_ylabel('Temperature (°C)')
        
        # Add value labels on bars
        for bar, temp in zip(bars, temps):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{temp}°C', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def _show_error(self, message):
        """Show error message"""
        with self.status_output:
            clear_output()
            display(HTML(f"""
            <div style="
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border: 2px solid #f5c6cb;
            ">
                <strong>❌ Error:</strong> {message}
            </div>
            """))
    
    def display(self):
        """Display the complete calculator interface"""
        # Create beautiful header
        header_html = """
        <div style="
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        ">
            <h1 style="margin: 0; font-size: 32px; font-weight: bold;">
                🔧 Heat Reuse System Calculator
            </h1>
            <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">
                Professional heat recovery analysis made simple
            </p>
        </div>
        """
        
        # Input controls section
        input_section = widgets.VBox([
            widgets.HTML("""
            <div style="
                background: #e8f5e9;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                border-left: 5px solid #4CAF50;
            ">
                <h3 style="margin: 0 0 10px 0; color: #2e7d32;">📊 System Parameters</h3>
                <p style="margin: 0; color: #555; font-size: 14px;">
                    Select your system requirements. Results update automatically.
                </p>
            </div>
            """),
            widgets.HBox([
                widgets.VBox([self.power_widget, self.t1_widget]),
                widgets.VBox([self.temp_diff_widget, self.approach_widget])
            ], layout=widgets.Layout(justify_content='center'))
        ])
        
        # Complete interface
        main_interface = widgets.VBox([
            widgets.HTML(header_html),
            input_section,
            widgets.HBox([self.calculate_button], layout=widgets.Layout(justify_content='center')),
            self.status_output,
            self.system_output,
            self.cost_output,
            self.chart_output
        ], layout=widgets.Layout(
            border='3px solid #4CAF50',
            border_radius='15px',
            padding='25px',
            margin='10px',
            background_color='#fafafa'
        ))
        
        display(main_interface)
        
        # Auto-calculate with default values for immediate results
        self._perform_calculation()
        
        print("🎉 Heat Reuse Calculator is ready! Adjust the parameters above to see results.")
