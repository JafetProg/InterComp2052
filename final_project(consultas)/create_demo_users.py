from app import create_app, db
from app.models import Role, User

app = create_app()

with app.app_context():
    # Roles para el sistema médico
    roles = ['Administrador', 'Medico', 'Paciente']
    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            print(f'✅ Rol "{role_name}" creado.')

    db.session.commit()

    # Usuarios médicos iniciales
    users_data = [
        {
            "username": "Dr. Juan Pérez",
            "email": "medico@example.com",
            "password": "medico123",
            "role_name": "medico"
        },
        {
            "username": "Lucía Gómez",
            "email": "pacciente@example.com",
            "password": "paciente123",
            "role_name": "Paciente"
        },
        {
            "username": "Admin General",
            "email": "admin@hospital.com",
            "password": "adminmedico123",
            "role_name": "Administrador"
        }
    ]

    for user_info in users_data:
        existing_user = User.query.filter_by(email=user_info['email']).first()
        if not existing_user:
            role = Role.query.filter_by(name=user_info['role_name']).first()
            user = User(
                username=user_info['username'],
                email=user_info['email'],
                role=role
            )
            user.set_password(user_info['password'])  # Asegúrate de que el modelo User tenga este método
            db.session.add(user)
            print(f'✅ Usuario "{user.username}" creado con rol "{role.name}".')
        else:
            print(f'ℹ️ El usuario con email {user_info["email"]} ya existe.')

    db.session.commit()
    print("✅ Todos los usuarios médicos fueron procesados correctamente.")
