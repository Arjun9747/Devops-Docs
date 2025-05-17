import subprocess
import logging 
import platform

#check if server is rechable 

def ping_server(server):
  try:
    if plaform.system().lower() == "windows":
      output = subprocess.check_output(["ping", "-n", "1" , server])
    else:
      platform.system().lower() == "linux":
      output = subprocess.check_output(["ping","c","1", server]) 
      return True
  except subprocess.CalledProcessError:
    return False
  except Exception as e:
    logging.error(f"an error occured"{e}") 

#Return dict with server name as key and boolean value indicating if it is rechanble 

def check_server(servers):
   results = {}
   for server in servers:
     results[server] = ping_server(server)
  return results
