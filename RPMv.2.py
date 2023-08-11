# Gen.2

import sys
import random
from getpass import getpass
import hashlib
from time import sleep
import pyperclip as pc

VERSION = 2
name = f"RPMv.{VERSION}.py"


class f:
    """Contains variables used for formatting."""

    l = 30  # line len

    tl = "╭"
    bl = "╰"
    tr = "╮"
    br = "╯"

    h = "─"
    v = "│"

    top = tl + l * h + tr
    bottom = bl + l * h + br


def help_msg():
    """Prints a list of commands arguments that
    can be used with this script."""

    print(
        f"""{f.top}
{f.v}   Commands Help
{f.v}   
{f.v}   --help
{f.v}    {f.bl} shows this page
{f.v}
{f.v}   --hide-all
{f.v}    {f.bl} Disables terminal input viewing for both password and key.
{f.v}
{f.v}   --hide-pass
{f.v}    {f.bl} Disables terminal input viewing for the password.
{f.v}
{f.v}   --hide-key
{f.v}    {f.bl} Disables terminal input viewing for the key.
{f.bottom}"""
    )
    sys.exit(0)


def startup():
    """Prints a startup message."""

    print(
        f"""{f.top}
{f.v}       ── Roc ────────
{f.v}       Password Manager
{f.v}       ──────── v.{VERSION} ──
{f.v}       
{f.v}    * run {name} --help
{f.v}    for additional options
{f.bottom}"""
    )


def get_secure(key_type, hide, double):
    """Function for prompting and getting secure values,
    dynamic based on function inputs."""

    checker_list = []

    if double:
        iterations = 2
    else:
        iterations = 1

    for _ in range(iterations):
        if hide:
            secureValue = str(getpass(f"{f.v} {key_type}: "))
            if secureValue == "":
                print("ERRORx1: ValueError, Required field left blank.")
                sys.exit(1)

            checker_list.append(secureValue)
        else:
            secureValue = str(input(f"{f.v} {key_type}: "))
            if secureValue == "":
                print("ERRORx1: ValueError, Required field left blank.")
                sys.exit(1)

            checker_list.append(secureValue)

    if iterations == 2:
        if checker_list[0] == checker_list[1]:
            return secureValue
        else:
            print("Double-checker failed.")
            sys.exit(2)
    else:
        return secureValue


def promptUser(hide, double):
    """Prompts the user for values used by the rest of the script."""

    global masterPassword, referenceKey, passwordLength, showPassword

    print(f.top)

    masterPassword = get_secure("Master Password", hide, double)
    referenceKey = get_secure("Reference Key", hide, double)

    passwordLength = input(f"{f.v} Output Len: ")
    if passwordLength == "":
        passwordLength = 22
    else:
        try:
            passwordLength = int(passwordLength)
        except ValueError:
            print("ERRORx1: ValueError, An integer was not entered.")
            sys.exit(1)

    showPassword = str(input(f"{f.v} Show Output (y / n): "))
    if showPassword == "y" or showPassword == "Y":
        showPassword = True
    elif showPassword == "n" or showPassword == "N":
        showPassword = False
    elif showPassword == "" or showPassword == " ":
        showPassword = False
    else:
        print("ERRORx1: ValueError, Invalid input to y/n question.")
        sys.exit(1)

    print(f.bottom)


def generator(seed, length):
    """Generates a password based on the values passed to this function."""

    random.seed(seed)

    characters = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=~"
    )

    hasher = hashlib.sha256()

    password = ""
    while len(password) < length:
        data = str(random.random()).encode() + seed.encode()
        hasher.update(data)
        digest = hasher.digest()
        for byte in digest:
            if len(password) >= length:
                break
            index = byte % len(characters)
            password += characters[index]

    return password


def rpm(hide: bool, double: bool):
    """The core of the code."""

    # Prompts the user for values
    promptUser(hide, double)

    # Generates Password
    pw = generator((masterPassword + referenceKey), passwordLength)

    # Either prints or copies the password
    if showPassword:
        print(f.top)
        print(f.v, pw)
        print(f.bottom)
    else:
        pc.copy(pw)

        print(f"{f.tl} Copied to Clipboard! Clearing in 15 seconds.")

        sleep(15)

        pc.copy("// Cleared //")
        print(f"{f.bl} Clipboard Cleared!")

        sys.exit(0)


if __name__ == "__main__":
    startup()

    # Sets Defaults
    hideInput = False
    doubleAsk = False

    # Checks arguments and gets user values
    for arg_index in sys.argv[1:]:
        try:
            if "--hide" in arg_index:
                hideInput = True
            elif "--help" in arg_index:
                help_msg()
                break
            elif "--double" in arg_index:
                doubleAsk = True
        except IndexError:
            pass

    rpm(hideInput, doubleAsk)
