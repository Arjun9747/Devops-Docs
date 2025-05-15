import json

# Log file path
LOG_FILE = "application.log"

def parse_json_logs(log_file):
    """Parse JSON logs and extract specific information."""
    with open(log_file, "r") as file:
        for line in file:
            try:
                # Parse each line as JSON
                log_entry = json.loads(line.strip())
                
                # Extract only ERROR logs
                if log_entry.get("level") == "ERROR":
                    timestamp = log_entry.get("timestamp")
                    message = log_entry.get("message")
                    user_id = log_entry.get("user_id")
                    
                    # Display extracted information
                    print(f"[ERROR] {timestamp} | User ID: {user_id} | Message: {message}")
            except json.JSONDecodeError as e:
                print(f"Failed to parse line: {line}. Error: {e}")

# Execute the log parser
parse_json_logs(LOG_FILE)
