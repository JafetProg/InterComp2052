from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Carga el usuario desde su ID (para Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de rol (Admin, Medico, Paciente)
class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    # Relación con usuarios
    users = db.relationship('User', backref='role', lazy=True)

# Modelo de usuario
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relaciones según rol
    consultas_como_medico = db.relationship('Consulta', backref='medico', foreign_keys='Consulta.medico_id', lazy=True)
    consultas_como_paciente = db.relationship('Consulta', backref='paciente', foreign_keys='Consulta.paciente_id', lazy=True)

    def set_password(self, password: str):
        """Genera el hash de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica la contraseña contra el hash almacenado."""
        return check_password_hash(self.password_hash, password)

# Modelo de consulta médica
class Consulta(db.Model):
    __tablename__ = 'consulta'

    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    diagnostico = db.Column(db.Text, nullable=True)

    # Relaciones con usuarios
    medico_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
