import logging
from pathlib import Path
from datetime import datetime
import sys

def setup_logger():
    try:
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
        
        # Add exception hook to catch unhandled exceptions
        def handle_exception(exc_type, exc_value, exc_traceback):
            logger = logging.getLogger(__name__)
            logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
            sys.__excepthook__(exc_type, exc_value, exc_traceback)  # Call the default handler
        
        sys.excepthook = handle_exception
        
        return logging.getLogger(__name__)
    except Exception as e:
        # Fallback logging to ensure we at least capture initialization errors
        fallback_log = Path(__file__).parent / "execution_logs" / "logger_setup_error.log"
        with open(fallback_log, 'a') as f:
            f.write(f"\n{datetime.now()} - ERROR - Logger setup failed: {str(e)}")
        raise

logger = setup_logger()