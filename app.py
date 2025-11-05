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

origem_front = "https://sistema-de-controle-financeiro-fron.vercel.app"

CORS(
    app,
    origins=[origem_front],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Rotas
app.register_blueprint(usuario_routes, url_prefix="/api")
app.register_blueprint(contas_routes, url_prefix="/api")
app.register_blueprint(metas_routes, url_prefix="/api")
app.register_blueprint(relatorio_routes, url_prefix="/api")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
