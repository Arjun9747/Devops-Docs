**Create sequential folder**

```sh
for i in $(seq -w 1 111); do
    mkdir -p "/test/bin/$i"
done
```

**Renaming file extenstion**

```shell

echo "hello world" | cut -c 1-5

Output: hello

echo "user1:x:1001:1001:User One:/home/user1:/bin/bash" | cut -d ':' -f 1,5

-d ':' sets colon as the delimiter; -f 1,5 extracts the 1st and 5th fields

```

```shell
ls | cut -d . -f1 | xargs -i mv {}.txt {}.log

ls --> list the file 

cut -d .f1 --> split each filename using .dot and keeps only the first field (f1)

xargs takes each output line from the previous command and runs the mv command with it

i tells xargs to replace {} with each input

So for file1, the command becomes

mv file1.txt file1.log
```
**Redirection**

">:" Redirects an output

```shell
"Hello" > file.txt
```
">>" Appends 

```shell
"Hello" >> file.txt --> add the word to the end of the text
```

**Error Redirection**

"2>"

```shell
2> error.log --> redirects error message
```

"2>>"

```shell
2>> error.log will append error messages to error.log
```

**Output and Redirection**

"&>"
```shell
&> output.log  --> Redirects both stdout and stderr to a file
```

"&>>"

```shell
&>> output.log will append both output and error messages to output.log
```
**Input Redirection**

```shell
sort < file.txt will sort the contents of file.txt.
```

$0	--> script name 

1, $2, $3, etc. --> echo first second and third arguments 

$#	--> number of command line arguments 

$?	--> Exit status 

$$	--> PID 

**Loops**

```shell
for i in {1..5}; do
  if [ $i -eq 3 ]; then
    continue
  fi
  echo "$i"
done

for file in $file; do
  mv $file "${file%.txt}.log"


data="value123"
echo "${data%23}"   ##output --> 1
```


#

i=1
while [ $i -le 5 ]; do
  echo "$i"
  i=$((i + 1))
done

for file in *.log; do
    echo "Processing $file"
done

```

exit 0 # sucessfull termination

exit 1 # general error 

exit $ # exit status of last command 

set -e # command exits if there is an error in command 

set -o pipefail # pipeline command fails for non-zero exit status 

set -x # debug error 

ps # process status --> info about running process 

top # real time info 

kill # execute SIGTERM(terminate) , SIGKILL (force kill)

no hup # no hung up --> command continue to run after session termination

& ./run.sh  # used to run command in backgroud

jobs # runs background jobs 

fg # bring background job to foreground 

bg # send the  the background 

sleep 5  # pause for 5 seconds

wait $!  # wait for the last background job to complete

wait 1234  # wait for process with PID 1234 to complete

| Command | Description | Example |
| --- | --- | --- |
| `cut` | Extract specific fields from lines | `cut -d':' -f1 /etc/passwd` (Get usernames) |
| `awk` | Pattern scanning and processing | `awk '{print $1, $3}' users.txt` (Print 1st & 3rd columns) |
| `sed` | Stream editor for modifying text | `sed 's/error/ERROR/g' log.txt` (Replace 'error' with 'ERROR') |

```shell
admin:x:0:0:root:/root:/bin/bash
```

| Expression         | Description                      | Example Input          | Result         |
|--------------------|----------------------------------|-------------------------|----------------|
| `${var%suffix}`    | Remove shortest match from end   | `"logfile.txt"`         | `"logfile"`    |
| `${var%%suffix}`   | Remove longest match from end    | `"archive.tar.gz"`      | `"archive"`    |
| `${var#prefix}`    | Remove shortest match from start | `"v1.2.3-release"`      | `"1.2.3-release"` |
| `${var##prefix}`   | Remove longest match from start  | `"v1.2.3-release"`      | `"release"`    |

path="abcd.txt"

echo "${path%.txt}"  # Output: abcd

echo "${path##*.}"  # Output: txt

echo "root:x:0:0:root:/root:/bin/bash" | awk -F ':' '{print $5}'

uniq only removes consecutive duplicates, so it doesn’t help unless the input is sorted.

```shell
sort names.txt | uniq
```

Check if file exist
-e --> for if **exists**
```shell
if [ -e /var/www/html/index.html ]; then
  echo "File exists"
else 
  echo "File does not exist"
fi 
```
**Cron job**
```shell
0 0 * * * /home/ubuntu/script.sh
```
M H D M Day of Week Command 

**$? hold the exist status of the command
```shell
if [ $? -eq 0 ]; then
  echo "command executed successfully"
else
  echo "Command failed execution"
fi
```
**Get disk usage information, excluding certain filesystems**

```shell
df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output; do
    usage=$(echo $output | awk '{ print $1}' | sed 's/%//g')
    partition=$(echo $output | awk '{ print $2 }')
    if [ $usage -ge $THRESHOLD ]; then
        echo "Alert: High disk usage on $partition ($usage%)"
        # Send email or other alert here (e.g., using mail command)
    fi
done
```
**Check if the service is active**

if ! systemctl is-active --quiet $SERVICE; then
    echo "$SERVICE is not running, starting it..."
    systemctl start $SERVICE
    echo "$SERVICE started"
else
    echo "$SERVICE is already running"
fi

**Find and archive logs older than 7 days**

```shell
find $LOG_DIR -type f -mtime +7 -exec tar -rvf $BACKUP_DIR/logs_backup_$(date +%F).tar {} \;
 -exec rm {} \;
echo "Logs older than 7 days have been backed up and deleted."
```
-m time 
-c time -ownership/permission
-a time - access time 

**Loop through each service and check its status**
```shell
#!/bin/bash
SERVICES=("nginx" "mysql" "redis")

for SERVICE in "${SERVICES[@]}"; do
    if ! systemctl is-active --quiet $SERVICE; then
        echo "$SERVICE is not running, restarting it..."
        systemctl restart $SERVICE
        echo "$SERVICE restarted"
    else
        echo "$SERVICE is running"
    fi
done
```
```code
┌──────────── minute (0 - 59)
│ ┌────────── hour (0 - 23)
│ │ ┌──────── day of month (1 - 31)
│ │ │ ┌────── month (1 - 12)
│ │ │ │ ┌──── day of week (0 - 7) (Sunday is 0 or 7)
│ │ │ │ │
│ │ │ │ │
0 0 * * * /path/to/your/script.sh
```

*To get files modified (mtime) or metadata-changed (ctime) in the last 7 days*

```bash
#!bin/bash

#default directory is current directory
DIR = "${1:-.}"

find $DIR -type f \(-mtime -7 -o -ctime -7"\) | while -r file; do
mtime = $(stat -c "%y" "$file")
ctime = $(stat -c "%z" "$file")

echo "$mtime"
echo "$ctime"
done
```









