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

CORS(app, 
     resources={r"/api/*": {"origins": ["https://sistema-de-controle-financeiro-fron.vercel.app"]}},
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"])

app.register_blueprint(usuario_routes, url_prefix="/api")
app.register_blueprint(contas_routes, url_prefix='/api')
app.register_blueprint(metas_routes, url_prefix='/api')
app.register_blueprint(relatorio_routes, url_prefix='/api')

@app.before_request
def handle_options():
    from flask import request, make_response
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "https://sistema-de-controle-financeiro-fron.vercel.app")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response
         
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
