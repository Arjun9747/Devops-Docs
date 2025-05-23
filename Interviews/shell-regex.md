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
```







