from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'desdepixela3d_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

USUARIO = 'ariel'
PASSWORD_HASH = generate_password_hash('Mandarina1')

UPLOAD_FOLDER = os.path.join('static', 'uploads')

# Modelo de la base de datos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    foto = db.Column(db.String(200), nullable=False)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    return 'El servidor de Desde Pixel a 3D está funcionando.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    datos = request.get_json()
    usuario = datos.get('usuario')
    password = datos.get('password')
    if usuario == USUARIO and check_password_hash(PASSWORD_HASH, password):
        session['autenticado'] = True
        return jsonify({'ok': True})
    return jsonify({'ok': False})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if not session.get('autenticado'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/admin/subir', methods=['POST'])
def subir_producto():
    if not session.get('autenticado'):
        return jsonify({'ok': False})

    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    foto = request.files.get('foto')

    if not nombre or not descripcion or not foto:
        return jsonify({'ok': False})

    nombre_foto = secure_filename(foto.filename)
    foto.save(os.path.join(UPLOAD_FOLDER, nombre_foto))

    producto = Producto(nombre=nombre, descripcion=descripcion, foto=nombre_foto)
    db.session.add(producto)
    db.session.commit()

    return jsonify({'ok': True})

@app.route('/admin/productos')
def listar_productos():
    if not session.get('autenticado'):
        return jsonify([])
    productos = Producto.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'descripcion': p.descripcion,
        'foto': p.foto
    } for p in productos])

@app.route('/admin/eliminar/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    if not session.get('autenticado'):
        return jsonify({'ok': False})
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True)