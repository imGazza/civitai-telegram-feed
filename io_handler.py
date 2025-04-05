import json
from datetime import datetime
from dataclasses import asdict
import glob
from model import image

def save_new_log(images: list[image.Image], username):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'{username}_{timestamp}.json'

    new_log_json = create_log_json(images)

    try:
        os.makedirs('logs', exist_ok=True)
        # Save file in logs directory
        log_path = os.path.join('logs', file_name)
        with open(log_path, 'w', encoding='utf-8') as file:
            json.dump(new_log_json, file, indent=4)
    except IOError as e:
        # Delete the file if it was created but had an error while writing
        if file_name and os.path.exists(file_name):
            os.remove(file_name)

def create_log_json(images: list[image.Image]): 
    return {
        'images_ids': [image.id for image in images],
        'images': [asdict(image) for image in images]
    }

def get_last_saved_log(username):
    # Get all log files for this username
    log_pattern = os.path.join('logs', f'{username}_*.json')
    log_files = glob.glob(log_pattern)
    if not log_files:
        return None
        
    # Sort files by name (timestamp) and get the last one
    latest_log = max(log_files)
    
    with open(latest_log, 'r', encoding='utf-8') as file:
        return json.load(file)
