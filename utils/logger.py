import logging
import os
from datetime import datetime

# Create reports/logs directory if not exists
log_dir = os.path.join("reports", "logs")
os.makedirs(log_dir, exist_ok=True)

# Log file name per run
log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Configure logger
logger = logging.getLogger("TestLogger")
logger.setLevel(logging.INFO)

# File handler
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add handlers
logger.addHandler(fh)
logger.addHandler(ch)
