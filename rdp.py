# requires xvfb and freerdp-x11
import subprocess

def xvfb():
    subprocess.Popen('sudo Xvfb :50 -screen 0 1024x768x16', shell=True)

def rdp_check(host, username, password):
    command = "export DISPLAY=:50; xfreerdp +auth-only /cert:ignore /v:'"+host+"' /u:'"+username+"' /p:'"+password+"'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = process.stderr.readlines()
    # out = process.stdout.readlines()
    for line in err:
        if 'status 0' in str(err):
            return 0
        elif 'status 1' in str(err):
            return str(err)

if __name__ == '__main__':
    # threading.Thread(target=rdp_display).start
    ip = '192.168.151.98'
    username = 'ccdc'
    password = 'Password123!@#'
    result = rdp_check(ip, username, password)
    print(f'rdp: {result}')