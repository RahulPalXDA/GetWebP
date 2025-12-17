# WSGI Configuration
# Point your WSGI configuration file to this file

import sys
import os

# Add your project directory to sys.path
project_home = '/home/YOUR_USERNAME/GetWebP'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import and initialize the Flask app
from app import app as application, init_db

# Initialize database on first run
init_db()
