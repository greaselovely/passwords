"""
This script generates secure passphrases based on phonetic representations fetched from the Password Wolf API.
It supports various features including command-line arguments for customization, interactive user prompts,
the ability to copy passphrases to the clipboard, and options to write the generated passphrases to a file.

Features:
- Generate passphrases with a specified number of words.
- Fetch phonetic representations of passwords from an external API.
- Interactive user interface for customizing passphrase generation.
- Options to copy the generated passphrase to the clipboard or write to a file.
- Command-line argument support for automation and advanced usage.
"""


import random
import os
import argparse
import sys
import pathlib
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#####
#
min_qty = 0
max_qty = 20
def_number_of_words = 6
min_number_of_words = 2
max_number_of_words = max_qty
#
# Change to 'on' or 'off' to enable or disable each:
upper = 'on'
lower = 'on'
numbers = 'on'
special = 'on'
# phonetic = 'off'  # unused via API
#
# Length of the password
length = 16
# number of passwords to generate:
qty = 9
# characters to exclude:
# If we were using the actual password generated
# we may not want crazy special characters, but 
# we want more diversity in the phrase so we don't
# ie...exclude = r"@!<>|[]{}/?&^,`)(" 
exclude = ""
#
#####

"""
usage: passphrase_genut.py [-h] -q QTY [-n NUM] [-c] [-f] [-o]

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
passphrases_file_name = "passphrases.txt"
passphrases_full_path = pathlib.Path.joinpath(local_path, passphrases_file_name)


def clear() -> None:
    """
    Clears the terminal screen. Uses 'cls' for Windows and 'clear' for Unix/Linux.
    """
    os.system("cls" if os.name == "nt" else "clear")

def argue_with_me() -> tuple:
    """
    Parses command-line arguments to customize passphrase generation.

    This function handles the parsing of command-line arguments, providing options for the quantity of passphrases,
    the number of words per passphrase, and flags for copying to clipboard, writing to file, and obfuscating output.

    Returns:
        tuple: A tuple containing the parsed number of words, quantity, copy flag, file flag, and obfuscate flag.
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

def dialog_qty() -> tuple:
    """
    Prompts the user for the quantity of passphrases to generate and the number of words per passphrase.

    This function asks the user to input the desired number of passphrases and the preferred number of words
    for each passphrase. It validates and ensures the input falls within predefined limits or sets defaults.

    Returns:
        tuple: A tuple containing the user-specified quantity of passphrases and number of words per passphrase.
    """
    qty = input(f"\n\tNumber of passphrases to generate (1-[{max_qty}]): ")
    try:
        qty = int(qty)
    except ValueError:
        qty = max_qty
    if qty >= max_qty + 1:
        print("\n\tToo many, try again\n")
        sys.exit()
    num = dialog_num_of_words()
    return qty, num

def dialog_num_of_words() -> int:
    """
    Prompts the user for the desired number of words in each passphrase.

    The function asks for user input and validates it, ensuring it falls within the pre-defined
    minimum and maximum number of words. If the input is invalid or not provided, defaults to a preset value.

    Returns:
        int: The number of words to be used in each passphrase, as specified by the user or the default value.
    """
    num = input(f"\n\tNumber of words per passphrase (2-{max_qty}) [{def_number_of_words}]: ")
    try:
        num = int(num)
    except ValueError:
        num = def_number_of_words
    if num >= max_number_of_words + 1:
        print("\n\tToo many, using defaults\n")
        num = def_number_of_words
    return num

def dialog_copy(copy: bool, n=1) -> None:
    """
    Handles the selection of a passphrase to copy to the clipboard or display.

    If multiple passphrases are generated, this function prompts the user to choose one. If only one is generated,
    or if the `-c/--copy` flag is used, it automatically copies the passphrase to the clipboard or displays it.

    Parameters:
        copy (bool): Indicates whether the passphrase should be copied to the clipboard.
        n (int): The number of passphrases generated, to determine if user input is needed for selection.
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

def password_wolf(length: int, numbers: int, upper: str, lower: str, special: str, exclude: str, qty: int) -> list:
    """
    Fetches passwords from the Password Wolf API based on specified parameters.

    Parameters:
        length (int): The length of each password.
        numbers (int): The inclusion of numbers in the password.
        upper (str): Enable or disable uppercase letters in the password.
        lower (str): Enable or disable lowercase letters in the password.
        special (str): Enable or disable special characters in the password.
        exclude (str): Characters to exclude from the password.
        qty (int): The quantity of passwords to fetch.

    Returns:
        list: A list of dictionaries, each containing a password and its phonetic representation.
    """
    URL = f"https://passwordwolf.com/api/?length={length}&numbers={numbers}&upper={upper}&lower={lower}&special={special}&exclude={exclude}&repeat={qty}"
    passwords = requests.get(URL, verify=False).json()
    return passwords

def gen_passphrase(word_list: list, file: bool, number_of_words: int, qty=1) -> None:
    """
    Generates and stores passphrases based on the provided word list and options.

    Takes a list of phonetic representations, slices each to the desired number of words, and stores the results.
    If the file option is enabled, writes the generated passphrases to a file.

    Parameters:
        word_list (list): A list of dictionaries containing phonetic representations of passwords.
        file (bool): Flag indicating whether to write the passphrases to a file.
        number_of_words (int): The number of words to include in each passphrase.
        qty (int): The number of passphrases to generate.
    """
    for i, p in enumerate(word_list, start=1):
        words = p['phonetic'].split()  # Split the phonetic string into a list of words
        passphrases[i] = ' '.join(words[:number_of_words])  # Join the first 'number_of_words' back into a string
    
    if file: write_file(passphrases)

def copy_pwd(p: str, n: int) -> None:
    """
    Copies the selected passphrase to the clipboard, if possible.

    Attempts to use the `pyperclip` library to copy the selected passphrase to the clipboard. If `pyperclip` is not
    installed or if copying fails, displays the passphrase and prompts the user to manually copy it.

    Parameters:
        p (str): The passphrase to copy.
        n (int): The numeric identifier of the selected passphrase, for display purposes.
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
    Writes the generated passphrases to a file.

    Saves all generated passphrases to a predefined file location. The file path is determined based on the script's
    location and a predefined filename. Each passphrase is written on a new line.

    Parameters:
        passphrases (dict): A dictionary of passphrases to write, with keys as identifiers and values as passphrase strings.
    """
    with open(passphrases_full_path, 'w') as file:
        file.write('\n'.join(list(passphrases.values()))+'\n')
    print(f"\n\tWritten to {passphrases_full_path}\n\n")


def main():
    """
    Main function to orchestrate the passphrase generation process.

    This function acts as the entry point for the script, handling user interactions, parsing command-line arguments,
    generating passphrases based on user preferences, and managing output options such as copying to clipboard,
    writing to a file, or obfuscating the output.
    """
    clear()
    copy = True
    file = False
    obfuscate = False
    number_of_words = def_number_of_words

    # Check for arguments, send to function if > 1 or > 2 or -h.
    # Otherwise generates passphrases
    if len(sys.argv) > 2:
        number_of_words, qty, copy, file, obfuscate = argue_with_me()
    elif len(sys.argv) > 1: # will simply send help to the user
        argue_with_me()
    else:
        loop = True
        while loop:
            qty, number_of_words = dialog_qty()
            if qty:
                loop = False

    if number_of_words > max_number_of_words:
        number_of_words = def_number_of_words
        print(f"\n\n\tMaximum number of words is {max_number_of_words}, using default of {number_of_words}\n\n")
    elif number_of_words < min_number_of_words:
        number_of_words = def_number_of_words
        print(f"\n\n\tMinimum number of words is {min_number_of_words}, using default of {number_of_words}\n\n")

    passwords = password_wolf(length, numbers, upper, lower, special, exclude, qty)

    if qty == 1:
        gen_passphrase(passwords, file, number_of_words)
        p = passphrases.get(1)
        if copy:
            copy_pwd(p, 1)
        else:
            print(p if not file else '') # to capture from stdout out let's just dump the passphrase.
    elif file:
        gen_passphrase(passwords, file, number_of_words, qty)
    else:
        gen_passphrase(passwords, file, number_of_words, qty)
        print()
        
        for i,p in passphrases.items():
            print(f"\t{i}.\t{p if not obfuscate else '*' * len(p)}")
        dialog_copy(copy, n=qty)

if __name__ == "__main__":
    main()
