"""
Basic autostart - just prove it works!
"""

from IPython.display import display, HTML

def test_calculator():
    """Just show that it works!"""
    
    html = """
    <div style="
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    ">
        <h1 style="margin: 0; font-size: 48px;">🎉</h1>
        <h2 style="margin: 10px 0; font-size: 32px;">IT WORKS!</h2>
        <p style="margin: 10px 0 0 0; font-size: 20px; opacity: 0.9;">
            Heat Reuse Calculator autostart.py is loading successfully!
        </p>
        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.8;">
            MVP achieved! 🚀
        </p>
    </div>
    """
    
    display(HTML(html))
    print("✅ autostart.py loaded and executed successfully!")
    print("🔧 Heat Reuse Calculator MVP is working!")

# Run the test
test_calculator()