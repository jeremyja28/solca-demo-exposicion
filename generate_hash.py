import bcrypt
print(bcrypt.hashpw("Solca2026!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
