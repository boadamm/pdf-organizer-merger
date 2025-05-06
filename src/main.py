#!/usr/bin/env python3
"""
PDF Organizer & Merger - Main Application Entry Point

A desktop application for managing and manipulating PDF files.
"""
import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui.app import main


if __name__ == "__main__":
    main() 