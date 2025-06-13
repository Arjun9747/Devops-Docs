```yaml
- name: Update SSH configuration to be more secure.
  lineinfile:
    dest: /etc/ssh/sshd_config
    regexp: "{{ item.regexp }}"
    line: "{{ item.line }}"
    state: present
    validate: 'sshd -t -f %s'
  with_items:
    - { regexp: "^PasswordAuthentication", line: "PasswordAuthentication no" }
    - { regexp: "^PermitRootLogin", line: "PermitRootLogin no" }
    - { regexp: "^Port", line: "Port 2849" }
  notify: restart ssh
```
Uses the lineinfile module to ensure specific lines exist in the file:

Disables password authentication

Disables root login

Changes the SSH port to 2849

```yaml
- name: Allow sshd to listen on tcp port 2849.
  seport:
    ports: 2849
    proto: tcp
    setype: ssh_port_t
    state: present
  when: ansible_selinux.status == 'enabled'
```
By explicitly managing SELinux policy and defining that sshd can listen on a non-default port (2849), you prevent unauthorized or unintended processes from using that port.

Helps maintain controlled, predictable configuration — a key part of maintaining system integrity.


```yaml
- name: Add sudo rights for deployment user.
  lineinfile:
    dest: /etc/sudoers
    regexp: '^johndoe'
    line: 'johndoe ALL=(ALL) NOPASSWD: ALL'
    state: present
    validate: 'visudo -cf %s'
```
To grant johndoe passwordless sudo access by inserting a line in /etc/sudoers.

Modifying /etc/sudoers manually can break sudo access if there's a syntax error. Using validate: 'visudo -cf %s' ensures that:

Ansible validates the syntax before applying the change.

If the syntax is invalid, the playbook will fail safely without making the change.

Remove unused software, open only required ports

- name: Remove unused packages.
package:
name:
- nano
- sendmail
state: absent
purge: yes

**UFW**
ufw stands for Uncomplicated Firewall. It is a frontend for iptables designed to simplify the process of configuring a firewall on Linux systems, especially Ubuntu.

🔐 What Does ufw Do?
ufw helps you easily:

Allow or deny incoming/outgoing connections on specific ports or IPs

Set up rules for services like SSH, HTTP, HTTPS

Enable or disable the firewall

Log firewall activity

```yaml
- name: Configure open ports with ufw.
ufw:
rule: "{{ item.rule }}"
port: "{{ item.port }}"
proto: "{{ item.proto }}"
with_items:
- { rule: 'allow', port: 22, proto: 'tcp' }
- { rule: 'allow', port: 80, proto: 'tcp' }
- { rule: 'allow', port: 123, proto: 'udp' }
- name: Configure default incoming/outgoing rules with ufw.
ufw:
direction: "{{ item.direction }}"
policy: "{{ item.policy }}"
state: enabled
with_items:
- { direction: outgoing, policy: allow }
- { direction: incoming, policy: deny }
```

```yaml
- name: Configure open ports with firewalld.
firewalld:
state: "{{ item.state }}"
port: "{{ item.port }}"
zone: external
immediate: yes
permanent: yes
with_items:
- { state: 'enabled', port: '22/tcp' }
- { state: 'enabled', port: '80/tcp' }
- { state: 'enabled', port: '123/udp' }
```

fail2ban is a security tool that:

Monitors log files for suspicious activity (e.g., failed SSH logins)

Temporarily bans IP addresses showing signs of malicious behavior

```yaml
- name: Install fail2ban (RedHat).
dnf:
name: fail2ban
state: present
enablerepo: epel
when: ansible_os_family == 'RedHat'
- name: Install fail2ban (Debian).
apt:
name: fail2ban
state: present
when: ansible_os_family == 'Debian'
- name: Ensure fail2ban is running and enabled on boot.
service:
name: fail2ban
state: started
enabled: yes
```

**EC2- Plugin**

The Ansible EC2 plugin is a dynamic inventory plugin that:

Queries AWS EC2 using AWS APIs

Automatically gathers information about EC2 instances

Organizes hosts into groups based on tags, regions, instance states, etc

```yaml
plugin: amazon.aws.aws_ec2
regions:
  - ap-south-1  # Replace with your region
filters:
  instance-state-name: running
keyed_groups:
  - prefix: tag
    key: tags.Role  # Group hosts by EC2 tag "Role"
hostnames:
  - private-ip-address
```



