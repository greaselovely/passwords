import random, os, re
import argparse
import sys
import secrets
import pathlib

#####
#
min_length = 12
max_length = 31
def_length = 25
min_qty = 0
max_qty = 20
file_name = "passwords.txt"
#
#####

"""
usage: password_marmot.py [-h] -q QTY [-l LENGTH] [-s] [-c] [-f] [-o]

Generate passwords when passed a quantity and length. Writing to file will override
other options (ie...copy) unless qty = 1

options:
  -h, --help            show this help message and exit
  -q QTY, --qty QTY     Number of password to generate as integer
  -l LENGTH, --length LENGTH
                        Length of password as integer
  -s, --no_special         Exclude special characters
  -c, --copy            Copy password to clipboard
  -f, --file            Write passwords to file
  -o, --obfuscate       Obfuscates password output to stdout

"""

passwords = {}
special = "!@#$%^&*()?"
numbers = "0123456789"

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def argue_with_me() -> tuple:
    """
    This is called if there are arguments passed to the script via cli,
    and assigns and returns the variables qty (int), length (int),
    spec_char (True / False) and copy (True / False) to the script.
    """
    parser = argparse.ArgumentParser(description='Generate passwords when passed a quantity and length.  Writing to file will override other options (ie...copy) unless qty = 1')
    parser.add_argument('-q', '--qty', type=int, help='Number of password to generate as integer', required=True)
    parser.add_argument('-l', '--length', type=int, help='Length of password as integer', required=False)
    parser.add_argument('-s', '--no_special', action='store_true', help='Exclude special characters', required=False)
    parser.add_argument('-c', '--copy', action='store_true', help='Copy password to clipboard', required=False)
    parser.add_argument('-f', '--file', action='store_true', help='Write passwords to file', required=False)
    parser.add_argument('-o', '--obfuscate', action='store_true', help='Obfuscates password output to stdout', required=False)
    args = parser.parse_args()
    qty = args.qty
    length = args.length if args.length else def_length
    spec_char = args.no_special
    copy = args.copy
    file = args.file
    obfuscate = args.obfuscate
    return qty, length, spec_char, copy, file, obfuscate

def gen_password(length: int, spec_char: bool, file: bool, qty=1) -> None:
    """
    Generate passwords accepting the length and qty.
    This is using secrets.token_urlsafe to generate a 
    random base64 string, and we take that long string
    clean up based on my preference, and then use random.choices 
    to choose n number of characters from that string for length.
    Then we replace random characters with a special character and
    a number, we reverse the password, and then send it to be shuffled.
    Each one sent to check complexity requirements
    and if return True then we add it to the dict and print
    stdout, if return False then it loops again.
    Dictionary looks like:
    { 1: "password", 2: "Password", 3: "P@55w0rd" }
    """
    global special
    if spec_char:   # boolean
        special = numbers   # instead of using null
    i = 1
    pwd = secrets.token_urlsafe(54) # 72 characters long, a random URL-safe base64 text string
    pwd = pwd.replace('-', '').replace('_', '') # cleanup, I don't want them
    while len(passwords) < qty: # build a dict of passwords
        new_pwd = ''.join(random.choices(pwd, k=length))    # grab n number of characters from pwd
        s,n = random_char_index(new_pwd)    # generate random numbers based on length of pwd
        new_pwd = replace_chars(new_pwd, s, n)  # insert numbers and characters into pwd
        new_pwd = reverse_chars(new_pwd)     # reverse it
        new_pwd = shuffle_pwd(new_pwd)  # shuffle it
        chk = check_password(new_pwd, spec_char)  # Check it to see if it meets complexity
        if not chk: continue    # don't add it to the dict
        passwords[i] = new_pwd  # add it to the dict
        i += 1  # increment the count which is used as key in dict
    if file: write_file(passwords)

def reverse_chars(pwd: str) -> str:
    return pwd[::-1]

def replace_chars(pwd: str, s: int, n: int) -> str:
        """
        Replaces at random locations with a random 
        number and special character
        """
        spec = random.choice(special)
        numb = random.choice(numbers)
        new_pwd = pwd.replace(pwd[s], spec).replace(pwd[n], numb)
        return new_pwd

def shuffle_pwd(pwd: str) -> str:
    pwd_list = list(pwd)
    random.shuffle(pwd_list)
    return ''.join(pwd_list)

def random_char_index(pwd: str) -> tuple:
    """
    Generate random int's minus 1 based on the len of pwd 
    and return the ints. Used to pick a random index in the
    string to replace with a number (n) and a special (s) character
    """
    s = random.randint(0, len(pwd) - 1)
    n = random.randint(0, len(pwd) - 1)
    random_char_index(pwd) if s == n else None
    return s,n

def check_password(pwd: str, spec_char: bool) -> bool:
    """
    Complexity checking.  Each password is checked that at least one of each type of character:
    special, upper, lower, and a number.  If not, we return False and the password
    is effectively rejected.
    """
    if spec_char:
        s = re.compile("")
    else:
        s = re.compile("[\~\!\@\#\$\%\^\&\*\(\)\_\+\-\=\{\}\|\[\]\\\:\;\'\<\>\?\,\.\/\*]") # special
    l = re.compile("[a-z]") # lower
    u = re.compile("[A-Z]") # upper
    n = re.compile("[0-9]") # numbers
    return True if re.findall(s, pwd) and re.findall(l, pwd) and re.findall(u, pwd) and re.findall(n, pwd) else False

def dialog_qty() -> tuple:
    """
    Entry point for all dialogs and returns all results
    Creates a dialog to respond to for the number of passwords to generate.  This function
    then calls the dialog_length function for how long each password should be, and then returns both
    values so that it can be sent for password(s) generation.  If invalid characters are entered, then we
    just make some decisions based on variables above.  Right now we are giving up if they enter more than
    the max_qty variable because it's not important to fight that level of dumb.
    """
    qty = input(f"\n\tNumber of passwords to generate (1-[{max_qty}]): ")
    try:
        qty = int(qty)
    except ValueError:
        qty = max_qty

    if qty >= max_qty + 1:
        print("\n\tToo many, try again\n")
        sys.exit()
    length = dialog_length(qty)
    spec_char = dialog_special(qty)
    return qty, length, spec_char

def dialog_length(qty: int) -> int:
    """
    Creates a dialog to respond to for the length of passwords to generate.  This function
    is called from dialog_qty function, and then returns the length.
    If invalid characters are entered, then we just make some decisions based on variables above.
    Right now we are giving up if they enter more than the max_length variable because
    it's not important to fight that level of dumb.
    """
    length = input(f"\n\tEnter the length of password (min:{min_length}, max:{max_length}) [{def_length}]: ")
    try:
        length = int(length)
        if length < min_length or length > max_length:
            print(f"\n\tSpecified length {length} does not meet requirements\n\n\tLength has to be between {min_length} and {max_length}\n\n")
            sys.exit()
    except ValueError:
        length = def_length
    return length

def dialog_special(qty: int) -> bool:
    """
    Creates a dialog to ask if special characters are wanted or not.
    Use case: sometimes dumb people make apps that they can't / won't
    allow special characters.
    """
    s = input("\n\tInclude special characters? ([y]/n): ")
    print("\n\n\tYour Passwords:\n\n") if qty > 1 else None
    return False if s.lower() != 'n' else True

def dialog_copy(copy: bool, n=1) -> None:
    """
    Creates a dialog to respond to for the password to copy to the clipboard.
    If invalid characters are entered we simple choose a random integer between
    1 and the length of the passwords dictionary and then call copy_pwd.
    """
    more = " to copy:" if copy else ":"
    if n == 1:
        p = passwords.get(n)
        copy_pwd(p, n)
    else:
        p2c = input(f"\n\tChoose a password{more} ") # p2c = password to copy
        try:
            p2c = int(p2c)
        except ValueError:
            p2c = random.randint(1, len(passwords))
        p = passwords.get(p2c)
        if p == None:
            p2c = random.randint(1, len(passwords))
            p = passwords.get(p2c)
        copy_pwd(p, p2c) if copy else print(f"\n\n\tYour password is: {p}\n\n")

def copy_pwd(p: str, n: int) -> None:
    """
    we attempt to import pyperclip, if the module is not
    installed locally, we error out and print the password to manually
    copy the password.
    """
    try:
        import pyperclip
        pyperclip.copy(p)
        print(f"\n\tPassword #{n} Copied.\n")
    except ImportError as e:
        print(f"\n\tCan't copy to clipboard,n\t{str(e).lower()}")
        print(f"\n\n\tYour password is: {p}\n\n")
        sys.exit()
    except pyperclip.PyperclipException as e:
        print(f"\n\tCan't copy to clipboard,\n\t\t{str(e).lower()}")
        print(f"\n\n\tYour password is: {p}\n\n")
        sys.exit()


def write_file(passwords: dict) -> None:
    """
    If the file (-f) argument is passed, we save the passwords
    into the localpath of this script and display that path
    """
    local_path = pathlib.Path(__file__).parent
    full_path = pathlib.Path.joinpath(local_path, file_name)
    with open(full_path, 'w') as file:
        file.write('\n'.join(list(passwords.values()))+'\n')
    print(f"\n\tWritten to {full_path}\n\n")

def main():
    clear()
    """
    Arguably, this is yet another example of generating passwords but with a higher entropy
    by the method of generation, shuffling, random char replacement, and so on.  Just 
    another script that will sit unused but good for continued work.

    I've tried to optimize this one a bit more, but also really bloated it with almost
    unnecessary functions but creates a more logical view of the process.  Also continue
    to work on type hints.

    I'm still not worried too much about PEP, as I find some of the extra spaces 
    and wraps annoying so I can't currently capitulate to PEP standards.

    We start out looking at how many arguments are passed to the python script.
    > 3; then we send it to argparse to dissect the arguments and it handles any errors
    > 1; basically errors out and sends back an abbreviated help from argparse
    finally; we create dialogs to ask what the user wants and display from variables
    above.  The user can simply hit enter to accept all defaults and we'll handle it
    using try / except to choose for them.
    """
    copy = True
    file = False
    obfuscate = False

    # Check for arguments, send to function if > 1 or > 2 or -h.
    # Otherwise generates passwords
    if len(sys.argv) > 2:
        qty, length, spec_char, copy, file, obfuscate = argue_with_me()
        if length < min_length or length > max_length:
            print(f"\n\tSpecified length {length} does not meet requirements\n\n\tLength has to be between {min_length} and {max_length}\n\n")
            sys.exit()
    elif len(sys.argv) > 1: # will simply send help to the user
        argue_with_me()
    else:
        loop = True
        while loop:
            qty, length, spec_char = dialog_qty()
            if qty and length:
                loop = False


    if qty == 1:
        gen_password(length, spec_char, file, qty)
        p = passwords.get(1)
        if copy:
            copy_pwd(p, 1)
        else:
            print(p) # to capture from stdout out let's just dump the password.
    elif file:
        gen_password(length, spec_char, file, qty)
    else:
        gen_password(length, spec_char, file, qty)
        for i,p in passwords.items():
            print(f"\t{i}.\t{p if not obfuscate else '*' * len(p)}")
        dialog_copy(copy, n=qty)

if __name__ == "__main__":
    main()
