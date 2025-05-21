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
xargs takes each output line from the previous command and runs the mv command with it.
i tells xargs to replace {} with each input.
So for file1, the command becomes
```shell
mv file1.txt file1.log
```
