# Running This Playbook

If you do not have it already, or do not know if you have it, install the community crypto module:

```bash
ansible-galaxy collection install community.crypto
```

Then run the playbook on your testing server with:

```bash
ansible-playbook -i "IP," -u username --private-key=path linux_testbox.yml
```

Where IP is the IP of the server, username is a user with root/sudo privileges, and the path to the private key is filled in (or the entire `--private-key` argument omitted if password authentication is used). 
