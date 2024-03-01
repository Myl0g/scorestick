import re, requests

def check_valid(check):
    required_keys = ['display_name', 'service', 'host', 'port', 'path', 'regex']
    for key in required_keys:
        if key not in check or check[key] == '':
            return False
    return True

def http_check(check):
    if not check_valid(check):
        return 'check error'
    try:
        url = 'http://' + check['host'] + ':' + check['port'] + check['path']
        result = requests.get(url)
        if re.search(check['regex'], result.text) == None:
            return 'failed content check'
        return 0
    except Exception as e:
        return e