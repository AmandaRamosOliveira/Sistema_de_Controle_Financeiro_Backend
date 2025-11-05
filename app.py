from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from routes.usuario import usuario_routes
from routes.contas import contas_routes
from routes.metas import metas_routes
from routes.relatorio import relatorio_routes

load_dotenv()

app = Flask(__name__)


CORS(
    app,
    supports_credentials=True,
    origins=["https://sistema-de-controle-financeiro-fron.vercel.app"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

app.register_blueprint(usuario_routes, url_prefix="/api")
app.register_blueprint(contas_routes, url_prefix="/api")
app.register_blueprint(metas_routes, url_prefix="/api")
app.register_blueprint(relatorio_routes, url_prefix="/api")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
