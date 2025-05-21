from datetime import datetime  
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import ConsultaForm, ChangePasswordForm, EditUserForm
from app.models import Role, db, Consulta, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual es incorrecta.')
            return render_template('cambiar_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Contraseña actualizada correctamente.')
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name == 'Paciente':
        consultas = Consulta.query.filter_by(paciente_id=current_user.id).all()
    elif current_user.role.name == 'Medico':
        consultas = Consulta.query.filter_by(medico_id=current_user.id).all()
    else:  # Admin
        consultas = Consulta.query.all()

    return render_template('dashboard.html', consultas=consultas)

@main.route('/consultas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_consulta():
    if current_user.role.name not in ['Medico', 'Admin']:
        flash('No tienes permiso para crear consultas.')
        return redirect(url_for('main.dashboard'))

    form = ConsultaForm()
    if form.validate_on_submit():
        consulta = Consulta(
            paciente_id=form.paciente_id.data,
            medico_id=current_user.id if current_user.role.name == 'Medico' else form.medico_id.data,
            fecha_hora=form.fecha_hora.data,
            motivo=form.motivo.data,
            diagnostico=form.diagnostico.data,
            estado=form.estado.data
        )
        db.session.add(consulta)
        db.session.commit()
        flash("Consulta creada correctamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('consultas_form.html', form=form)

@main.route('/consultas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_consulta(id):
    consulta = Consulta.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Medico'] or (
        consulta.medico_id != current_user.id and current_user.role.name != 'Admin'):
        flash('No tienes permiso para editar esta consulta.')
        return redirect(url_for('main.dashboard'))

    form = ConsultaForm(obj=consulta)
    if form.validate_on_submit():
        consulta.paciente_id = form.paciente_id.data
        consulta.fecha_hora = form.fecha_hora.data
        consulta.motivo = form.motivo.data
        consulta.diagnostico = form.diagnostico.data
        consulta.estado = form.estado.data
        db.session.commit()
        flash("Consulta actualizada correctamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('consultas_form.html', form=form, editar=True)

@main.route('/consultas/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_consulta(id):
    consulta = Consulta.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Medico'] or (
        consulta.medico_id != current_user.id and current_user.role.name != 'Admin'):
        flash('No tienes permiso para eliminar esta consulta.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(consulta)
    db.session.commit()
    flash("Consulta eliminada correctamente.")
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role.name != 'Admin':
        flash("No tienes permiso para ver esta página.")
        return redirect(url_for('main.dashboard'))

    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)

@main.route('/guardar_consulta', methods=['POST'])
def guardar_consulta():
    if request.method == 'POST':
        try:
            nueva_consulta = Consulta(
                paciente_id=request.form.get('paciente_id'),
                medico_id=request.form.get('medico_id') or current_user.id,
                fecha_hora=datetime.strptime(
                    f"{request.form.get('fecha')} {request.form.get('hora')}", 
                    '%Y-%m-%d %H:%M'
                ),
                motivo=request.form.get('motivo'),
                diagnostico=request.form.get('diagnostico'),
                estado=request.form.get('estado')
            )
            
            db.session.add(nueva_consulta)
            db.session.commit()
            
            flash('Consulta guardada exitosamente!', 'success')
            return redirect(url_for('main.nueva_consulta'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar la consulta: {str(e)}', 'danger')
            return redirect(url_for('main.nueva_consulta'))

# ✅ Estas rutas estaban mal indentadas, ahora están en el lugar correcto:

@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('main.listar_usuarios'))

@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    form.role.choices = [(role.id, role.name) for role in Role.query.all()]

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role_id = form.role.data

        if form.password.data:
            if form.password.data == form.confirm_password.data:
                user.set_password(form.password.data)
            else:
                flash("Passwords do not match.", "danger")
                return render_template('main.edit_user.html', form=form, user=user)

        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('main.listar_usuarios'))

    form.role.data = user.role_id
    return render_template('edit_user.html', form=form, user=user)
