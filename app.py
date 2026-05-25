import sys
import os

# Add parent directory to path if running as script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=5000)
