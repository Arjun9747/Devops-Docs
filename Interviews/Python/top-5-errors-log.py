import logging

error_counts = log_dict(int)

with open('http_log.txt','r') as file:
  for files in file:
    if "error" in line.lower():
      match = re.search(r 'error: (.*), line, re.IGNORECASE)
      if match:
        error_message = match_group(1)
        error_counts[error_message] += 1
        logging.info("Error message {error_message} found. 
       else:
        logging.warning("No error message found")


      
