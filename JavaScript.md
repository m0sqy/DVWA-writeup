# JavaScript

Objective

Simply submit the phrase "success" to win the level. Obviously, it isn't quite
that easy, each level implements different protection mechanisms, the JavaScript
included in the pages has to be analysed and then manipulated to bypass the
protections.

## low

Submit the phrase "success" and we get a prompt: "invalid token".  
From webpage source we can see a hidden input param called "token", which is set
to the hex digest of `md5(rot_13(phrase))`.  
The script only gets executed once on webpage load, therefore, our token is
initialized by the default phrase "ChangeMe".

There're two ways to do the trick: We either modify the token in browser's
console by changing the phrase to "success" and re-run `generate_token()`, or
pre-compute MD5 hex digest with python, intercept the POST request and
substitute the token.

```py
import codecs
import hashlib
print(hashlib.md5(codecs.encode("success").encode()).hexdigest())
# 38581812b435834ebf84ebcc2c6424d6
```

Server echoes "Well done!", which indicates that we've solved this challenge.

## medium

Our script is placed at
`/vulnerabilites/javascript/source/medium.js`.  
Token initialization is delayed by `setTimeout()` function.

The 'password' token is easy to find out: `"XX"+"success"[::-1]+"XX"` =
`"XXsseccusXX"`.  
Run `document.getElementById("token").value="XXsseccusXX";` in the console,
modify the phrase and submit to see the "Well done!" prompt.

## high

In this level our script is obfuscated.  

We can deobfuscate it using
[Deobfuscate Javascript](http://deobfuscatejavascript.com).  
There's also some imported code which I guess is an implementation of sha256.  
```js
function do_something(e) {
    for (var t = "", n = e.length - 1; n >= 0; n--) t += e[n];
    return t
}
function token_part_3(t, y = "ZZ") {
    document.getElementById("token").value = sha256(document.getElementById("token").value + y)
}
function token_part_2(e = "YY") {
    document.getElementById("token").value = sha256(e + document.getElementById("token").value)
}
function token_part_1(a, b) {
    document.getElementById("token").value = do_something(document.getElementById("phrase").value)
}
document.getElementById("phrase").value = "";
setTimeout(function() {
    token_part_2("XX")
}, 300);
document.getElementById("send").addEventListener("click", token_part_3);
token_part_1("ABCD", 44);
```

At the time we submit our phrase, our token should have the value
`sha256("XXsseccus")`. So the server will get `sha256(token + "ZZ")`.  
Just as the low security level, we can imitate client's behavior in console 
and click "submit", or craft our own POST request with python.  

Either way we should pre-compute `sha256("XXsseccus")`, but if you want to
do it with your own script, remember there's another step to compute
`sha256(token + "ZZ")`.

```js
/* token after part 2
 * 7f1bfaaf829f785ba5801d5bf68c1ecaf95ce04545462c8b8f311dfc9014068a
 */
document.getElementById("token").value = sha256("XXsseccus");
/* token after part 3
 * Don't do it if you submit phrase with the button.
 * ec7ef8687050b6fe803867ea696734c67b541dfafb286a0b1239f42ac5b0aa84
 */
document.getElementById("token").value = sha256("XXsseccus"+"ZZ");
```
