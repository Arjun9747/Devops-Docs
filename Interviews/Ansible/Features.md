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

*Register*

Register keyword is used to capture the output of a task (such as command output, status code, etc.) and store it in a variable.

```yaml
---
- name: Register output of a task
  hosts: all

  tasks:
  - name: Run a command and register output
    shell: "uptime"
    register: uptime_output

  - name: Display registered output
    debug:
      msg: "Uptime output: {{ uptime_output.stdout }}"
```

*Ansible Galaxy*

Ansible Galaxy is a repository of pre-built Ansible roles that can be easily installed and used in your playbooks. 

*Handlers*

Handlers are special tasks in Ansible that run only when notified by other tasks. They are typically used for actions that 

should happen only if something changed, such as:

Restarting a service

Reloading a configuration

Rebooting a system

*Notify*

Notify is a directive used in a task to trigger a handler when that task makes a change.

```yaml
---
- name: Configure NGINX and handle changes
  hosts: webservers
  become: yes

  tasks:

    - name: Copy NGINX configuration file
      copy:
        src: files/nginx.conf        # Source file in your Ansible project
        dest: /etc/nginx/nginx.conf  # Destination on target host
        owner: root
        group: root
        mode: '0644'
      notify: Restart NGINX

    - name: Ensure NGINX is running
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:

    - name: Restart NGINX
      service:
        name: nginx
        state: restarted
```

*Dynamic Inventory*

In Ansible, an inventory is a list of hosts (systems) you manage.

By default, Ansible uses a static inventory file (hosts), but this can become limiting when your infrastructure is dynamic — such as in cloud environments (AWS, Azure, GCP, etc.) where instances may start/stop/change frequently.

👉 Dynamic inventory solves this by generating the list of hosts programmatically at runtime, often from an API or script.

```yaml
# File: aws_ec2.yml

plugin: aws_ec2
regions:
  - us-east-1
  - us-west-2
filters:
  tag:Environment: dev
hostnames:
  - private-ip-address
compose:
  ansible_host: private_ip_address
```
The aws_ec2 plugin is used to generate the dynamic inventory.

The regions section specifies the AWS regions to query for EC2 instances.

The filters section specifies a filter to only include instances with the Environment tag set to dev.

*jinja files*

Generate config files (nginx.conf, sshd_config, httpd.conf, etc.)

Create scripts dynamically (e.g., startup.sh, install.sh)

Template cloud init or Terraform variables

Customize email templates, Slack messages, or alerts

*Structure*

name

host

become

vars 

roles 

The lineinfile module is used to ensure a specific line is present, absent, or replaced in a text file on a target machine.

```yaml
- name: Ensure a line is present in a file
  ansible.builtin.lineinfile:
    path: /etc/myconfig.conf
    line: 'export PATH=/usr/local/bin:$PATH'
```

*Grouping Host*

Grouping hosts in Ansible means organizing your inventory into groups based on criteria like environment, role, location, OS, etc

| Optimization Technique   | Benefit                            |
| ------------------------ | ---------------------------------- |
| Loops                    | Reduce repetition, concise code    |
| Native modules           | Idempotent and optimized           |
| Handlers                 | Avoid unnecessary service restarts |
| Fact caching             | Speed up repeated runs             |
| Delegation & Async       | Efficient task distribution        |
| Play-level `become`      | Cleaner, less repetition           |
| Selective fact gathering | Faster playbook start              |
| Tags                     | Run partial playbooks              |
| Roles                    | Modular, reusable code             |

*Delegate*

Sometimes a task must be run on a specific control node or jump host instead of the target host. For example, copying 

files from one host to another, or running a command on the control machine while managing remote hosts.

*Async*

Run tasks asynchronously, allowing the playbook to continue without waiting for the task to finish.

async: maximum time (in seconds) allowed for the task to run

poll: 0: fire and forget (don’t wait for the result)

*Selective Fact Gathering*

Gathering facts can be slow, especially on many hosts or when you don’t need all facts. Selective gathering or disabling it speeds up playbook execution

| Feature                      | Purpose                                         | Example Use Case                          |
| ---------------------------- | ----------------------------------------------- | ----------------------------------------- |
| **Delegation**               | Run task on different host (e.g., control node) | Copy files from remote to local           |
| **Async**                    | Run long tasks without blocking playbook        | Run backup or build jobs in background    |
| **Selective Fact Gathering** | Speed up execution by limiting gathered facts   | Skip gathering or gather only needed info |

