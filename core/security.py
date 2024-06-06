from passlib.context import CryptContext

CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verificar_senha(senha, hash_senha):
    return CRYPTO.verify(senha, hash_senha)

def gerar_hash_senha(senha):
    return CRYPTO.hash(senha)