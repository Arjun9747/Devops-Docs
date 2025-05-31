*Facts*

Pieces of information collected by ansible 

```yaml
---
- name: Gather facts and display system information
  hosts: all
  gather_facts: yes

  tasks:
  - name: Display system information
    debug:
      msg: |
        OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
        IP Address: {{ ansible_default_ipv4.address }}
        Memory: {{ ansible_memtotal_mb }} MB
```


