import winrm

def winrm_check(check):
    try:
        session = winrm.Session(check['host'], auth=(check['username'], check['password']))
        result = session.run_cmd(check['command'])
    except Exception as e:
        return e
    return 0