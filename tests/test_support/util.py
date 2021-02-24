from hashlib import sha256

def digest(data):
    digest = sha256(data)
    digest_str = digest.hexdigest()
    return digest_str
