import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app import BleScannerApp

if __name__ == "__main__":
    BleScannerApp().run()
