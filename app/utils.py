import hashlib

def hashlib_md5(value):
    return hashlib.md5(value.strip().lower().encode('utf-8')).hexdigest()