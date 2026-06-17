# =======================================
# SERVICES/ACESSOS.PY - Módulo de Autenticação e Banco de Dados
# Gerencia: Banco de dados, Hash de senhas, Autenticação, Auditoria
# =======================================
import sqlite3
import hashlib
import hmac
import secrets
from datetime import datetime
from pathlib import Path

# =======================================
# CONFIGURAÇÕES
# =======================================
DB_PATH = Path(__file__).parent.parent / "finaneasy.db"
SALT = secrets.token_hex(32)  # Salt para hash

# =======================================
# CLASSE DE USUÁRIO
# =======================================
class Pessoa:
    """Classe para representar um usuário"""
    def __init__(self, id, username, email, password_hash, role='user', created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# =======================================
# FUNÇÕES DE HASH
# =======================================
def hash_password(password, salt=None):
    """
    Hash de senha com PBKDF2
    
    Args:
        password (str): Senha em texto plano
        salt (str): Salt para o hash (gerado se None)
    
    Returns:
        tuple: (hash, salt) ou somente hash se salt fornecido
    """
    if salt is None:
        salt = secrets.token_hex(32)
    
    # PBKDF2 com SHA-256
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # Número de iterações
    ).hex()
    
    return password_hash, salt

def verify_password(stored_hash, stored_salt, provided_password):
    """
    Verifica se a senha fornecida corresponde ao hash armazenado
    
    Args:
        stored_hash (str): Hash armazenado no banco
        stored_salt (str): Salt armazenado no banco
        provided_password (str): Senha fornecida pelo usuário
    
    Returns:
        bool: True se a senha é válida
    """
    provided_hash, _ = hash_password(provided_password, stored_salt)
    return hmac.compare_digest(stored_hash, provided_hash)

# =======================================
# FUNÇÕES DE BANCO DE DADOS
# =======================================
def get_db_connection():
    """Obtém conexão com o banco de dados"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de contas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_name TEXT NOT NULL,
            account_type TEXT DEFAULT 'Corrente',
            bank_name TEXT,
            balance REAL DEFAULT 0,
            currency TEXT DEFAULT 'BRL',
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Tabela de transações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            transaction_date TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Tabela de auditoria
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Tabela de configurações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            theme TEXT DEFAULT 'light',
            currency TEXT DEFAULT 'BRL',
            language TEXT DEFAULT 'pt-BR',
            notifications BOOLEAN DEFAULT 1,
            two_factor_enabled BOOLEAN DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados inicializado com sucesso!")

# =======================================
# FUNÇÕES DE AUTENTICAÇÃO
# =======================================
def register_user(username, email, password):
    """
    Registra um novo usuário
    
    Args:
        username (str): Nome de usuário
        email (str): Email do usuário
        password (str): Senha em texto plano
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se usuário já existe
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            conn.close()
            return False, "Usuário ou email já cadastrado!"
        
        # Hash da senha
        password_hash, salt = hash_password(password)
        
        # Inserir novo usuário
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, salt)
            VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, salt))
        
        user_id = cursor.lastrowid
        
        # Criar configurações padrão
        cursor.execute("""
            INSERT INTO user_settings (user_id)
            VALUES (?)
        """, (user_id,))
        
        conn.commit()
        conn.close()
        
        log_audit(user_id, "REGISTER", f"Novo usuário {username} registrado")
        return True, "Usuário registrado com sucesso!"
    
    except Exception as e:
        return False, f"Erro ao registrar: {str(e)}"

def authenticate(username, password):
    """
    Autentica um usuário
    
    Args:
        username (str): Nome de usuário
        password (str): Senha em texto plano
    
    Returns:
        dict: Dados do usuário se autenticado, None caso contrário
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, salt, role, active
            FROM users
            WHERE username = ? AND active = 1
        """, (username,))
        
        user_row = cursor.fetchone()
        conn.close()
        
        if not user_row:
            return None
        
        # Verificar senha
        if verify_password(user_row['password_hash'], user_row['salt'], password):
            return {
                'id': user_row['id'],
                'username': user_row['username'],
                'email': user_row['email'],
                'role': user_row['role']
            }
        
        return None
    
    except Exception as e:
        print(f"Erro na autenticação: {str(e)}")
        return None

def get_user_by_username(username):
    """Obtém um usuário pelo nome de usuário"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, role, created_at, updated_at
            FROM users
            WHERE username = ?
        """, (username,))
        
        user_row = cursor.fetchone()
        conn.close()
        
        if user_row:
            return dict(user_row)
        return None
    
    except Exception as e:
        print(f"Erro ao obter usuário: {str(e)}")
        return None

def get_user_by_id(user_id):
    """Obtém um usuário pelo ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, role, created_at, updated_at
            FROM users
            WHERE id = ?
        """, (user_id,))
        
        user_row = cursor.fetchone()
        conn.close()
        
        if user_row:
            return dict(user_row)
        return None
    
    except Exception as e:
        print(f"Erro ao obter usuário: {str(e)}")
        return None

def update_user_profile(user_id, email=None, password=None):
    """Atualiza o perfil do usuário"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if email:
            cursor.execute("""
                UPDATE users
                SET email = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (email, user_id))
        
        if password:
            password_hash, salt = hash_password(password)
            cursor.execute("""
                UPDATE users
                SET password_hash = ?, salt = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (password_hash, salt, user_id))
        
        conn.commit()
        conn.close()
        
        log_audit(user_id, "UPDATE_PROFILE", "Perfil atualizado")
        return True, "Perfil atualizado com sucesso!"
    
    except Exception as e:
        return False, f"Erro ao atualizar perfil: {str(e)}"

# =======================================
# FUNÇÕES DE AUDITORIA
# =======================================
def log_audit(user_id, action, details="", ip_address="localhost"):
    """
    Registra uma ação no log de auditoria
    
    Args:
        user_id (int): ID do usuário
        action (str): Tipo de ação
        details (str): Detalhes da ação
        ip_address (str): Endereço IP
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO audit_log (user_id, action, details, ip_address)
            VALUES (?, ?, ?, ?)
        """, (user_id, action, details, ip_address))
        
        conn.commit()
        conn.close()
    
    except Exception as e:
        print(f"Erro ao registrar auditoria: {str(e)}")

def get_audit_log(user_id=None, limit=50):
    """Obtém o log de auditoria"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
                SELECT user_id, action, details, ip_address, datetime
                FROM audit_log
                WHERE user_id = ?
                ORDER BY datetime DESC
                LIMIT ?
            """, (user_id, limit))
        else:
            cursor.execute("""
                SELECT user_id, action, details, ip_address, datetime
                FROM audit_log
                ORDER BY datetime DESC
                LIMIT ?
            """, (limit,))
        
        logs = cursor.fetchall()
        conn.close()
        
        return [dict(log) for log in logs]
    
    except Exception as e:
        print(f"Erro ao obter log de auditoria: {str(e)}")
        return []

# =======================================
# FUNÇÕES AUXILIARES (para compatibilidade)
# =======================================
def generate_fake_data():
    """Gera dados fake para testes (opcional)"""
    pass

def load_df():
    """Carrega dados em DataFrame (opcional)"""
    pass
