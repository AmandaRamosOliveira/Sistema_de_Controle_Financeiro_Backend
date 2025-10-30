from flask import Blueprint, request, jsonify
from models.relatorio import RelatorioModel

relatorio_routes = Blueprint("relatorio_routes", __name__)

@relatorio_routes.route("/relatorio/<int:id_usuario>/<int:mes>/<int:ano>", methods=["GET"])
def gerar_relatorio(id_usuario, mes, ano):
    try:
        from database import get_db
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT salario FROM usuario WHERE id_usuario = %s", (id_usuario,))
        user = cursor.fetchone()
        salario = float(user['salario']) if user else 0.0
        conn.close()

        relatorio = RelatorioModel.obter_relatorio(id_usuario, mes, ano, salario)
        return jsonify(relatorio)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@relatorio_routes.route("/relatorio/anual/<int:id_usuario>/<int:ano>", methods=["GET"])
def relatorio_anual(id_usuario, ano):
    try:
        relatorio_anual = RelatorioModel.obter_relatorio_anual(id_usuario, ano)
        return jsonify(relatorio_anual)
    except Exception as e:
        return jsonify({"erro:": str(e)}), 500