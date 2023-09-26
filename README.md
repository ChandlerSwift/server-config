# Server configuration scripts

```sh
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
ansible-playbook -kKc paramiko zirconium.yml
# subsequent runs omit `-kKc paramiko`, since we've configured public key auth and disabled sudo password
```

### User per service
https://blog.wesleyac.com/posts/how-i-run-my-servers

### Editing secrets in ansible-vault
```sh
EDITOR="code --wait" ansible-vault edit group_vars/all.yml
```
