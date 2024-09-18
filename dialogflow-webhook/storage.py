import json
import os
from datetime import datetime, timezone
LOGS_DIR = 'logs'
LOG_FILE = os.path.join(LOGS_DIR, 'conversations.json')

def save_log_entry(user_id, user_message, bot_response):
    # Ensure logs directory exists
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    
    # Prepare log entry
    log_entry = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'user_id': user_id,
        'user_message': user_message,
        'bot_response': bot_response,
    }
    
    # Load existing logs
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = []
    
    # Append new log entry
    data.append(log_entry)
    
    # Save logs back to file
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=4)
