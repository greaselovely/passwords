import random, os, re
import argparse
import sys
import pathlib
import requests
import inflect

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#####
#
# min_length = 12
# max_length = 31
# def_length = 25
min_qty = 0
max_qty = 20
def_number_of_words = 3
min_number_of_words = 2
max_number_of_words = 6
passphrases_file_name = "passphrases.txt"
word_list_file_name = "dictionary.txt"
expletive_file_name = "english_expletive.txt"
word_list_url = "https://github.com/dolph/dictionary/raw/master/popular.txt"
#
#####

"""
usage: passphrase_lemur.py [-h] -q QTY [-n NUM] [-c] [-f] [-o]

Generate passphrases when passed a quantity. Writing to file will override other options
(ie...copy) unless qty = 1

options:
  -h, --help         show this help message and exit
  -q QTY, --qty QTY  Number of passphrases to generate
  -n NUM, --num NUM  Number of words to use for passphrase
  -c, --copy         Copy passphrase to clipboard
  -f, --file         Write passphrases to file
  -o, --obfuscate    Obfuscates passphrase output to stdout

"""

passphrases = {}

local_path = pathlib.Path(__file__).parent
passphrases_full_path = pathlib.Path.joinpath(local_path, passphrases_file_name)
word_list_full_path = pathlib.Path.joinpath(local_path, word_list_file_name)
expletive_full_path = pathlib.Path.joinpath(local_path, expletive_file_name)

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def argue_with_me() -> tuple:
    """
    This is called if there are arguments passed to the script via cli,
    and assigns and returns the variables qty (int), length (int),
    spec_char (True / False) and copy (True / False) to the script.
    """
    parser = argparse.ArgumentParser(description='Generate passphrases when passed a quantity.  Writing to file will override other options (ie...copy) unless qty = 1')
    parser.add_argument('-q', '--qty', type=int, help='Number of passphrases to generate', required=True)
    parser.add_argument('-n', '--num', type=int, help='Number of words to use for passphrase', required=False)
    parser.add_argument('-c', '--copy', action='store_true', help='Copy passphrase to clipboard', required=False)
    parser.add_argument('-f', '--file', action='store_true', help='Write passphrases to file', required=False)
    parser.add_argument('-o', '--obfuscate', action='store_true', help='Obfuscates passphrase output to stdout', required=False)
    args = parser.parse_args()
    qty = args.qty
    copy = args.copy
    file = args.file
    obfuscate = args.obfuscate
    number_of_words = 3 if not args.num else args.num
    return number_of_words, qty, copy, file, obfuscate

def gen_passphrase(word_list: list, file: bool, number_of_words: int, qty=1) -> None:
    """
    Generate passphrases using the word list provided.
    Dictionary looks like:
    { 1: "word word word", 2: "word word word", 3: "word word word" }
    """
    i = 1
    while len(passphrases) < qty: # build a dict of passphrases
        pwd = ' '.join(random.choices(word_list, k=number_of_words))
        passphrases[i] = pwd  # add it to the dict
        i += 1  # increment the count which is used as key in dict
    if file: write_file(passphrases)

def dialog_qty() -> tuple:
    """
    Entry point for all dialogs and returns all results
    Creates a dialog to respond to for the number of passphrases to generate.  This function
    then calls the dialog_length function for how long each passphrase should be, and then returns both
    values so that it can be sent for passphrase(s) generation.  If invalid characters are entered, then we
    just make some decisions based on variables above.  Right now we are giving up if they enter more than
    the max_qty variable because it's not important to fight that level of dumb.
    """
    qty = input(f"\n\tNumber of passphrases to generate (1-[{max_qty}]): ")
    try:
        qty = int(qty)
    except ValueError:
        qty = max_qty
    if qty >= max_qty + 1:
        print("\n\tToo many, try again\n")
        sys.exit()
    return qty

def dialog_copy(copy: bool, n=1) -> None:
    """
    Creates a dialog to respond to for the passphrase to copy to the clipboard.
    If invalid characters are entered we simple choose a random integer between
    1 and the length of the passphrases word_list and then call copy_pwd.
    """
    more = " to copy:" if copy else ":"
    if n == 1:
        p = passphrases.get(n)
        copy_pwd(p, n)
    else:
        p2c = input(f"\n\tChoose a passphrase{more} ") # p2c = passphrase to copy
        try:
            p2c = int(p2c)
        except ValueError:
            p2c = random.randint(1, len(passphrases))
        p = passphrases.get(p2c)
        if p == None:
            p2c = random.randint(1, len(passphrases))
            p = passphrases.get(p2c)
        copy_pwd(p, p2c) if copy else print(f"\n\n\tYour passphrase is: {p}\n\n")

def copy_pwd(p: str, n: int) -> None:
    """
    we attempt to import pyperclip, if the module is not
    installed locally, we error out and print the passphrase to manually
    copy the passphrase.
    """
    try:
        import pyperclip
        pyperclip.copy(p)
        print(f"\n\tPassphrase #{n} Copied.\n")
    except ImportError as e:
        print(f"\n\tCan't copy to clipboard,n\t{str(e).lower()}")
        print(f"\n\n\tYour passphrase is: {p}\n\n")
        sys.exit()
    except pyperclip.PyperclipException as e:
        print(f"\n\tCan't copy to clipboard,\n\t\t{str(e).lower()}")
        print(f"\n\n\tYour passphrase is: {p}\n\n")
        sys.exit()

def write_file(passphrases: dict) -> None:
    """
    If the file (-f) argument is passed, we save the passphrases
    into the localpath of this script and display that path
    """
    with open(passphrases_full_path, 'w') as file:
        file.write('\n'.join(list(passphrases.values()))+'\n')
    print(f"\n\tWritten to {passphrases_full_path}\n\n")

def download_word_list():
    with open(word_list_full_path, 'w') as f:
        word_list = requests.get(word_list_url, verify=False).text
        f.write(word_list)
        word_list = word_list.split()
    return word_list

def clean_word_list(word_list: list) -> list:
    min_word_length = 6
    """
    Takes the word list, and removes all words in the english expletives file
    using inflect, we take every word, and attempt to make it singular, 
    and add to the new list.
    if inflect returns False, then we just add the word to new the list as it 
    Then it takes the list and makes a new unique valued list and then sorts it
    We then overwrite the dictionary file for future use.
    """
    with open(expletive_full_path, 'r') as f:
        expletives = f.read().splitlines()
    for expletive in expletives:
        try:
            expletive_index = word_list.index(expletive)
            word_list.pop(expletive_index)
        except ValueError:
            pass

    sanitized_word_list = []
    p = inflect.engine()
    for i, word in enumerate(word_list):
        if len(word) < min_word_length: continue  # I don't want short words
        try:
            sanitized_word_list.append(p.singular_noun(word)) if p.singular_noun(word) else sanitized_word_list.append(word)
        except IndexError:
            sanitized_word_list.append(word)

    final_word_list = list(set(sanitized_word_list)) # unique values
    final_word_list.sort()
    
    # write new dictionary file
    with open(word_list_full_path, 'w') as f:
        f.write('\n'.join(final_word_list) + '\n')
    return final_word_list

def main():
    clear()
    """
    This one is used to create a passphrase instead of a complex passphrase.

    It downloads a list from github, sanitizes it of expletives, and writes the new file.

    It then creates a list of strings, and each string is a three word passphrase.
    To do: give an option for number of words in a passphrase.

    We start out looking at how many arguments are passed to the python script.
    > 2; then we send it to argparse to dissect the arguments and it handles any errors
    > 1; basically errors out and sends back an abbreviated help from argparse
    finally; we create dialogs to ask what the user wants and display from variables
    above.  The user can simply hit enter to accept all defaults and we'll handle it
    using try / except to choose for them.
    """
    copy = True
    file = False
    obfuscate = False
    number_of_words = def_number_of_words

    # Download the word_list if it doesn't exist and clean it up
    if not pathlib.Path.is_file(word_list_full_path) or pathlib.Path(word_list_full_path).stat().st_size == 0:
        word_list = clean_word_list(download_word_list())
    else:
        with open(word_list_full_path, 'r') as f:
            word_list = f.read().splitlines()


    # Check for arguments, send to function if > 1 or > 2 or -h.
    # Otherwise generates passphrases
    if len(sys.argv) > 2:
        number_of_words, qty, copy, file, obfuscate = argue_with_me()
    elif len(sys.argv) > 1: # will simply send help to the user
        argue_with_me()
    else:
        loop = True
        while loop:
            qty = dialog_qty()
            if qty:
                loop = False

    if number_of_words > max_number_of_words:
        number_of_words = def_number_of_words
        print(f"\n\n\tMaximum number of words is {max_number_of_words}, using default of {number_of_words}\n\n")
    elif number_of_words < min_number_of_words:
        number_of_words = def_number_of_words
        print(f"\n\n\tMinimum number of words is {min_number_of_words}, using default of {number_of_words}\n\n")

    if qty == 1:
        gen_passphrase(word_list, file, number_of_words)
        p = passphrases.get(1)
        if copy:
            copy_pwd(p, 1)
        else:
            print(p if not file else '') # to capture from stdout out let's just dump the passphrase.
    elif file:
        gen_passphrase(word_list, file, number_of_words, qty)
    else:
        gen_passphrase(word_list, file, number_of_words, qty)
        print()
        for i,p in passphrases.items():
            print(f"\t{i}.\t{p if not obfuscate else '*' * len(p)}")
        dialog_copy(copy, n=qty)

if __name__ == "__main__":
    main()
