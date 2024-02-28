import winrm

def check(host, username, password, command):
    try:
        session = winrm.Session(host, auth=(username, password))
        result = session.run_cmd(command)
    except Exception as e:
        return e
    return 0

if __name__ == '__main__':
    host = '192.168.151.98'
    username = 'ccdc'
    password = 'Password123!@#'
    command = 'whoami & dir'
    result = check(host, username, password, command)
    print(f'winrm: {result}')