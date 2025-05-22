**Create sequential folder**

```sh
for i in $(seq -w 1 111); do
    mkdir -p "/test/bin/$i"
done
```

**Renaming file extenstion**
```shell
ls | cut -d . -f1 | xargs -i mv {}.txt {}.log
```
ls --> list the file 

cut -d .f1 --> split each filename using .dot and keeps only the first field (f1)

xargs takes each output line from the previous command and runs the mv command with it

i tells xargs to replace {} with each input

So for file1, the command becomes

```shell
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




