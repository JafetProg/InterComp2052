from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Consulta

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    return '<h1>API de Consultas Médicas corriendo en modo prueba.</h1>'

@main.route('/consultas', methods=['GET'])
@login_required
def listar_consultas():
    consultas = Consulta.query.all()
    data = [
        {
            'id': consulta.id,
            'paciente_id': consulta.paciente_id,
            'medico_id': consulta.medico_id,
            'fecha_hora': consulta.fecha_hora.isoformat(),
            'motivo': consulta.motivo,
            'diagnostico': consulta.diagnostico,
            'estado': consulta.estado
        }
        for consulta in consultas
    ]
    return jsonify(data), 200

@main.route('/consultas/<int:id>', methods=['GET'])
@login_required
def obtener_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    data = {
        'id': consulta.id,
        'paciente_id': consulta.paciente_id,
        'medico_id': consulta.medico_id,
        'fecha_hora': consulta.fecha_hora.isoformat(),
        'motivo': consulta.motivo,
        'diagnostico': consulta.diagnostico,
        'estado': consulta.estado
    }
    return jsonify(data), 200

@main.route('/consultas', methods=['POST'])
@login_required
def crear_consulta():
    if current_user.role.name not in ['Medico', 'Admin']:
        return jsonify({'error': 'No tienes permiso para crear consultas.'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    try:
        consulta = Consulta(
            paciente_id=data.get('paciente_id'),
            medico_id=current_user.id if current_user.role.name == 'Medico' else data.get('medico_id'),
            fecha_hora=data.get('fecha_hora'),
            motivo=data.get('motivo'),
            diagnostico=data.get('diagnostico'),
            estado=data.get('estado', 'Pendiente')
        )

        db.session.add(consulta)
        db.session.commit()
        return jsonify({'message': 'Consulta creada', 'id': consulta.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear consulta: {str(e)}'}), 500

@main.route('/consultas/<int:id>', methods=['PUT'])
@login_required
def actualizar_consulta(id):
    consulta = Consulta.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Medico'] or \
       (consulta.medico_id != current_user.id and current_user.role.name != 'Admin'):
        return jsonify({'error': 'No tienes permiso para actualizar esta consulta.'}), 403

    data = request.get_json()
    try:
        consulta.fecha_hora = data.get('fecha_hora', consulta.fecha_hora)
        consulta.motivo = data.get('motivo', consulta.motivo)
        consulta.diagnostico = data.get('diagnostico', consulta.diagnostico)
        consulta.estado = data.get('estado', consulta.estado)

        db.session.commit()
        return jsonify({'message': 'Consulta actualizada', 'id': consulta.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar consulta: {str(e)}'}), 500

@main.route('/consultas/<int:id>', methods=['DELETE'])
@login_required
def eliminar_consulta(id):
    consulta = Consulta.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Medico'] or \
       (consulta.medico_id != current_user.id and current_user.role.name != 'Admin'):
        return jsonify({'error': 'No tienes permiso para eliminar esta consulta.'}), 403

    try:
        db.session.delete(consulta)
        db.session.commit()
        return jsonify({'message': 'Consulta eliminada', 'id': consulta.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar consulta: {str(e)}'}), 500
