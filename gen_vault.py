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

def parse_key(file):
    """Parse OpenPGP and ssh key files"""
    # Read the data from file.
    f = open(file, "r")
    data = f.read()
    f.close()

    data = data.replace("\n","\\n")
    data = "\"" + data + "\""

    return data

if __name__ == "__main__":
    """Main function """

    # Get arguments from args.
    parser = argparse.ArgumentParser(
            description="Generate ansible vault file from template file"
            )

    parser.add_argument(
            '-t',
            '--template-file',
            type=str,
            help='Input template file',
            required=True
            )
    parser.add_argument(
            '-o',
            '--output-file',
            type=str,
            help='Output vault file',
            required=True
            )
    parser.add_argument(
            '-btpub',
            '--backup-taker-pubkey',
            type=str,
            help='OpenPGP armored public key file used for encrypting backups with backup_taker',
            required=True
            )
    parser.add_argument(
            '-btpf',
            '--backup-taker-pubkey-fingerprint',
            type=str,
            help='OpenPGP fingerprint of public key used for encrypting backups with backup_taker',
            required=True
            )
    parser.add_argument(
            '-gspub',
            '--github-ssh-pubkey',
            type=str,
            help='Developers github ssh public key',
            required=False
            )
    parser.add_argument(
            '-gspriv',
            '--github-ssh-privkey',
            type=str,
            help='Developers github ssh private key',
            required=False
            )

    args = parser.parse_args()

    # Check that input template file exsist and is a file.
    if os.path.isfile(args.template_file) is False:
        print("Error: Template file can not be found")
        sys.exit(1)

    # check thath backup_taker pubkey is a file
    if os.path.isfile(args.backup_taker_pubkey) is False:
        print("Error: OpenPGP public key file can not be found")
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
        elif "vault_mailsystem_db_dev_user_password_hash" in line:
            argon2i_hash = gen_hash("password")
            line = line.replace("change_me_to_argon2_hash", argon2i_hash)

            f.write(line)
            save = None
        elif "vault_mailsystem_db_dev_user_file_hash" in line:
            argon2i_hash = gen_hash("password")
            line = line.replace("change_me_to_argon2_hash", argon2i_hash)

            f.write(line)
            save = None
        elif "vault_mailsystem_db_dev_email_hash" in line:
            none_default_ph = PasswordHasher(time_cost=3,memory_cost=65536,parallelism=1)
            argon2i_hash = none_default_ph.hash("password")
            line = line.replace("change_me_to_argon2_hash", argon2i_hash)

            f.write(line)
            save = None
        elif "vault_ddmail_backup_taker_pubkey_fingerprint" in line:
            line = line.replace("change_me", args.backup_taker_pubkey_fingerprint)

            f.write(line)
            save = None
        elif "vault_ddmail_backup_taker_pubkey" in line:
            pub_key_data = parse_key(args.backup_taker_pubkey)

            data = "vault_ddmail_backup_taker_pubkey: " + pub_key_data + "\n"

            f.write(data)
            save = None
        elif "vault_github_ssh_pubkey" in line and args.github_ssh_pubkey is not None:
            pub_key_data = parse_key(args.github_ssh_pubkey)

            data = "vault_github_ssh_pubkey: " + pub_key_data + "\n"
            f.write(data)
            save = None
        elif "vault_github_ssh_privkey" in line and args.github_ssh_privkey is not None:
            priv_key_data = parse_key(args.github_ssh_privkey)

            data = "vault_github_ssh_privkey: " + priv_key_data + "\n"
            f.write(data)
            save = None
        else:
            f.write(line)
            save = None
    f.close()

    print("Do not forget to encrypt the vault file with: ")
    print("ansible-vault encrypt " + args.output_file)
