from database import get_db
import math
from datetime import datetime

def adicionar_meta(data):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    descricaoMeta = data["descricaoMeta"]
    valor = float(data["valorMensal"])
    valor_final = float(data["valorFinal"])
    id_usuario = data["id_usuario"]
    
    periodo_meses = math.ceil(valor_final / valor) if valor > 0 else 0

    query = """INSERT INTO meta (descricaoMeta, valor, valor_final, periodo_meses, id_usuario)
               VALUES (%s, %s, %s, %s, %s)"""
    values = (descricaoMeta, valor, valor_final, periodo_meses, id_usuario)

    cursor.execute(query, values)
    conn.commit()

    nova_meta_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "id_meta": nova_meta_id,
        "descricaoMeta": descricaoMeta,
        "valor": valor,
        "valor_final": valor_final,
        "periodo_meses": periodo_meses,
        "id_usuario": id_usuario
    }


def listar_metas():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM meta")
    metas = cursor.fetchall()
    cursor.close()
    conn.close()
    return metas


def listar_metas_por_usuario(id_usuario):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM meta WHERE id_usuario = %s", (id_usuario,))
    metas = cursor.fetchall()
    cursor.close()
    conn.close()
    return metas


def atualizar_status(id_meta, novo_status):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if novo_status == "concluida":
        agora = datetime.now()
        mes_conclusao = agora.month
        ano_conclusao = agora.year
        
        query =  """
            UPDATE meta
            SET status = %s, mes_conclusao = %s, ano_conclusao = %s
            WHERE id_meta = %s
        """
        cursor.execute(query, (novo_status,mes_conclusao, ano_conclusao, id_meta))
    else:
        query= """UPDATE meta
                  SET status = %s, mes_conclusao = NULL, ano_conclusao= NULL
                  WHERE id_meta = %s"""
        cursor.execute(query,(novo_status, id_meta))
    conn.commit()
    cursor.close()
    conn.close()
