from werkzeug.security import generate_password_hash, check_password_hash

def hashear_password(password):
    return generate_password_hash(password)

def verificar_password(password_hash, password_plana):
    return check_password_hash(password_hash, password_plana)