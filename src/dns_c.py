import dns
from dns import resolver

def dns_check(check):
    try:
        r = resolver.Resolver(configure=False)
        r.nameservers = [check['host']]
        return r.resolve(check['name'], 'A')
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