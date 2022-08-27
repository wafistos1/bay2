from weakref import proxy
import requests

# proxy = '8.219.97.248:80'
# proxy = '159.197.250.171:3128'
# proxy = '159.197.128.76:3128'
# proxy = '133.18.194.45:8080' #  Slow Japan
# proxy = '178.128.211.134:6868' #  Slow Singapore
# proxy = '198.59.191.234:8080'
proxy = '51.223.251.124:8080'

LIST_PROXY_SKA = [
    ('78.110.2.90', '8080', 'HTTPS'),
    ('2.89.13.48', '8080', 'HTTPS'),
    ('78.93.58.60', '3128', 'HTTPS'),
    ('2.88.32.255', '8080', 'HTTPS'),
    ('94.98.217.246', '8080', 'HTTPS'),
    ('94.98.210.249', '8080', 'HTTPS'),
    ('89.144.100.11', '3128', 'HTTPS'),
    ('2.89.254.175', '8080', 'HTTPS'),
    ('176.44.211.208', '8080', 'HTTPS'),
    ('77.31.227.110', '8080', 'HTTPS'),
    ('2.88.5.97', '8080', 'HTTPS'),
    ('51.223.254.222', '8080', 'HTTPS'),
    ('213.230.18.214', '80', 'HTTPS'),
    ('51.223.250.76', '8080', 'HTTPS'),
    ('2.89.216.24', '8080', 'HTTPS'),
    ('77.31.202.17', '8080', 'HTTPS'),
    ('51.223.255.197', '8080', 'HTTPS'),
    ('77.30.111.248', '8080', 'HTTPS'),
    ('213.230.18.251', '8080', 'HTTPS'),
    ('141.164.204.37', '8080', 'HTTPS'),
    ('31.167.251.161', '8080', 'HTTPS'),
    ('94.99.61.68', '8080', 'HTTPS'),
    ('37.224.70.100', '8080', 'HTTPS'),
    ('31.166.157.18', '8080', 'HTTPS'),
    ('51.235.185.211', '8080', 'HTTPS'),
    ('88.213.78.130', '8080', 'HTTPS'),
    ('31.166.142.28', '8080', 'HTTPS'),
    ('91.147.185.2', '51459', 'HTTPS'),
    ('91.147.180.1', '43410', 'HTTPS'),
    ('37.104.140.246', '8080', 'HTTPS'),
    ('178.80.10.122', '8080', 'HTTPS'),
    ('93.189.103.78', '3128', 'HTTPS'),
    ('178.80.46.38', '8080', 'HTTPS'),
    ('31.166.33.185', '8080', 'HTTPS'),
    ('91.147.184.253', '51459', 'HTTPS'),
    ('51.218.181.179', '8080', 'HTTPS'),
    ('91.147.185.2', '57327', 'HTTPS'),
    ('213.230.18.241', '8080', 'HTTPS'),
    ('94.99.118.254', '9999', 'HTTPS'),
    ('2.91.64.110', '8080', 'HTTPS'),
    ('91.147.184.253', '35428', 'HTTPS'),
    ('94.99.125.202', '8080', 'HTTPS'),
    ('193.169.190.241', '80', 'HTTPS'),
    ('178.80.46.6', '8080', 'HTTPS'),
    ('51.39.186.24', '53281', 'HTTPS'),
    ('37.216.248.146', '8080', 'HTTPS'),
    ('37.224.85.67', '58337', 'HTTPS'),
    ('51.235.79.140', '8080', 'HTTPS'),
    ('91.147.185.2', '54318', 'HTTPS'),
    ('37.216.228.6', '53281', 'HTTPS'),
    ('193.169.190.242', '80', 'HTTPS')
 ]


for p in LIST_PROXY_SKA:
    # print(p[0] + ':' + p[1])
    try:
        r = requests.get('https://httpbin.org/ip', proxies={'http': p[0] + ':' + p[1], 'https': p[0] + ':' + p[1]}, timeout=30)
        print(r.status_code)
        print(r.json())
        print('Cool find proxy: ', p['value'])
    except requests.exceptions.ConnectTimeout as er:
        print('Failed: ', er)
    