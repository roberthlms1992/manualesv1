from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL no está configurada. Asegúrate de definirla en Render.")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

class Manual(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    ata = db.Column(db.String(10), nullable=False)
    numero_parte_manual = db.Column(db.String(50), nullable=False)
    fabricante = db.Column(db.String(100), nullable=False)
    numero_revision = db.Column(db.String(20), nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=False)
    numero_parte_componente = db.Column(db.String(50), nullable=False)
    pdf_path = db.Column(db.String(255), nullable=False)

@app.route('/')
def home():
    return jsonify({'message': 'API de Manuales funcionando correctamente'}), 200

@app.route('/manuals', methods=['GET'])
def get_manuals():
    manuals = Manual.query.all()
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre,
        'ata': m.ata,
        'numero_parte_manual': m.numero_parte_manual,
        'fabricante': m.fabricante,
        'numero_revision': m.numero_revision,
        'fecha_publicacion': m.fecha_publicacion.strftime('%Y-%m-%d'),
        'numero_parte_componente': m.numero_parte_componente,
        'pdf_path': m.pdf_path
    } for m in manuals])

@app.route('/manuals/<int:id>', methods=['GET'])
def get_manual(id):
    manual = Manual.query.get(id)
    if not manual:
        return jsonify({'error': 'Manual no encontrado'}), 404
    return jsonify({
        'id': manual.id,
        'nombre': manual.nombre,
        'ata': manual.ata,
        'numero_parte_manual': manual.numero_parte_manual,
        'fabricante': manual.fabricante,
        'numero_revision': manual.numero_revision,
        'fecha_publicacion': manual.fecha_publicacion.strftime('%Y-%m-%d'),
        'numero_parte_componente': manual.numero_parte_componente,
        'pdf_path': manual.pdf_path
    })

@app.route('/manuals', methods=['POST'])
def add_manual():
    data = request.form
    pdf_file = request.files['pdf']
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)

    manual = Manual(
        nombre=data['nombre'],
        ata=data['ata'],
        numero_parte_manual=data['numero_parte_manual'],
        fabricante=data['fabricante'],
        numero_revision=data['numero_revision'],
        fecha_publicacion=data['fecha_publicacion'],
        numero_parte_componente=data['numero_parte_componente'],
        pdf_path=pdf_path
    )
    db.session.add(manual)
    db.session.commit()

    return jsonify({'message': 'Manual agregado exitosamente'}), 201

@app.route('/manuals/<int:id>', methods=['PUT'])
def update_manual(id):
    manual = Manual.query.get(id)
    if not manual:
        return jsonify({'error': 'Manual no encontrado'}), 404

    data = request.json
    manual.nombre = data.get('nombre', manual.nombre)
    manual.ata = data.get('ata', manual.ata)
    manual.numero_parte_manual = data.get('numero_parte_manual', manual.numero_parte_manual)
    manual.fabricante = data.get('fabricante', manual.fabricante)
    manual.numero_revision = data.get('numero_revision', manual.numero_revision)
    manual.fecha_publicacion = data.get('fecha_publicacion', manual.fecha_publicacion)
    manual.numero_parte_componente = data.get('numero_parte_componente', manual.numero_parte_componente)
    
    db.session.commit()
    return jsonify({'message': 'Manual actualizado correctamente'})

@app.route('/manuals/<int:id>', methods=['DELETE'])
def delete_manual(id):
    manual = Manual.query.get(id)
    if not manual:
        return jsonify({'error': 'Manual no encontrado'}), 404

    db.session.delete(manual)
    db.session.commit()
    return jsonify({'message': 'Manual eliminado correctamente'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
