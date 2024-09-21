# What is ddmail_ansible
Ansible for the DDMail project. 

## What is ddmail
DDMail is a e-mail system/service and e-mail provider with strong focus on security, privacy and anonymity. A current production example can be found at www.ddmail.se

## Operating system
Developt for and tested on debian 12.

## Installation and setup for dev
The development environment is designed to be run locally on your computer on two separate vms. Those two vms needs to have access to each other and the host over a host only network. Those vms also needs to be able to reach internet over ipv4, recommended is to add a secondary network card with NAT. The development servers should not be reached from internet. The two vms will have there own seperate ddmail systems, seperate local domains dev1.ddmail.internal and dev2.ddmail.internal. They will be able to send email to each other using the host only network using those domains. Both vms needs to install sshd and python3. Set up ssh key authentication for the user dev. Setup user dev to be able to use su.

### Development vm specifications
vm1<br>
dev1.ddmail.internal<br>
local user: dev<br>
host only network ip: 192.168.56.101<br>
<p>
vm2<br> 
dev2.ddmail.internal<br>
local user: dev<br>
host only network ip: 192.168.56.102<br>

### Add dev vm domainnames to hosts file
Add the following to your local /etc/hosts<br>
`192.168.56.101	dev1.ddmail.internal`<br>
`192.168.56.102	dev2.ddmail.internal`

### Setup python virtual environments
`python -m venv [ansible venv path]`<br>
`source [ansible venv path]/bin/activate`

### Get ddmail ansible code
`git clone https://github.com/drzobin/ddmail_ansible`<br>
`cd ddmail_ansible`<br>
`pip install -r install ansible`

### Set up SSH agent to avoid retyping passwords
`ssh-agent bash`<br>
`ssh-add ~/.ssh/[key file]`

### Run ansible to setup development vms
`export EDITOR=[your editor of choise]`<br>

`[your editor of choise] environments/dev/hosts`<br>
`[edit file to match your dev env]`<br>
`cp dev_vault_template environments/dev/group_vars/all/vault`<br>
`ansible-vault encrypt environments/dev/group_vars/all/vault`<br>
`ansible-vault edit environments/dev/group_vars/all/vault`<br>
`[edit vault file to match your dev env]`<br>
<br>
`ansible-playbook dev_playbook.yml -i environments/dev/ --ask-vault-pass --key-file [ssh key file]`

### Login to your local ddmail development system
Open your webbrowser and access http://dev1.ddmail.internal and/or http://dev2.ddmail.internal using those login details:<br>
Username: DEV<br>
Password: password<br>
Key file content: password<br>

### Setup Thunderbird
IMAP mail server<br>
Server name: dev1.ddmail.internal<br>
Port: 993<br>
Connection security: SSL/TLS<br>
Authentication method: normal password<br>
Username: dev@dev1.ddmail.internal<br>
Password: password<br>
<br>
Outgoing SMTP server<br>
Server name: dev1.ddmail.internal<br>
Port: 465<br>
Connection security: SSL/TLS<br>
Authentication method: normal password<br>
Username: dev@dev1.ddmail.internal<br>
Password: password<br>
<br> 
<br>
Do the same thing for both dev1.ddmail.internal and dev2.ddmail.internal. You should now be able to send email between dev@dev1.ddmail.internal and dev@dev2.ddmail.internal

## Installation and setup for prod
DDMail is designed to be run on two separate servers in different datacenters. Both servers need seperate public ipv4 addresses that is reachable from internet. The primary server runs all the services and the secondary server stores backups, handle monitoring and alerting.

`export EDITOR=[your editor of choise]`<br>

`[your editor of choise] environments/prod/hosts`<br>
`[edit file to match your prod env]`<br>
`cp prod_vault_template environments/prod/group_vars/all/vault`<br>
`ansible-vault encrypt environments/prod/group_vars/all/vault`<br>
`ansible-vault edit environments/prod/group_vars/all/vault`<br>
`[edit vault file to match your prod env]`<br>
<br>
`ansible-playbook prod_playbook_primary_srv.yml -i environments/prod/ --ask-vault-pass --key-file [ssh key file]`
<br>
`ansible-playbook prod_playbook_secondary_srv.yml -i environments/prod/ --ask-vault-pass --key-file [ssh key file]`
