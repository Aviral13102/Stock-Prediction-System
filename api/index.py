import os
import sys

# Add the project root to the Python path so it can find the src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.app import app
