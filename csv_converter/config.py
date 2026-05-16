"""
Configuration settings for CSV to Excel Converter Web App
"""

import os

# Application Settings
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# File Upload Settings
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'csv'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Excel Styling
HEADER_COLOR = "2E75B6"
LIGHT_BLUE = "DCE6F1"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S"
