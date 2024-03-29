import random, os, re
import argparse
import sys

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
usage: password_rabbit.py [-h] -q QTY [-l LENGTH] [-s] [-c] [-f]

Generate passwords when passed a quantity and length. Writing to file will override other options (ie...copy)
unless qty = 1

options:
  -h, --help            show this help message and exit
  -q QTY, --qty QTY     Number of password to generate as integer
  -l LENGTH, --length LENGTH
                        Length of password as integer
  -s, --special         Exclude special characters
  -c, --copy            Copy password to clipboard
  -f, --file            Write passwords to file

"""

passwords = {}
alpha = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
special = "!@#$%^&*()?"
allchar = alpha + special

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def qty_and_length_args():
    """
    This is called if there are arguments passed to the script via cli,
    and assigns and returns the variables qty (int), length (int),
    spec_char (True / False) and copy (True / False) to the script.
    """
    parser = argparse.ArgumentParser(description='Generate passwords when passed a quantity and length.  Writing to file will override other options (ie...copy) unless qty = 1')
    parser.add_argument('-q', '--qty', type=int, help='Number of password to generate as integer', required=True)
    parser.add_argument('-l', '--length', type=int, help='Length of password as integer', required=False)
    parser.add_argument('-s', '--special', action='store_true', help='Exclude special characters', required=False)
    parser.add_argument('-c', '--copy', action='store_true', help='Copy password to clipboard', required=False)
    parser.add_argument('-f', '--file', action='store_true', help='Write passwords to file', required=False)
    args = parser.parse_args()
    qty = args.qty
    length = args.length if args.length else def_length
    spec_char = args.special
    copy = args.copy
    file = args.file
    return qty, length, spec_char, copy, file

def gen_password(length, spec_char, file, qty=1):
    """
    Generate passwords accepting the length and qty.
    send each one as it is generated to check complexity requirements
    and if return True then we add it to the dict and print
    stdout, if return False then it loops again.
    Dictionary looks like:
    { 1: "password", 2: "Password", 3: "P@55w0rd" }
    """
    if spec_char:
        all = alpha # don't use special char
    else:
        all = allchar
    i = 1
    while len(passwords) < qty:
        p = "".join(random.sample(all, length))
        chk = check_password(p, spec_char)
        if not chk: continue
        passwords[i] = p
        i += 1

def check_password(p, spec_char):
    """
    Complexity checking.  Each password is checked that at least one of each type of character:
    special, upper, lower, and a number.  If not, we return False and the password
    is effectively rejected.
    """
    if spec_char:
        s = re.compile("")
    else:
        s = re.compile(r"[\~\!\@\#\$\%\^\&\*\(\)\_\+\-\=\{\}\|\[\]\\\:\;\'\<\>\?\,\.\/\*]") # special
    l = re.compile("[a-z]") # lower
    u = re.compile("[A-Z]") # upper
    n = re.compile("[0-9]") # numbers
    return True if re.findall(s, p) and re.findall(l, p) and re.findall(u, p) and re.findall(n, p) else False

def dialog_qty():
    """
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

def dialog_length(qty):
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

def dialog_special(qty):
    """
    Creates a dialog to ask if special characters are wanted or not.
    Use case: sometimes dumb people make apps that they can't / won't
    allow special characters.
    """
    s = input("\n\tInclude special characters? ([y]/n): ")
    print("\n\n\tYour Passwords:\n\n") if qty > 1 else None
    return False if s.lower() != 'n' else True


def dialog_copy(copy, n=1):
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

def copy_pwd(p, n):
    """
    we attempt to import pyperclip, if the module is not
    installed locally, we error out and print the password to manually
    copy the password.
    """
    try:
        import pyperclip
    except ImportError as e:
        print(f"\n\tCan't copy to clipboard, {str(e).lower()}")
        print(f"\n\n\tYour password is: {p}\n\n")
        sys.exit()
    pyperclip.copy(p)
    print(f"\n\tPassword #{n} Copied.\n")

def write_file():
    home = os.path.expanduser('~')
    output = os.path.join(home, file_name)
    with open(output, 'w') as file:
        file.write('\n'.join(list(passwords.values()))+'\n')
    print(f"\n\tWritten to {output}\n\n")


def main():
    clear()
    """
    We start out looking at how many arguments are passed to the python script.
    > 3; then we send it to argparse to dissect the arguments and it handles any errors
    > 1; basically errors out and sends back an abbreviated help from argparse
    finally; we create dialogs to ask what the user wants and display from variables
    above.  The user can simply hit enter to accept all defaults and we'll handle it
    using try / except to choose for them.
    """
    copy = True
    file = False
    if len(sys.argv) > 2:
        qty, length, spec_char, copy, file = qty_and_length_args()
        if length < min_length or length > max_length:
            print(f"\n\tSpecified length {length} does not meet requirements\n\n\tLength has to be between {min_length} and {max_length}\n\n")
            sys.exit()
    elif len(sys.argv) > 1: # will simply send help to the user
        qty_and_length_args()
    else:
        loop = True
        while loop:
            qty, length, spec_char = dialog_qty()
            if qty and length:
                loop = False

    if qty == 1:
        gen_password(length, spec_char, file, qty)
        p = passwords.get(1)
        if file:
            write_file()
        elif copy:
            copy_pwd(p, 1)
        else:
            print(p) # to capture from stdout out let's just dump the password.
    elif file:
        gen_password(length, spec_char, file, qty)
        write_file()
    else:
        gen_password(length, spec_char, file, qty)
        for i,p in passwords.items():
            print(f"\t{i}.\t{p}")
        dialog_copy(copy, n=qty)

if __name__ == "__main__":
    main()
