import os

class Config:
    """
    Configuración segura y escalable para el sistema de consultas médicas.
    Implementa buenas prácticas para entornos de desarrollo y producción.
    """

    # Seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
    SESSION_COOKIE_SECURE = True  # Solo enviar cookies sobre HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protección CSRF

    # Base de datos - Configuración robusta
    DB_USER = os.environ.get('DB_USER', 'root') 
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')  
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'consultas_medicas')  

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?charset=utf8mb4&connect_timeout=10"
    )
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,  # Verifica conexiones antes de usarlas
        'max_overflow': 20,
        'isolation_level': 'READ COMMITTED'  # Nivel de aislamiento para transacciones
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False  # Solo activar para debugging

    # Configuración adicional para el sistema médico
    MEDICAL_CONFIG = {
        'MAX_CONSULTAS_DIARIAS': 30,  # Límite de consultas por día
        'HORARIO_ATENCION': '08:00-17:00',
        'DIAS_ATENCION': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    }

    # Configuración de logs
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }


class DevelopmentConfig(Config):
    """Configuración específica para desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Muestra queries SQL en consola
    SQLALCHEMY_RECORD_QUERIES = True
    EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(Config):
    """Configuración específica para producción"""
    DEBUG = False
    PREFERRED_URL_SCHEME = 'https'
    SQLALCHEMY_ENGINE_OPTIONS = {
        **Config.SQLALCHEMY_ENGINE_OPTIONS,
        'pool_size': 20,
        'max_overflow': 30
    }