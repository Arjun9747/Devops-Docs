**awk**

```csv
Alice,25,Engineer
Bob,30,Designer
Charlie,28,Manager
David,22,Engineer
Eve,30,Analyst
```

```shell
awk -F ',' `$3 = "Engineer" { print $1}'  data.txt

awk -F ',' '$3 ~ /sign/' data.txt   --> output Designer

awk '/error/ { print $0 }' logfile.txt --> matches line contains "error" word

awk $3 == 'error' { print $0 } logfile.txt  --> 3rd coln is error, print entire line,
                                                 $0 refers to the entire line of input.

awk '$1 == "INFO" && $3 ~ /timeout/ { print $0 }' logfile.txt

Matches lines where the first field is "INFO" and the third field contains "timeout".

awk 'BEGIN { print "Start Processing" }
     /error/ { count++ }
     END { print "Total error lines:", count }' logfile.txt

print start message, which matches the pattern "error" count it and display total number of count

```

**sed**

```shell
sed 's/old/new/' file --> replaces the first occurrence of the string "old" with "new" on each line of file.txt

sed 's/old/new/g ' file --> replaces the all occurrence of the string "old" with "new" on each line of file.txt

sed '/pattern/ s/foo/bar/' file --> replaces the pattern first occurance of foo with bar

sed '/^#/d' file	--> delete commented line

sed '5d' file	--> delete line 5 
```

Line 1

Line 2

Line 3

```shell
sed 'Line 2'/a Append new line
```

Line 1

Line 2

Appended Line

Line 3

sed -n '/error/p' file	

print only lines matching "error" pattern








