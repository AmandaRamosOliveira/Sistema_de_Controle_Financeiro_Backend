from flask import Blueprint, request, jsonify
from models import contas 

contas_routes = Blueprint("contas_routes", __name__)

@contas_routes.route("/contas", methods=["POST"])
def adicionar_conta_route():
    try:
        data = request.get_json()
        conta = contas.adicionar_conta(data)
        return jsonify({"conta": conta}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@contas_routes.route("/contas", methods=["GET"])
def listar_contas_route():
    try:
        return jsonify(contas.listar_contas()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@contas_routes.route("/contas/usuario/<int:id_usuario>", methods=["GET"])
def listar_contas_por_usuario_route(id_usuario):
    try:
        mes = request.args.get("mes")
        ano = request.args.get("ano")
        return jsonify(contas.listar_contas_por_usuario(id_usuario, mes, ano)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
