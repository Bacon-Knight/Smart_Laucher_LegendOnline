import logging
import os
import sys

def get_logger(name="Launcher"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler (in AppData)
        app_data_path = os.getenv('LOCALAPPDATA') or os.path.expanduser('~')
        log_dir = os.path.join(app_data_path, "LegendOnlineLauncher")
        os.makedirs(log_dir, exist_ok=True)
        
        fh = logging.FileHandler(os.path.join(log_dir, "launcher.log"), encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
