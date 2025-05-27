import hashlib

def hashlib_md5(value):
    """Genera un hash MD5 a partir de un valor dado"""
    return hashlib.md5(value.strip().lower().encode('utf-8')).hexdigest()