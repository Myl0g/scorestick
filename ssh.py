import paramiko

def ssh_check(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
    except Exception as e:
        return e
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read()

if __name__ == '__main__':
    host = '192.1.151.98'
    username = 'ccdc'
    password = 'Password123!@#'
    command = 'whoami & dir'
    result = ssh_check(host, username, password, command)
    print(f'ssh: {result}')