import random


def get_salt_code(length=10):
    string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()_+-=/*[];\',./{}:"<>?"'
    return ''.join(random.choice(string) for _ in range(length))


def make_token(length=10):
    string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(string) for _ in range(length))
