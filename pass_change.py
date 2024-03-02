import os, sys, json

# returns list of tuples containing relative filename and check contents
def get_checks_and_files(directory):
    checks = []
    names = []
    for filename in os.listdir(directory):
        if '.json' in filename:
            with open(directory + filename, 'r') as f:
                new_check = json.loads(f.read())
                if ('display_name' in new_check) and ('service' in new_check) and ('host' in new_check):
                    checks.append(new_check)
                    names.append(directory + filename)
                f.close()
    return checks, names

def check_valid(check):
    required_keys = ['display_name', 'username', 'password']
    for key in required_keys:
        if key not in check:
            return False
    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage is:\n\t' + sys.argv[0] + ' check_directory/ input.csv')
        exit()

    input = sys.argv[2]
    path = sys.argv[1]
    if path[-1] != '/':
        path += '/'
    
    checks, names = get_checks_and_files(path)

    for line in open(input, 'r').readlines():
        values = line.replace(' ', '').replace('\n', '').split(',')
        display_name = values[0]
        username = values[1]
        password = values[2]
        for check in checks:
            if not check_valid(check):
                continue
            condition_1 = (display_name.lower() in check['display_name'].lower())
            condition_2 = (username.lower() in check['username'].lower())
            if condition_1 and condition_2:
                print(f'changed user {check['username']} on {check['display_name']}')
                filename = names[checks.index(check)]
                check['password'] = password
                with open(filename, 'w') as f:
                    data = json.dumps(check, indent=2)
                    f.write(data)
                    f.close()
