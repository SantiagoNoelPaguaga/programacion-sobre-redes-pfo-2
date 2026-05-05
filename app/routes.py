from flask import Blueprint, request, jsonify, render_template, session, redirect
from .models import db, Usuario
from .auth import hashear_password, verificar_password

main = Blueprint('main', __name__)

@main.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Faltan datos"}), 400
    
    usuario_nombre = datos['usuario']
    password_plana = datos['contraseña']
    
    if Usuario.query.filter_by(usuario=usuario_nombre).first():
        return jsonify({"error": "El nombre de usuario ya está ocupado"}), 400

    password_hash = hashear_password(password_plana)
    
    nuevo_usuario = Usuario(usuario=usuario_nombre, password_hash=password_hash)
    
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar en la base de datos"}), 500

@main.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Faltan credenciales"}), 400

    usuario_db = Usuario.query.filter_by(usuario=datos['usuario']).first()
    
    if usuario_db and verificar_password(usuario_db.password_hash, datos['contraseña']):
        session['usuario_id'] = usuario_db.id
        session['usuario_nombre'] = usuario_db.usuario
        return jsonify({"mensaje": "Inicio de sesión exitoso", "acceso": True}), 200
    
    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@main.route('/tareas', methods=['GET'])
def tareas():
    if 'usuario_id' not in session:
        return "<h1>Acceso Denegado</h1><p>Debes iniciar sesión primero.</p>", 401

    nombre = session.get('usuario_nombre')
    
    user_agent = request.headers.get('User-Agent', '')

    if 'python-requests' in user_agent:
        return render_template('bienvenida.html', nombre=nombre)
    else:
        url_github = f"https://santiagonoelpaguaga.github.io/programacion-sobre-redes-pfo-2/bienvenida.html?nombre={nombre}"
        return redirect(url_github)