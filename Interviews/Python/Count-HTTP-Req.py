
import request 
import logging 

define dictionary to store counts

requests_counts = http_dict(int)

open log file 

with open('https_file.txt', 'r') as file:
   for line in file:
      match = re.search(r '(\d+ \d + \d + \d)', line) 
      if match :
          ip_address = match.group(1) 
          request_count[ip_address] +=1
          logging.info("Requests from {ip_address} found. Total Requests {request_counts[ip_address]}")
    else:
        logging.warning("No ip address found in line")

