import paramiko

def check_valid(check):
    required_keys = ['display_name', 'service', 'host', 'username', 'password', 'command']
    for key in required_keys:
        if key not in check or check[key] == '':
            return False
    return True

def ssh_check(check):
    if not check_valid(check):
        return 'check error'
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(check['host'], username=check['username'], password=check['password'], banner_timeout=200)
        stdin, stdout, stderr = ssh.exec_command(check['command'])
        return 0
    except Exception as e:
        return e