from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
try:
    print(pwd_context.verify("Solca2026!", "$2b$12$1q1FCk/ijq6YU/e142.91.TSDVc6wgE43eYSy6EjsE0knO4g4K./u"))
except Exception as e:
    print("Error:", e)
