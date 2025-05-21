from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

# Formulario para login de usuario
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

# Formulario para registrar un nuevo usuario
class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    
    role = SelectField(
        'Rol',
        choices=[('Paciente', 'Paciente'), ('Medico', 'Medico'), ('Admin', 'Admin')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Registrar')

# Formulario para cambiar la contraseña del usuario
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Contraseña actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar nueva contraseña', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Actualizar contraseña')

# Formulario para crear o editar una consulta médica
class ConsultaForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    
    role = SelectField(
        'Rol',
        choices=[('Paciente', 'Paciente'), ('Medico', 'Medico'), ('Admin', 'Admin')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Registrar')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password (optional)', validators=[Optional()])
    confirm_password = PasswordField('Confirm Password', validators=[Optional()])
    role = SelectField('Role', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update User')
