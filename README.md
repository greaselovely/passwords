# Password Lemur

Passphrase generator with min and max number of words to generate, dynamically download, sanitize and unique values in the dictionary list.

# Password Marmot

Rehash of Password Rabbit, using secrets.token_urlsafe as a generator, take random characters from that, replace random characters with random number and random special character, reverse it, shuffle it, and check it for complexity.  Overall my goal was to have a very random high entropy script.  I added some functionality via arguments and incorporated type hints.

# Password Rabbit

Took that idea to create a local password generator, which is not a new, unique or clever idea, but worked it to either be called via arguments or via dialog.  It does self checks to make sure password complexity is adhered to, enforcing upper, lower, numbers and special characters.  The option of excluding special characters is provided.

Password Rabbit is named after the following scripts previously written and renamed recently.


<hr><hr>

# Password Wolf

Retrieves passwords from  <a href="https://passwordwolf.com" target="_blank">PasswordWolf</a>, shows you all the passwords generated, and allows you to select one.  Once you select the password, it copies it to your clipboard.

# Variables

Change them as needed.  For instance turn everything off except special characters and see the 'hilarious' passwords it generates.

<hr><hr>

# password_wolf.sh

Bash v4 supported shell script to generate passwords and copy to the clipboard.  Use of this script is when you are on a Linux workstation in a local terminal session, NOT a SSH session to a remote system.  xclip is used and only interacts with the local UI.

# Tested on:

Ubuntu, MacOS

<hr><hr>

# password_wolf.py

Python v3 supported script to generate passwords and copy to the clipboard.

# Tested on

Windows, MacOS, Ubuntu

<hr><hr>

# password_wolf.ps1

PowerShell supported script to generate passwords and copy to the clipboard.

# Tested on

Windows, MacOS, Ubuntu
