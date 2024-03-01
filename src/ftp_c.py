# incomplete
from ftplib import FTP, FTP_TLS
import ssl

def check_valid(check):
    required_keys = ['display_name', 'service', 'host', 'username', 'password', 'file', 'md5']
    for key in required_keys:
        if key not in check or check[key] == '':
            return False
    return True

def ftp_check(check):
    return 'check error'
    if not check_valid(check):
        return 'check error'
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")
        ftp = FTP_TLS()
        ftp.ssl_version = ssl.PROTOCOL_SSLv23
        ftp.debugging = 2
        ftp.connect(check['host'], 21)
        ftp.login(check['username'], check['password'])
        return ftp.getwelcome()
    except Exception as e:
        return e

if __name__ == '__main__':
    check = {
        "display_name": "selfharm-ftp",
        "service": "ftp",
        "host": "192.168.151.98",
        "username": "ccdc",
        "password": "Password123!@#",
        "file": "catboy.png",
        "md5": "a"
    }
    print(f'ftp: {ftp_check(check)}')