-- 1. Eliminar base de datos existente
DROP DATABASE IF EXISTS consultas_medicas;

-- 2. Crear nueva base de datos
CREATE DATABASE consultas_medicas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3. Usar la base de datos
USE consultas_medicas;

-- 4. Crear tabla de roles
CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) UNIQUE
);

-- 5. Insertar roles básicos
INSERT INTO role (name) VALUES ('Admin'), ('Medico'), ('Paciente');

-- 6. Crear tabla de usuarios
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(256),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

-- 7. Crear tabla de consultas (con el nombre que espera tu aplicación)
CREATE TABLE consulta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME,
    medico_id INT,
    paciente_id INT,
    motivo TEXT,
    estado ENUM('Agendada', 'Cancelada', 'Realizada'),
    observaciones TEXT,
    diagnostico TEXT,
    FOREIGN KEY (medico_id) REFERENCES user(id),
    FOREIGN KEY (paciente_id) REFERENCES user(id)
);