import paramiko

def ssh_check(check):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(check['host'], username=check['username'], password=check['password'])
        stdin, stdout, stderr = ssh.exec_command(check['command'])
    except Exception as e:
        return e
    return 0