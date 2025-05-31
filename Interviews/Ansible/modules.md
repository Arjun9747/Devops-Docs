**ansible.builtin**

 When you use a module like yum, copy, or user in your playbook, you are actually using modules from the ansible.builtin collection, even if you don't explicitly write the prefix.

Example: ansible.builtin.yum or just yum means the same module.

ansible.builtin.lineinfile: Edit text files line by line

async specifies the maximum time to wait for the task to complete.

poll: 0 tells Ansible not to wait for the task to finish immediately.

**CIA implementation**

**1. Confidentiality (Protecting data/privacy)**

ansible.builtin.user & ansible.builtin.group

Manage user accounts and groups to control who can access the system.

ansible.builtin.file

Manage file permissions and ownership to restrict access to sensitive files and directories.

ansible.builtin.copy or ansible.builtin.template (with mode parameter)

Deploy configuration files with secure permissions.

ansible.builtin.seboolean (SELinux booleans)

Manage SELinux booleans to enforce security policies on access controls.

ansible.posix.acl

Manage Access Control Lists (ACLs) for fine-grained file permissions.

ansible.builtin.firewalld or ansible.posix.firewall
Configure firewalls to restrict network access.

**Integrity (Ensuring data is accurate and unaltered)**

ansible.builtin.lineinfile / replace / blockinfile

Ensure critical config files have the correct content and no unauthorized changes.

ansible.builtin.command / shell (with checksum tools)

Run integrity check tools like sha256sum, aide, or tripwire (custom scripts).

ansible.builtin.stat

Check file checksums, permissions, timestamps.

ansible.builtin.assert

Validate conditions (e.g., file hashes or content checks) during playbook run.

ansible.builtin.yum / apt

Keep software packages (including security patches) up to date to maintain system integrity.

**Availability (Ensuring services are up and running)**

ansible.builtin.service / ansible.builtin.systemd

Manage critical services to ensure they are started and enabled.

ansible.builtin.reboot

Reboot systems when kernel or critical patches are applied.

ansible.builtin.shell / command

Run custom health checks or scripts to verify system availability.

ansible.builtin.wait_for

Wait for services or ports to be available before continuing tasks.

ansible.builtin.fail / ansible.builtin.debug

Detect failures and notify accordingly.

**Scenario**

- name: Disable root SSH login
- name: Ensure ufw is installed and configured | Uncomplicated Firewall. It simplifies firewall management for users who
  
  may not be comfortable writing complex iptables rules directly, making basic firewall configuration accessible and quick.

- name:  Ensure critical services are running (availability)

```yaml
---
- name: Ensure critical services are running and enabled
  hosts: all
  become: yes

  vars:
    critical_services:
      - sshd
      - firewalld
      - cron

  tasks:
    - name: Ensure critical services are running and enabled
      ansible.builtin.service:
        name: "{{ item }}"
        state: started
        enabled: yes
      loop: "{{ critical_services }}"
```





  
