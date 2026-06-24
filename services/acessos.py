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
# FUNÇÕES DE CONTAS (ACCOUNTS)
# =======================================
def criar_conta(user_id, account_name, account_type="Corrente", bank_name=None, balance=0):
    """Cria uma nova conta para o usuário"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO accounts (user_id, account_name, account_type, bank_name, balance)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, account_name, account_type, bank_name, balance))
    conn.commit()
    account_id = cursor.lastrowid
    conn.close()
    log_audit(user_id, "CREATE_ACCOUNT", f"Conta {account_name} criada")
    return account_id

def listar_contas(user_id):
    """Lista as contas ativas de um usuário"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, account_name, account_type, bank_name, balance, active, created_at
        FROM accounts
        WHERE user_id = ? AND active = 1
        ORDER BY created_at
    """, (user_id,))
    contas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return contas

def obter_conta(account_id):
    """Obtém uma conta pelo id"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def saldo_total(user_id):
    """Soma o saldo de todas as contas ativas do usuário"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(SUM(balance), 0) AS total FROM accounts WHERE user_id = ? AND active = 1",
        (user_id,)
    )
    total = cursor.fetchone()["total"]
    conn.close()
    return total

# =======================================
# FUNÇÕES DE TRANSAÇÕES (TRANSACTIONS)
# =======================================
def _atualizar_saldo(conn, account_id, delta):
    """Aplica delta ao saldo da conta dentro de uma transação"""
    conn.execute(
        "UPDATE accounts SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (delta, account_id)
    )

def depositar(account_id, user_id, amount, category="Depósito", description=""):
    """Registra um depósito e credita o saldo da conta"""
    if amount <= 0:
        return False, "Valor deve ser maior que zero."
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (account_id, user_id, transaction_type, category, amount, description, transaction_date)
            VALUES (?, ?, 'Depósito', ?, ?, ?, ?)
        """, (account_id, user_id, category, amount, description, datetime.now()))
        _atualizar_saldo(conn, account_id, amount)
        conn.commit()
        log_audit(user_id, "DEPOSIT", f"Depósito de {amount}")
        return True, "Depósito realizado com sucesso!"
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao depositar: {str(e)}"
    finally:
        conn.close()

def sacar(account_id, user_id, amount, category="Saque", description=""):
    """Registra um saque, validando saldo suficiente antes de debitar"""
    if amount <= 0:
        return False, "Valor deve ser maior que zero."
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        if row is None:
            return False, "Conta não encontrada."
        if row["balance"] < amount:
            return False, "Saldo insuficiente."
        
        cursor.execute("""
            INSERT INTO transactions (account_id, user_id, transaction_type, category, amount, description, transaction_date)
            VALUES (?, ?, 'Saque', ?, ?, ?, ?)
        """, (account_id, user_id, category, amount, description, datetime.now()))
        _atualizar_saldo(conn, account_id, -amount)
        conn.commit()
        log_audit(user_id, "WITHDRAW", f"Saque de {amount}")
        return True, "Saque realizado com sucesso!"
    except Exception as e:
        conn.rollback()
        return False, f"Erro ao sacar: {str(e)}"
    finally:
        conn.close()

def listar_transacoes(user_id, account_id=None, limit=50):
    """Lista o histórico de transações do usuário"""
    conn = get_db_connection()
    cursor = conn.cursor()
    if account_id:
        cursor.execute("""
            SELECT t.id, t.transaction_type, t.category, t.amount, t.description, t.transaction_date, a.account_name
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            WHERE t.user_id = ? AND t.account_id = ?
            ORDER BY t.transaction_date DESC
            LIMIT ?
        """, (user_id, account_id, limit))
    else:
        cursor.execute("""
            SELECT t.id, t.transaction_type, t.category, t.amount, t.description, t.transaction_date, a.account_name
            FROM transactions t
            JOIN accounts a ON a.id = t.account_id
            WHERE t.user_id = ?
            ORDER BY t.transaction_date DESC
            LIMIT ?
        """, (user_id, limit))
    transacoes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return transacoes
