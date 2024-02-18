# Password Genut

Passphrase generator with min and max number of words to generate using Password Wolf's password phonetic that is provided via API

Example Output:
```
        1.      nine xray QUEBEC four BRAVO INDIA at six
        2.      charlie dot five five golf pappa comma XRAY
        3.      five seven question-mark yankee GOLF BRAVO tango left-paren

        Choose a passphrase to copy: 

        Passphrase #2 Copied.
```

# Password Lemur

Passphrase generator with min and max number of words to generate, dynamically download, sanitize and unique values in the dictionary list.

Example Output:
```
        1.      partying glimpsed fireproof urinal
        2.      bambino detergent golfer inadequacy
        3.      mediocrity revival improvised quintessential

        Choose a passphrase to copy: 

        Password #2 Copied.
```

# Password Marmot

Rehash of Password Rabbit, using secrets.token_urlsafe as a generator, take random characters from that, replace random characters with random number and random special character, reverse it, shuffle it, and check it for complexity.  Overall my goal was to have a very random high entropy script.  I added some functionality via arguments and incorporated type hints.

Example Output:
```
        1.      G1uCJcCbux65?bC5uk19
        2.      RccV5)kbEnubhREkx)kd
        3.      Cbn3SHvtVMcdhVE0^16t

        Choose a password to copy: 

        Password #3 Copied.
```

# Password Rabbit

Took that idea to create a local password generator, which is not a new, unique or clever idea, but worked it to either be called via arguments or via dialog.  It does self checks to make sure password complexity is adhered to, enforcing upper, lower, numbers and special characters.  The option of excluding special characters is provided.

Password Rabbit is named after the following scripts previously written and renamed recently.

Example Output:
```

        1.      S9(Ghfy#Q@xin)4m&00H
        2.      9A*cWTJrkC6$@VS#^5eL
        3.      ^l@GJE)7(cfBD&8t0adH

        Choose a password to copy: 

        Password #3 Copied.
```


<hr><hr>

# Password Wolf

Retrieves passwords from  <a href="https://passwordwolf.com" target="_blank">PasswordWolf</a>, shows you all the passwords generated, and allows you to select one.  Once you select the password, it copies it to your clipboard.

### Variables

Change them as needed.  For instance turn everything off except special characters and see the 'hilarious' passwords it generates.

<hr><hr>

### password_wolf.sh

Bash v4 supported shell script to generate passwords and copy to the clipboard.  Use of this script is when you are on a Linux workstation in a local terminal session, NOT a SSH session to a remote system.  xclip is used and only interacts with the local UI.

### Tested on:

Ubuntu, MacOS

<hr><hr>

### password_wolf.py

Python v3 supported script to generate passwords and copy to the clipboard.

### Tested on

Windows, MacOS, Ubuntu

<hr><hr>

### password_wolf.ps1

PowerShell supported script to generate passwords and copy to the clipboard.

### Tested on

Windows, MacOS, Ubuntu

Example Output:
```
        1. yUQPc-9Km3aX%eMD
        2. mM8pCC3-C*kJ-vv1
        3. #&QnazD0BNTuw*6n


        Select Password to Copy: 
        Password #1 Copied

```
