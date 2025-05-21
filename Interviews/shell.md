**Create sequential folder**

```sh
for i in $(seq -w 1 111); do
    mkdir -p "/test/bin/$i"
done
```
