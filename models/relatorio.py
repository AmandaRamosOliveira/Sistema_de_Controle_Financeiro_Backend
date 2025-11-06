from database import get_db

class RelatorioModel:
    @staticmethod
    def obter_relatorio(id_usuario, mes, ano, salario):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query_contas = """
            SELECT categoria, SUM(valor) AS total_categoria
            FROM conta
            WHERE id_usuario = %s AND mes = %s AND ano = %s
            GROUP BY categoria
        """
        cursor.execute(query_contas, (id_usuario, mes, ano))
        contas = cursor.fetchall()

        total_gasto = sum([float(c['total_categoria']) for c in contas]) if contas else 0.0

        maior_gasto = max(
            contas, key=lambda c: c['total_categoria'],
            default={'categoria': None, 'total_categoria': 0}
        )
        maior_gasto_valor = float(maior_gasto['total_categoria']) if maior_gasto else 0.0

        query_meta = """
           SELECT 
            SUM(
            CASE
                WHEN status = 'pendente' THEN valor
                WHEN status = 'concluida' AND mes_conclusao = %s AND ano_conclusao = %s THEN valor_final
                ELSE 0
                END
               ) AS total_meta
               FROM Meta
               WHERE id_usuario = %s
             """
        cursor.execute(query_meta, (mes, ano, id_usuario))
        meta = cursor.fetchone()


        valor_meta = float(meta['total_meta']) if meta and meta['total_meta'] else 0.0
        economia = max((salario - total_gasto) + valor_meta, 0.0)

        conn.close()

        return {
            "mes": mes,
            "ano": ano,
            "salario":salario,
            "total_gasto": total_gasto,
            "maior_gasto": {
                "categoria": maior_gasto['categoria'],
                "valor": maior_gasto_valor
            },
            "economia": economia,
            "categorias": contas
        }

    @staticmethod
    def obter_relatorio_anual(id_usuario, ano):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        query_mensal = """
            SELECT mes, SUM(valor) AS total_mes
            FROM conta
            WHERE id_usuario = %s AND ano = %s
            GROUP BY mes
            ORDER BY mes
        """
        cursor.execute(query_mensal, (id_usuario, ano))
        gastos_mensais = cursor.fetchall()

        query_categoria = """
            SELECT categoria, SUM(valor) AS total_categoria
            FROM conta
            WHERE id_usuario = %s AND ano = %s
            GROUP BY categoria
        """
        cursor.execute(query_categoria, (id_usuario, ano))
        categorias = cursor.fetchall()

        total_gasto_anual = sum([float(c['total_categoria']) for c in categorias]) if categorias else 0.0
        maior_categoria = max(
            categorias, key=lambda c: c['total_categoria'],
            default={'categoria': None, 'total_categoria': 0}
        )
        maior_categoria_valor = float(maior_categoria['total_categoria']) if maior_categoria else 0.0


        if gastos_mensais:
            mes_mais_gasto = max(gastos_mensais, key=lambda g: g['total_mes'])
            mes_mais_gasto_num = mes_mais_gasto['mes']
            total_mes_mais_gasto = float(mes_mais_gasto['total_mes'])
        else:
            mes_mais_gasto_num = None
            total_mes_mais_gasto = 0.0

        conn.close()

        return {
            "ano": ano,
            "total_gasto_anual": total_gasto_anual,
            "categoria_mais_gasta": {
                "categoria": maior_categoria['categoria'],
                "valor": maior_categoria_valor
            },
            "gastos_mensais": gastos_mensais,
            "categorias": categorias,
            "mes_mais_gasto": {
                "numero": mes_mais_gasto_num,
                "valor": total_mes_mais_gasto
            }
        }
