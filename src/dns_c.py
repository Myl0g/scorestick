import dns.resolver

def dns_check(check):
    try:
        r = dns.resolver.Resolver(configure=False)
        r.nameservers = [check['host']]
        result = r.resolve(check['name'], 'A')
        for ip in result:
            if check['ip'] in ip.to_text():
                return 0
            else:
                return 'wrong ip'
                
    except Exception as e:
        return e

if __name__ == '__main__':
    check = {
        "display_name": "dns :]",
        "service": "dns",
        "host": "192.168.151.98",
        "name": "db01.galacticspace.local",
        "ip": "192.168.151.1"
    }
    print(f'dns: {dns_check(check)}')