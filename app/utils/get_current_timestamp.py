from datetime import datetime, timezone

def get_current_timestamp_str():
    now = datetime.now(timezone.utc)
    timestamp_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return timestamp_str

def calculate_response_time(start_at: datetime) -> float:
    end_at = datetime.now()
    response_time = (end_at - start_at).total_seconds()
    return response_time