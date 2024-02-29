import subprocess

def xvfb():
    subprocess.Popen('sudo Xvfb :50 -screen 0 1024x768x16', shell=True)

def rdp_check(check):
    command = "export DISPLAY=:50; xfreerdp +auth-only /cert:ignore /v:'"+check['host']+"' /u:'"+check['username']+"' /p:'"+check['password']+"'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = process.stderr.readlines()
    # out = process.stdout.readlines()
    for line in err:
        if 'status 0' in str(err):
            return 0
        elif 'status 1' in str(err):
            return str(err)
    return str(err)