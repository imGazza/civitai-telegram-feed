import logging
from pathlib import Path
import datetime
from datetime import datetime

def setup_logger():
    # Create logs directory
    logs_dir = Path(__file__).parent / "execution_logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(logs_dir / f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            logging.StreamHandler()  # This will also print to console
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logger()