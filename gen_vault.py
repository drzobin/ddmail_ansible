"""Generate ansible vault file from template file"""
import argparse
import os
import string
import secrets
import sys
from argon2 import PasswordHasher


def gen_hash(string):
    """Generate argon2i hash from string."""
    ph = PasswordHasher()
    argon2i_hash = ph.hash(string)

    return argon2i_hash


def gen_pass(length):
    """Generate a password."""
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            sum(c.isdigit() for c in password) >= 3):
            break
    return password


def gen_key(length):
    """Generate a key in byte from"""
    key = secrets.token_hex(length)

    return key


if __name__ == "__main__":
    """Main function """

    # Get arguments from args.
    parser = argparse.ArgumentParser(
            description="Generate ansible vault file from template file"
            )

    parser.add_argument(
            '--template-file',
            type=str,
            help='Full path to input template file',
            required=True
            )
    parser.add_argument(
            '--output-file',
            type=str,
            help='Full path to output vault file',
            required=True
            )

    args = parser.parse_args()

    # Check that input template file exsist and is a file.
    if os.path.isfile(args.template_file) is False:
        print("Error: Template file can not be found")
        sys.exit(1)

    # Read the data from template file.
    f = open(args.template_file, "r")
    lines = f.readlines()
    f.close()

    # Open output file for writing
    f = open(args.output_file, "a")

    # Parse template file line by line.
    save = None
    for line in lines:
        if "change_me_to_password" in line:
            password = gen_pass(24)
            line = line.replace("change_me_to_password", password)
            save = line

            f.write(line)
        elif "change_me_to_argon2_hash" in line and save is not None:
            password = save.split(" ")[1]
            argon2i_hash = gen_hash(password)
            line = line.replace("change_me_to_argon2_hash", argon2i_hash)

            f.write(line)
            save = None
        elif "change_me_to_secret_key" in line:
            key = gen_key(128)
            line = line.replace("change_me_to_secret_key", key)

            f.write(line)
            save = None
        else:
            f.write(line)
            save = None
    f.close()

    print("Do not forget to encrypt the vault file with: ")
    print("ansible-vault encrypt " + args.output_file)
