import winrm

def check_valid(check):
    required_keys = ['display_name', 'service', 'host', 'username', 'password', 'command']
    for key in required_keys:
        if key not in check or check[key] == '':
            return False
    return True

def winrm_check(check):
    if not check_valid(check):
        return 'check error'
    try:
        session = winrm.Session(check['host'], auth=(check['username'], check['password']))
        result = session.run_cmd(check['command'])
    except Exception as e:
        return e
    return 0