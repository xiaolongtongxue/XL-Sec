import hashlib
password = 'MTIzNDU2ix}@fP$pb/fKLo!+9ji?b>Tznw{.gr'
print(hashlib.sha512(password.encode()).hexdigest())