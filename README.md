# ddmail_ansible
Ansible for ddmail, ddmail is a e-mail system/service for reasonable paranoid people who value privacy and security.

# Operating system
Developt for and tested on debian 12.

# Installation and setup for dev and prod
export EDITOR=[your editor of choise]<br>

[your editor of choise] environments/dev/hosts<br>
[edit file to match your dev env]<br>
cp dev_vault_template environments/dev/group_vars/all/vault<br>
ansible-vault encrypt environments/dev/group_vars/all/vault<br>
ansible-vault edit environments/dev/group_vars/all/vault<br>
[edit vault file to match your dev env]<br>

[your editor of choise] environments/prod/hosts<br>
[edit file to match your prod env]<br>
cp prod_vault_template environments/prod/group_vars/all/vault<br>
ansible-vault encrypt environments/prod/group_vars/all/vault<br>
ansible-vault edit environments/prod/group_vars/all/vault<br>
[edit vault file to match your prod env]<br>

# Run ansible for prod
ansible-playbook prod_playbook.yml -i environments/prod/ --ask-vault-pass --key-file [key file]

# Run ansible for dev
ansible-playbook dev_playbook.yml -i environments/dev/ --ask-vault-pass --key-file [key file]

