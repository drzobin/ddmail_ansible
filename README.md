# What is ddmail_ansible
Ansible for ddmail project. 

## What is ddmail
DDMail is a e-mail system/service and e-mail provider with strong focus on security, privacy and anonymity. A current production example can be found at www.ddmail.se

## Operating system
Developt for and tested on debian 12.

## Installation and setup for dev
export EDITOR=[your editor of choise]<br>

[your editor of choise] environments/dev/hosts<br>
[edit file to match your dev env]<br>
cp dev_vault_template environments/dev/group_vars/all/vault<br>
ansible-vault encrypt environments/dev/group_vars/all/vault<br>
ansible-vault edit environments/dev/group_vars/all/vault<br>
[edit vault file to match your dev env]<br>
<br>
ansible-playbook dev_playbook.yml -i environments/dev/ --ask-vault-pass --key-file [key file]

## Installation and setup for prod
export EDITOR=[your editor of choise]<br>

[your editor of choise] environments/prod/hosts<br>
[edit file to match your prod env]<br>
cp prod_vault_template environments/prod/group_vars/all/vault<br>
ansible-vault encrypt environments/prod/group_vars/all/vault<br>
ansible-vault edit environments/prod/group_vars/all/vault<br>
[edit vault file to match your prod env]<br>
<br>
ansible-playbook prod_playbook_primary_srv.yml -i environments/prod/ --ask-vault-pass --key-file [key file]
<br>
ansible-playbook prod_playbook_secondary_srv.yml -i environments/prod/ --ask-vault-pass --key-file [key file]


