import hashlib
import random
import string

def add_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(3)])


def make_hash_pw(password, salt=None):
    if not salt:
        salt = add_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash, salt)

def check_hash(password, hash):
    salt = hash.split(',')[1]

    print("\n")
    print(hash)
    print(make_hash_pw(password, salt))
    print("\n")

    if make_hash_pw(password, salt) == hash:
        return True

    return False