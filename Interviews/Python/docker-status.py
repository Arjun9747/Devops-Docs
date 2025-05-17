import docker
import re
import defaultdict 

client = docker.from_env()

containers = client.container.list()

for containers in container:
  container_status = container.status
  container_name = container.name
  container_id =  container.short_id 

logs = container.logs(stdout= True, stderr = True)

keywords = ['Error', 'Warning', 'CRITICAL']
keyword_count = default_dict(int)

log_lines = logs.split("\n") 


for line in log_lines:
  for keyword in keywords:
    if re.search (r '\b' + keyword + r '\b', line, re.IGNORECASE):
      keyword_count[keyword] +=1

print (f "log analysis")
for keyword , count in keyword_count.items():
  print(f"{keyword} {count})
  
