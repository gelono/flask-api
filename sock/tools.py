def check_token(token):
    with open('../storage/tokens.txt', 'r') as file:
        tokens = file.read().splitlines()
        return token in tokens


def check_ip(ip):
    with open('../storage/ips.txt', 'r') as file:
        ips = file.read().splitlines()
        return ip in ips
