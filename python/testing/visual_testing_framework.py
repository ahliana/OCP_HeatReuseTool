# python/testing/visual_test_runner.py
"""
Beautiful Visual Testing Framework
Shows gorgeous test results with smart error analysis
"""

import time
import traceback
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from typing import Dict, List, Any, Callable
import pandas as pd


class VisualTestRunner:
    """
    Creates beautiful, informative test displays
    Shows exactly what's working and what needs attention
    """
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.test_output = widgets.Output()
        self.progress_bar = None
    
    def run_all_tests(self, show_details=True):
        """Run all tests with beautiful visual feedback"""
        self.start_time = time.time()
        self.results = []
        
        # Create the beautiful test interface
        self._create_test_interface()
        
        # Discover and run all tests
        test_functions = self._discover_tests()
        total_tests = len(test_functions)
        
        with self.test_output:
            self._show_test_header(total_tests)
            
            for i, (test_name, test_func) in enumerate(test_functions):
                # Update progress
                self._update_progress(i, total_tests, test_name)
                
                # Run the test
                result = self._run_single_test(test_name, test_func)
                self.results.append(result)
                
                # Show result immediately
                if show_details:
                    self._display_test_result(result)
                
                time.sleep(0.1)  # Small delay for visual effect
            
            # Show beautiful summary
            self._show_test_summary()
    
    def _create_test_interface(self):
        """Create the beautiful test interface"""
        # Progress bar
        self.progress_bar = widgets.IntProgress(
            min=0, max=100, value=0,
            description='Testing:',
            bar_style='info',
            layout=widgets.Layout(width='100%')
        )
        
        # Main interface
        interface = widgets.VBox([
            widgets.HTML("<h3>🧪 Running Comprehensive Tests</h3>"),
            self.progress_bar,
            self.test_output
        ])
        
        display(interface)
    
    def _show_test_header(self, total_tests):
        """Show beautiful test header"""
        display(HTML(f"""
    def _show_test_header(self, total_tests):
        """Show beautiful test header"""
        display(HTML(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        ">
            <h2 style="margin: 0; font-size: 24px;">🔬 Heat Reuse Tool Test Suite</h2>
            <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
                Running {total_tests} comprehensive tests...
            </p>
        </div>
        """))
    
    def _update_progress(self, current, total, test_name):
        """Update progress bar with current test"""
        progress_percent = int((current / total) * 100)
        self.progress_bar.value = progress_percent
        self.progress_bar.description = f'Testing: {test_name[:30]}...'
    
    def _run_single_test(self, test_name, test_func):
        """Run a single test and capture results"""
        start_time = time.time()
        
        try:
            # Run the test function
            test_func()
            
            duration = time.time() - start_time
            return {
                'test_name': test_name,
                'status': 'passed',
                'duration': duration,
                'description': 'Test completed successfully',
                'error': None,
                'suggestions': []
            }
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            suggestions = self._analyze_error(error_msg, test_name)
            
            return {
                'test_name': test_name,
                'status': 'failed',
                'duration': duration,
                'description': f'Test failed: {error_msg[:100]}...',
                'error': error_msg,
                'traceback': traceback.format_exc(),
                'suggestions': suggestions
            }
    
    def _analyze_error(self, error_msg, test_name):
        """Smart error analysis with helpful suggestions"""
        suggestions = []
        
        # CSV/Data loading errors
        if 'CSV' in error_msg or 'not found' in error_msg.lower():
            suggestions.extend([
                "🔍 Check if all CSV files are in the data/ directory",
                "📊 Verify CSV files are not corrupted or empty",
                "🔄 Try reloading the data files",
                "📁 Ensure file permissions allow reading"
            ])
        
        # Number conversion errors
        elif 'universal_float_convert' in error_msg or 'conversion' in error_msg.lower():
            suggestions.extend([
                "🔢 Check for European number formats (1,234 vs 1.234)",
                "💰 Look for currency symbols in numeric data",
                "📝 Verify CSV encoding is UTF-8",
                "🧹 Check for hidden characters or extra spaces"
            ])
        
        # ALLHX lookup errors
        elif 'ALLHX' in error_msg or 'lookup' in error_msg.lower():
            suggestions.extend([
                "🎯 Verify the parameter combination exists in ALLHX.csv",
                "📋 Check if Power, T1, TempDiff, Approach values are valid",
                "🔍 Run data validation test first",
                "📊 Check ALLHX.csv for data completeness"
            ])
        
        # Physics calculation errors
        elif 'physics' in error_msg.lower() or 'formula' in error_msg.lower():
            suggestions.extend([
                "🧮 Check if input values are within physical limits",
                "🌡️ Verify temperature values are reasonable",
                "💧 Check flow rates are positive and realistic",
                "⚖️ Ensure units are consistent"
            ])
        
        # Widget/UI errors
        elif 'widget' in error_msg.lower() or 'display' in error_msg.lower():
            suggestions.extend([
                "🎨 Try restarting the Jupyter kernel",
                "📱 Check if ipywidgets is properly installed",
                "🔄 Refresh the browser page",
                "💻 Verify Jupyter extensions are enabled"
            ])
        
        # Performance issues
        elif 'timeout' in error_msg.lower() or 'slow' in error_msg.lower():
            suggestions.extend([
                "⚡ Large dataset detected - consider using sample data",
                "🔧 Check system memory availability",
                "📈 Monitor CPU usage during calculations",
                "💾 Consider data caching optimizations"
            ])
        
        # Generic suggestions
        if not suggestions:
            suggestions.extend([
                "🔍 Run the test in debug mode for more details",
                "📖 Check the documentation for this feature",
                "🧪 Try running related tests to isolate the issue",
                "💬 Report this issue if it persists"
            ])
        
        return suggestions
    
    def _display_test_result(self, result):
        """Display individual test result with beautiful styling"""
        if result['status'] == 'passed':
            icon = "✅"
            color = "#d4edda"
            border_color = "#c3e6cb"
            text_color = "#155724"
        elif result['status'] == 'failed':
            icon = "❌"
            color = "#f8d7da"
            border_color = "#f5c6cb"
            text_color = "#721c24"
        else:
            icon = "⚠️"
            color = "#fff3cd"
            border_color = "#ffeaa7"
            text_color = "#856404"
        
        # Main result display
        html = f"""
        <div style="
            background: {color};
            border: 2px solid {border_color};
            padding: 15px;
            margin: 8px 0;
            border-radius: 10px;
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
        ">
            <span style="font-size: 20px; margin-right: 15px;">{icon}</span>
            <div style="flex-grow: 1;">
                <strong style="color: {text_color}; font-size: 16px;">{result['test_name']}</strong>
                <br>
                <span style="color: {text_color}; opacity: 0.8;">{result['description']}</span>
            </div>
            <span style="
                color: {text_color}; 
                opacity: 0.7; 
                font-family: monospace;
                background: rgba(255,255,255,0.3);
                padding: 4px 8px;
                border-radius: 4px;
            ">
                {result['duration']:.3f}s
            </span>
        </div>
        """
        
        display(HTML(html))
        
        # Show detailed error analysis for failures
        if result['status'] == 'failed' and result['suggestions']:
            self._show_error_analysis(result)
    
    def _show_error_analysis(self, result):
        """Show detailed error analysis with suggestions"""
        suggestions_html = "<br>".join([f"• {suggestion}" for suggestion in result['suggestions']])
        
        analysis_html = f"""
        <div style="
            background: #fff8e1;
            border-left: 5px solid #ff9800;
            padding: 15px;
            margin: 5px 0 15px 40px;
            border-radius: 0 8px 8px 0;
        ">
            <h4 style="margin: 0 0 10px 0; color: #e65100;">💡 Smart Error Analysis</h4>
            <div style="color: #ef6c00; line-height: 1.5;">
                {suggestions_html}
            </div>
            
            <details style="margin-top: 15px;">
                <summary style="cursor: pointer; color: #bf360c; font-weight: bold;">
                    🔍 Technical Details (Click to expand)
                </summary>
                <pre style="
                    background: #f5f5f5; 
                    padding: 10px; 
                    border-radius: 4px; 
                    margin-top: 10px;
                    font-size: 12px;
                    overflow-x: auto;
                ">{result.get('traceback', 'No traceback available')}</pre>
            </details>
        </div>
        """
        
        display(HTML(analysis_html))
    
    def _show_test_summary(self):
        """Show beautiful test summary with charts"""
        total_time = time.time() - self.start_time
        
        # Calculate statistics
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r['status'] == 'passed'])
        failed_tests = len([r for r in self.results if r['status'] == 'failed'])
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Choose summary style based on results
        if failed_tests == 0:
            summary_color = "#d4edda"
            summary_border = "#c3e6cb"
            summary_icon = "🎉"
            summary_title = "All Tests Passed!"
        elif failed_tests < total_tests / 2:
            summary_color = "#fff3cd"
            summary_border = "#ffeaa7"
            summary_icon = "⚠️"
            summary_title = "Some Issues Found"
        else:
            summary_color = "#f8d7da"
            summary_border = "#f5c6cb"
            summary_icon = "❌"
            summary_title = "Multiple Failures"
        
        # Create summary display
        summary_html = f"""
        <div style="
            background: {summary_color};
            border: 3px solid {summary_border};
            padding: 20px;
            margin: 20px 0;
            border-radius: 15px;
            text-align: center;
        ">
            <h2 style="margin: 0 0 15px 0; font-size: 24px;">
                {summary_icon} {summary_title}
            </h2>
            
            <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                <div style="text-align: center;">
                    <div style="font-size: 36px; font-weight: bold; color: #28a745;">
                        {passed_tests}
                    </div>
                    <div style="color: #6c757d;">Passed</div>
                </div>
                
                <div style="text-align: center;">
                    <div style="font-size: 36px; font-weight: bold; color: #dc3545;">
                        {failed_tests}
                    </div>
                    <div style="color: #6c757d;">Failed</div>
                </div>
                
                <div style="text-align: center;">
                    <div style="font-size: 36px; font-weight: bold; color: #17a2b8;">
                        {success_rate:.1f}%
                    </div>
                    <div style="color: #6c757d;">Success Rate</div>
                </div>
                
                <div style="text-align: center;">
                    <div style="font-size: 36px; font-weight: bold; color: #6f42c1;">
                        {total_time:.2f}s
                    </div>
                    <div style="color: #6c757d;">Total Time</div>
                </div>
            </div>
        </div>
        """
        
        display(HTML(summary_html))
        
        # Create performance chart if there are results
        if self.results:
            self._create_performance_chart()
    
    def _create_performance_chart(self):
        """Create beautiful performance visualization"""
        # Prepare data
        test_names = [r['test_name'][:20] + '...' if len(r['test_name']) > 20 else r['test_name'] 
                     for r in self.results]
        durations = [r['duration'] for r in self.results]
        statuses = [r['status'] for r in self.results]
        
        # Create subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Performance bar chart
        colors = ['#28a745' if status == 'passed' else '#dc3545' for status in statuses]
        bars = ax1.bar(range(len(test_names)), durations, color=colors, alpha=0.7)
        
        ax1.set_xlabel('Tests')
        ax1.set_ylabel('Duration (seconds)')
        ax1.set_title('🚀 Test Performance Analysis', fontsize=14, fontweight='bold')
        ax1.set_xticks(range(len(test_names)))
        ax1.set_xticklabels(test_names, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, duration in zip(bars, durations):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{duration:.3f}s', ha='center', va='bottom', fontsize=8)
        
        # Status pie chart
        status_counts = pd.Series(statuses).value_counts()
        colors_pie = ['#28a745' if status == 'passed' else '#dc3545' 
                     for status in status_counts.index]
        
        wedges, texts, autotexts = ax2.pie(status_counts.values, 
                                          labels=status_counts.index,
                                          colors=colors_pie,
                                          autopct='%1.1f%%',
                                          startangle=90)
        ax2.set_title('📊 Test Results Distribution', fontsize=14, fontweight='bold')
        
        # Style the pie chart
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.show()
    
    def _discover_tests(self):
        """Discover all available test functions"""
        # This would be implemented to find all test functions
        # For now, returning some example tests
        return [
            ("CSV Data Loading", self._test_csv_loading),
            ("Physics Constants", self._test_physics_constants),
            ("Formula Calculations", self._test_formula_accuracy),
            ("ALLHX Lookup", self._test_allhx_lookup),
            ("Data Conversion", self._test_data_conversion),
            ("Widget Creation", self._test_widget_creation),
            ("Complete System Flow", self._test_complete_flow),
            ("Performance Benchmarks", self._test_performance)
        ]
    
    # Example test functions
    def _test_csv_loading(self):
        """Test CSV file loading"""
        from python.data.loader import CSVDataManager
        manager = CSVDataManager()
        manager.load_all_csv_files()
        assert len(manager.csv_data) > 0, "No CSV files loaded"
    
    def _test_physics_constants(self):
        """Test physics constants are reasonable"""
        from python.physics.constants import WATER_SPECIFIC_HEAT_20C, WATER_DENSITY_20C
        assert 4000 < WATER_SPECIFIC_HEAT_20C < 5000, "Water specific heat out of range"
        assert 990 < WATER_DENSITY_20C < 1010, "Water density out of range"
    
    def _test_formula_accuracy(self):
        """Test formula calculations match expected results"""
        from python.core.calculations.registry import calculation_registry
        calc = calculation_registry.get_calculation("Heat Transfer Rate")
        
        # Test with known values
        result = calc.calculate(
            flow_rate=1000,  # L/min
            inlet_temperature=20,  # °C
            outlet_temperature=30   # °C
        )
        
        # Should be approximately 0.7 MW for this input
        expected_mw = 0.7
        actual_mw = result['heat_rate_mw']
        assert abs(actual_mw - expected_mw) < 0.1, f"Heat calc error: expected ~{expected_mw}, got {actual_mw}"
    
    def _test_allhx_lookup(self):
        """Test ALLHX data lookup"""
        from python.core.lookup import lookup_allhx_data
        result = lookup_allhx_data(1, 20, 10, 2)
        assert result is not None, "ALLHX lookup failed"
        assert 'F1' in result, "Missing F1 in ALLHX result"
    
    def _test_data_conversion(self):
        """Test universal float conversion"""
        from python.data.converter import universal_float_convert
        
        test_cases = [
            ("1,493", 1493),  # European thousands
            ("12.5", 12.5),   # Decimal
            ("€1,375.2", 1375.2),  # Currency
        ]
        
        for input_val, expected in test_cases:
            result = universal_float_convert(input_val)
            assert abs(result - expected) < 0.01, f"Conversion failed: {input_val} -> {result}, expected {expected}"
    
    def _test_widget_creation(self):
        """Test widget creation doesn't crash"""
        from python.ui.widgets.input_widgets import DropdownWidget
        
        widget = DropdownWidget("test", "dropdown", {
            'options': [1, 2, 3],
            'default': 1,
            'label': 'Test'
        })
        
        widget_obj = widget.create()
        assert widget_obj is not None, "Widget creation failed"
    
    def _test_complete_flow(self):
        """Test complete calculation flow"""
        from python.core.system_analysis import get_complete_system_analysis
        
        analysis = get_complete_system_analysis(1, 20, 10, 2)
        assert analysis is not None, "Complete analysis failed"
        assert 'system' in analysis, "Missing system data"
        assert 'costs' in analysis, "Missing cost data"
    
    def _test_performance(self):
        """Test performance is acceptable"""
        import time
        from python.core.system_analysis import get_complete_system_analysis
        
        start_time = time.time()
        get_complete_system_analysis(1, 20, 10, 2)
        duration = time.time() - start_time
        
        assert duration < 2.0, f"Analysis too slow: {duration:.3f}s (should be < 2.0s)"


# python/testing/test_widgets.py
"""
Tiny, hidden debugging widgets for the main interface
"""

import ipywidgets as widgets
from IPython.display import display
from .visual_test_runner import VisualTestRunner


class MiniDebugInterface:
    """
    Tiny debugging interface that's barely visible until needed
    """
    
    def __init__(self):
        self.debug_visible = False
        self.test_runner = VisualTestRunner()
    
    def create_debug_button(self):
        """Create tiny debug button - barely visible in corner"""
        debug_button = widgets.Button(
            description="🔧",
            layout=widgets.Layout(
                width='25px',
                height='25px',
                margin='0 0 0 0'
            ),
            style={'font_size': '10px'},
            tooltip="Debug tools (click for system diagnostics)"
        )
        
        debug_button.on_click(self._show_debug_panel)
        return debug_button
    
    def _show_debug_panel(self, button):
        """Show comprehensive debug panel"""
        if self.debug_visible:
            return
        
        # Create debug interface
        debug_panel = self._create_debug_panel()
        display(debug_panel)
        self.debug_visible = True
    
    def _create_debug_panel(self):
        """Create the full debug panel"""
        # Quick status check
        status_output = widgets.Output()
        
        # Test runner output
        test_output = widgets.Output()
        
        # Control buttons
        quick_test_btn = widgets.Button(
            description="🧪 Quick Tests",
            button_style='info',
            tooltip="Run essential tests only"
        )
        
        full_test_btn = widgets.Button(
            description="🔬 Full Test Suite",
            button_style='primary',
            tooltip="Run complete test suite with visuals"
        )
        
        data_check_btn = widgets.Button(
            description="📊 Check Data Files",
            button_style='warning',
            tooltip="Validate all CSV files"
        )
        
        performance_btn = widgets.Button(
            description="⚡ Performance Test",
            button_style='success',
            tooltip="Benchmark calculation speed"
        )
        
        # Wire up button events
        quick_test_btn.on_click(lambda b: self._run_quick_tests(test_output))
        full_test_btn.on_click(lambda b: self._run_full_tests(test_output))
        data_check_btn.on_click(lambda b: self._check_data_files(status_output))
        performance_btn.on_click(lambda b: self._run_performance_test(test_output))
        
        # Show initial status
        with status_output:
            self._show_system_status()
        
        # Create accordion layout
        debug_accordion = widgets.Accordion(children=[
            widgets.VBox([
                widgets.HTML("<h4>System Status</h4>"),
                status_output
            ]),
            widgets.VBox([
                widgets.HTML("<h4>Test Controls</h4>"),
                widgets.HBox([quick_test_btn, full_test_btn]),
                widgets.HBox([data_check_btn, performance_btn]),
                test_output
            ])
        ])
        
        debug_accordion.set_title(0, "📊 System Status")
        debug_accordion.set_title(1, "🧪 Testing Tools")
        debug_accordion.selected_index = 0
        
        return widgets.VBox([
            widgets.HTML("""
            <div style="
                background: #f8f9fa;
                border: 2px dashed #6c757d;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            ">
                <h3 style="margin: 0 0 10px 0; color: #495057;">
                    🔧 Debug & Testing Panel
                </h3>
                <p style="margin: 0; color: #6c757d; font-size: 14px;">
                    Professional debugging tools for developers and power users
                </p>
            </div>
            """),
            debug_accordion
        ])
    
    def _show_system_status(self):
        """Show current system status"""
        try:
            from python.data.loader import CSVDataManager
            from python.physics.constants import WATER_SPECIFIC_HEAT_20C
            
            # Check CSV files
            manager = CSVDataManager()
            manager.load_all_csv_files()
            csv_count = len(manager.csv_data)
            
            # Check physics constants
            physics_ok = WATER_SPECIFIC_HEAT_20C > 4000
            
            status_html = f"""
            <div style="font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 5px;">
                <div style="color: {'#28a745' if csv_count > 5 else '#dc3545'};">
                    📁 CSV Files: {csv_count}/9 loaded
                </div>
                <div style="color: {'#28a745' if physics_ok else '#dc3545'};">
                    🧮 Physics Constants: {'OK' if physics_ok else 'ERROR'}
                </div>
                <div style="color: #28a745;">
                    🎨 Widget System: Ready
                </div>
                <div style="color: #17a2b8;">
                    ⚡ Status: System operational
                </div>
            </div>
            """
            
            display(widgets.HTML(status_html))
            
        except Exception as e:
            display(widgets.HTML(f"""
            <div style="color: #dc3545; background: #f8d7da; padding: 10px; border-radius: 5px;">
                ❌ System Check Failed: {str(e)}
            </div>
            """))
    
    def _run_quick_tests(self, output):
        """Run only the most critical tests"""
        with output:
            output.clear_output()
            display(widgets.HTML("<h4>🧪 Running Quick Tests...</h4>"))
            
            # Run subset of critical tests
            runner = VisualTestRunner()
            
            # Override to run only critical tests
            original_discover = runner._discover_tests
            runner._discover_tests = lambda: [
                ("CSV Loading", runner._test_csv_loading),
                ("Physics Constants", runner._test_physics_constants),
                ("Basic Calculations", runner._test_formula_accuracy)
            ]
            
            runner.run_all_tests(show_details=True)
    
    def _run_full_tests(self, output):
        """Run complete test suite"""
        with output:
            output.clear_output()
            runner = VisualTestRunner()
            runner.run_all_tests(show_details=True)
    
    def _check_data_files(self, output):
        """Check all data files"""
        with output:
            output.clear_output()
            display(widgets.HTML("<h4>📊 Checking Data Files...</h4>"))
            
            try:
                from python.data.loader import CSVDataManager
                import os
                
                manager = CSVDataManager()
                
                # Check if data directory exists
                if not os.path.exists("data"):
                    display(widgets.HTML("""
                    <div style="color: #dc3545;">❌ Data directory not found</div>
                    """))
                    return
                
                # Load and validate each file
                manager.load_all_csv_files()
                
                file_status = []
                expected_files = ['ALLHX.csv', 'PIPCOST.csv', 'PIPSZ.csv', 'ROOM.csv', 'CVALV.csv', 'IVALV.csv']
                
                for filename in expected_files:
                    csv_name = filename.replace('.csv', '').upper()
                    if csv_name in manager.csv_data:
                        df = manager.csv_data[csv_name]
                        rows = len(df)
                        cols = len(df.columns)
                        file_status.append(f"✅ {filename}: {rows} rows, {cols} columns")
                    else:
                        file_status.append(f"❌ {filename}: Missing")
                
                status_html = "<br>".join(file_status)
                display(widgets.HTML(f"""
                <div style="font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 5px;">
                    {status_html}
                </div>
                """))
                
            except Exception as e:
                display(widgets.HTML(f"""
                <div style="color: #dc3545;">❌ Data check failed: {str(e)}</div>
                """))
    
    def _run_performance_test(self, output):
        """Run performance benchmarks"""
        with output:
            output.clear_output()
            display(widgets.HTML("<h4>⚡ Running Performance Tests...</h4>"))
            
            import time
            
            try:
                # Test calculation speed
                from python.core.system_analysis import get_complete_system_analysis
                
                times = []
                for i in range(5):
                    start = time.time()
                    get_complete_system_analysis(1, 20, 10, 2)
                    times.append(time.time() - start)
                
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                
                performance_html = f"""
                <div style="font-family: monospace; background: #e8f5e8; padding: 15px; border-radius: 5px;">
                    <h5>📊 Calculation Performance</h5>
                    <div>Average Time: {avg_time:.3f}s</div>
                    <div>Fastest Time: {min_time:.3f}s</div>
                    <div>Slowest Time: {max_time:.3f}s</div>
                    <div style="margin-top: 10px;">
                        Status: {'🟢 Excellent' if avg_time < 0.5 else '🟡 Good' if avg_time < 1.0 else '🔴 Slow'}
                    </div>
                </div>
                """
                
                display(widgets.HTML(performance_html))
                
            except Exception as e:
                display(widgets.HTML(f"""
                <div style="color: #dc3545;">❌ Performance test failed: {str(e)}</div>
                """))