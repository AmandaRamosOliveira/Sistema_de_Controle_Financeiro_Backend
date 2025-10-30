from flask import Blueprint, request, jsonify
import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import usuario
from database import get_db

usuario_routes = Blueprint("usuario_routes", __name__)

@usuario_routes.route("/criarCadastro", methods=["POST"])
def criar_cadastro():
    dados = request.json
    senha = dados["senha"].encode("utf-8")
    senha_hash = bcrypt.hashpw(senha, bcrypt.gensalt()).decode("utf-8")

    usuario.criar_usuario(dados["nome"], dados["email"], dados["telefone"], dados["salario"], senha_hash)
    return jsonify({"Mensagem": "Usuário adicionado com sucesso!"})

@usuario_routes.route("/login", methods=["POST"])
def login():
    dados = request.json
    email = dados["email"]
    senha_usuario = dados["senha"].encode("utf-8")

    user = usuario.buscar_usuario_por_email(email)

    if user and bcrypt.checkpw(senha_usuario, user[3].encode("utf-8")):
        return jsonify({
            "Mensagem": "Login feito com sucesso!",
            "Usuario": {
                "id": user[0],
                "nome": user[1],
                "email": user[2]
            }
        })
    else:
        return jsonify({"Mensagem": "Email ou senha incorretos"}), 401

@usuario_routes.route("/usuario/<int:id_usuario>", methods=["GET"])
def get_usuario(id_usuario):
    user = usuario.buscar_usuario_por_id(id_usuario)
    if user:
        return jsonify(user)
    return jsonify({"Mensagem": "Usuário não encontrado"}), 404

@usuario_routes.route("/usuario/<int:id_usuario>/salario", methods=["GET"])
def get_salario_usuario(id_usuario):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        query = "select salario from usuario where id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@usuario_routes.route("/usuario/<int:id_usuario>/nome", methods=["PUT"])
def trocar_nome(id_usuario):
    try:
        data = request.get_json()
        novo_nome = data.get("nome")

        if not novo_nome:
            return jsonify({"error": "Nome não fornecido"}), 400

        conn = get_db()
        cursor = conn.cursor()
        query = "UPDATE usuario SET nome = %s WHERE id_usuario = %s"
        cursor.execute(query, (novo_nome, id_usuario))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"Mensagem": "Nome atualizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@usuario_routes.route("/usuario/<int:id_usuario>/senha", methods=["PUT"])
def trocar_senha(id_usuario):
    try:
        data = request.get_json()
        nova_senha = data.get("senha")

        if not nova_senha:
            return jsonify({"error": "Senha não fornecida"}), 400

        senha_hash = bcrypt.hashpw(nova_senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        conn = get_db()
        cursor = conn.cursor()
        query = "UPDATE usuario SET senha = %s WHERE id_usuario = %s"
        cursor.execute(query, (senha_hash, id_usuario))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"Mensagem": "Senha atualizada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@usuario_routes.route('/verificar-email', methods=['POST'])
def verificar_email():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({"erro": "Email não fornecido"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("select * from usuario where email = %s", (email,))
    usuario_existente = cursor.fetchone()
    
    if usuario_existente:
        return jsonify({"existe": True, "Mensagem": "Email já cadastrado"})
    else:
        return jsonify({"existe": False, "Mensagem": "Email disponível"})
    
@usuario_routes.route('/esqueceu-senha', methods=['PUT'])
def esqueceu_senha():
    data = request.get_json()
    email = data.get('email')
    nova_senha = data.get('senha')

    if not email or not nova_senha:
        return jsonify({"erro": "Email e nova senha são obrigatórios"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
    usuario_existente = cursor.fetchone()

    if not usuario_existente:
        cursor.close()
        db.close()
        return jsonify({"erro": "Email não cadastrado"}), 404

    senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor.execute("UPDATE usuario SET senha = %s WHERE email = %s", (senha_hash, email))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"Mensagem": "Senha atualizada com sucesso!"}), 200
