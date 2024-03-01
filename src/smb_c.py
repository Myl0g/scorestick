import hashlib
import smbclient

def check_valid(check):
    required_keys = ['display_name', 'service', 'host', 'username', 'password', 'file', 'md5']
    for key in required_keys:
        if key not in check or check[key] == '':
            return False
    return True

def smb_check(check):
    if not check_valid(check):
        return 'check error'
    try:
        url = '\\\\' + check['host'] + '\\' + check['file']
        smbclient.register_session(check['host'], username=check['username'], password=check['password'])
        with smbclient.open_file(url, mode='rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
            if md5 == check['md5']:
                return 0
            else:
                return 'failed content check'
    except Exception as e:
        return e

if __name__ == '__main__':
    check = { 
        "display_name": "selfharm-smb",
        "service": "smb",
        "host": "192.168.151.98",
        "username": "ccdc",
        "password": "Password123!@#",
        "file": "share\\catboy.png",
        "md5": "66C2DCA3C6EE7760DCB98A3F31259D22"
    }
    print(f'smb: {smb_check(check)}')