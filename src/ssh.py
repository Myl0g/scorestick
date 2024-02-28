import paramiko

def check(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
    except Exception as e:
        return e
    return 0

if __name__ == '__main__':
    host = '192.168.151.98'
    username = 'ccdc'
    password = 'Password123!@#'
    command = 'whoami & dir'
    result = check(host, username, password, command)
    print(f'ssh: {result}')