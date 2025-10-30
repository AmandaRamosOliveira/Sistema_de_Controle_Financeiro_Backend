from flask import Blueprint, request, jsonify
from models import metas 

metas_routes = Blueprint("metas_routes", __name__)

@metas_routes.route("/metas", methods=["POST"])
def adicionar_meta_route():
    try:
        data = request.get_json()
        meta = metas.adicionar_meta(data)
        return jsonify({"meta": meta}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@metas_routes.route("/metas", methods=["GET"])
def listar_metas_route():
    try:
        return jsonify(metas.listar_metas()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@metas_routes.route("/metas/usuario/<int:id_usuario>", methods=["GET"])
def listar_metas_por_usuario_route(id_usuario):
    try:
        return jsonify(metas.listar_metas_por_usuario(id_usuario)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@metas_routes.route("/metas/<int:id_meta>/status", methods=["PUT"])
def atualizar_status_route(id_meta):
    try:
        novo_status = request.json.get("status")
        if novo_status not in ["pendente", "concluida"]:
            return jsonify({"error": "Status inválido"}), 400
        
        metas.atualizar_status(id_meta, novo_status)
        return jsonify({"message": "Status atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
