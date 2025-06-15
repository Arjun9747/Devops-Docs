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

**Fail**

The fail module is used to fail a playbook when a certain condition is met. It can be used to stop the playbook execution when an error occurs or when a specific condition is not met.
```yaml
- name: Fail if the variable is not defined
  fail:
    msg: "The variable 'my_var' is not defined"
  when: my_var is not defined
```

**assert**

The assert module is used to verify that a certain condition is met. If the condition is not met, the playbook will fail.

```yaml
- name: Ensure /etc/passwd is not world-writable
  assert:
    that: stat_passwd.mode != '0666'
    fail_msg: "/etc/passwd should not be world-writable"
```

Use assert for checks and validations, and fail for hard stops with conditions, often combined with when

Ansible 
```markdonw
Facts are used to collect information about target systems. 
They are global 
1.Sys Infor --> Os, CPU
2. N/w ip addr
3.HW information
4. Package infor 

Registers
Variables that stores output of a task , specific to task 
1. Command Output
2.API response
3.Script Output

Notify tells handlers to trigger a task 
Handlers are specific task that are run only when notified 

SARIF --> Static Analysis Result Interchange Format 

PAM --> Pluggable Authentication Modules 
Use by System Admins to configure how authentication are handled for users and applications 

Ansible Roles --> Standarized way to organize Ansible Code 
locally in your playbook projects, 

Ansible galaxy --> Repository for sharing and downloading roles or collections.
On the internet 

Molecule is a testing framework for ansible role. It helps you to develope, test and lint ansible role in a repeated and automated way.
Create Docker container
Apply the ansible role 
Verify test the results
tear down the instance 


Jinja template 
Jinja templates in Ansible let us write dynamic, customizable configuration files using variables, loops, and conditions.
 This makes roles and playbooks much more flexible and reusable across different environments and hosts
```
 
 | Folder/File           | Purpose                                                                            |
| --------------------- | ---------------------------------------------------------------------------------- |
| `defaults/`           | Contains default variables (`main.yml`) that are the lowest precedence.            |
| `vars/`               | Contains higher-precedence variables used specifically for this role.              |
| `tasks/`              | Main task definitions go here (`main.yml`) — this is where the role’s logic lives. |
| `handlers/`           | Contains handlers triggered by `notify`, typically used for restarting services.   |
| `meta/`               | Includes role metadata (`main.yml`) like dependencies on other roles.              |
| `templates/`          | Jinja2 templates used to render config files dynamically (e.g., `nginx.conf.j2`).  |
| `README.md`           | Documentation about what the role does, variables to use, etc.                     |
| `CHANGELOG.md`        | Tracks changes to the role across versions.                                        |
| *(optional)* `files/` | If present, contains static files to be copied as-is.                              |

```markdown
This playbook applies OS-specific PAM hardening practices. It dynamically adjusts based on the OS type using ansible_facts.os_family.
 It disables password caching via pam_ccreds, ensures password hash algorithms are secure with SHA-512 (NSA recommendation),
 and applies specific templates and settings depending on the distribution. It uses Ansible constructs like package_facts,
 lineinfile, template, and import_tasks to maintain clean, modular, and secure configurations."
 
 
 This Ansible role configures hardened PAM settings for RedHat systems using templated files.
 It installs sssd-client if LDAP/SSSD is enabled, then deploys a central configuration file
 (rhel_auth.j2) to both system-auth-local and password-auth-local. These are then symlinked
 to the main system files, allowing centralized control over password complexity (passwdqc)
 and lockout policies (faillock). Using symlinks ensures the system uses our secure version without editing default-managed files directly.
```
 
 
 
 
 | Benefit                       | Description                                                                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------------ |
| 🔒 **Security Hardening**     | Ensures no extra UID=0 users, locks system account passwords, and limits home folder access      |
| 📜 **Compliance**             | Meets CIS, NIST, and NSA recommendations for password aging, shell locking, and user segregation |
| 🔄 **Automation**             | Dynamically handles any number of users across systems without hardcoding                        |
| 📦 **Idempotent & Auditable** | Safe to run repeatedly and can be integrated into CI pipelines or GitOps flows                   |


```markdown
"This playbook secures all cron directories and files by setting root ownership and removing group and other permissions.
 This follows CIS benchmarks and protects against unauthorized access or tampering with scheduled jobs, which could otherwise
 lead to privilege escalation or audit bypass."
 
  This file removes and purges deprecated or insecure packages from the system,
 but only if you’ve enabled this cleanup via the os_security_packages_clean variable.
 The specific packages to remove are defined in the os_security_packages_list variable.
 
 A core dump (or core file) is a snapshot of a program’s memory at the moment it crashes. It's mainly used for debugging.
 This file is designed to control whether core dumps are allowed on the system, which is an important aspect of security hardening.
 Disabling core dumps can prevent accidental leakage of sensitive information in crash dumps.
 
 The /etc/login.defs file in Linux is a configuration file used by user account management tools like useradd, usermod, passwd, and login.
 PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_WARN_AGE   14

UID_MIN         1000
UID_MAX         60000

CREATE_HOME     yes
ENCRYPT_METHOD  SHA512

LOGIN_RETRIES   5
LOGIN_TIMEOUT   60

In summary, this task ensures a hardened, consistent login.defs file is deployed as part of the system hardening process.
```
```yaml
dev-sec.os-hardening 
ansible-galaxy install dev-sec.os-hardening

ansible.builtin.users/files/lineinfile/service/template 

- name: Lock system accounts
  user:
    name: "{{ item }}"
    password: "!"
  loop: "{{ system_users }}"

lock their password settings to ! 

---
name:nginx install 
host" webServers
become: true 
gather-facts: true 

vars: 
	nginx-pakage_name: nginx 

tasks:
	- name: check if nginx is already installed 
	ansible.builtin.package_facts:
		manager: auto 
		
	- name: results 
	ansible.builtin.debug:
		msg: "NGXIN is not installed"
	when: nginx package not installed
	register: nginix_not_installed 
	
	- name: Install nginx
	  ansible.builtin.package:
		name: "{{nginx.package_name}}"
		state: present
		notify: start nginx
		
	- name: nginx 
	ansible.builtin.debug:
	name: "nginx not installed"
	
	-name: start NGINX
	ansible.builtin.service
	name: nginx
	state: started
	enabled: true
```
	
 



