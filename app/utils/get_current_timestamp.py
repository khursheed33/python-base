from datetime import datetime
def get_current_timestamp_str():
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    return timestamp_str