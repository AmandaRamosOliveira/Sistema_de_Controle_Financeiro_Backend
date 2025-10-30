from database import get_db

def criar_usuario(nome, email, telefone, salario, senha_hash):
    conn = get_db()
    cursor = conn.cursor()
    query = "INSERT INTO Usuario (nome, email, telefone, salario, senha) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nome, email, telefone, salario, senha_hash))
    conn.commit()
    cursor.close()
    conn.close()

def buscar_usuario_por_email(email):
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT id_usuario, nome, email, senha FROM Usuario WHERE email = %s"
    cursor.execute(query, (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def buscar_usuario_por_id(id_usuario):   
    conn = get_db()
    cursor = conn.cursor(dictionary=True)  
    query = "SELECT id_usuario, nome, email, telefone, salario FROM Usuario WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def trocar_nome(id_usuario, novo_nome):
    conn = get_db()
    cursor = conn.cursor()
    query = "update Usuario set nome = %s WHERE id_usuario = %s"
    cursor.execute(query,(novo_nome, id_usuario))
    conn.commit()
    conn.close()
    
def trocar_senha(id_usuario, nova_senha):
    conn = get_db()
    cursor = conn.cursor()
    query = "update usuario set senha = %s where id_usuario = %s"
    cursor.execute(query, (nova_senha, id_usuario))
    conn.commit()
    conn.close()
    
def esqueceu_senha(email, nova_senha):
    conn = get_db()
    cursor = conn.cursor()
    query = "UPDATE usuario SET senha = %s WHERE email = %s"
    cursor.execute(query, (nova_senha, email))
    conn.commit()
    conn.close()
