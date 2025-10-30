from database import get_db

def adicionar_conta(data):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = """
        INSERT INTO conta (categoria, valor, tipo, mes, ano, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        data["categoria"],
        data["valor"],
        data["tipo"],
        data["mes"],
        data["ano"],
        data["id_usuario"],
    )

    cursor.execute(query, values)
    conn.commit()
    nova_conta_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "id": nova_conta_id,
        "categoria": data["categoria"],
        "valor": data["valor"],
        "tipo": data["tipo"],
        "mes": data["mes"],
        "ano": data["ano"],
        "id_usuario": data["id_usuario"],
    }


def listar_contas():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM conta")
    contas = cursor.fetchall()
    cursor.close()
    conn.close()
    return contas


def listar_contas_por_usuario(id_usuario, mes=None, ano=None):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM conta WHERE id_usuario = %s"
    values = [id_usuario]

    if mes and ano:
        query += " AND mes = %s AND ano = %s"
        values.extend([mes, ano])

    cursor.execute(query, tuple(values))
    contas = cursor.fetchall()

    cursor.close()
    conn.close()
    return contas
