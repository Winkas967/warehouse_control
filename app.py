import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from routes.product_controller import product_route
from routes.contributor_controller import contributor_route
from routes.sector_controller import sector_route
from routes.transaction_controller import transaction_route
from routes.auth_controller import auth_route
from routes.report_controller import report_route

app = Flask(__name__, static_folder="static", static_url_path="/static")

app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(product_route)
app.register_blueprint(contributor_route)
app.register_blueprint(sector_route)
app.register_blueprint(transaction_route)
app.register_blueprint(auth_route)
app.register_blueprint(report_route)


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/entrar")
def login_page():
    return app.send_static_file("login.html")


@app.errorhandler(Exception)
def handle_error(e):
    # Sempre responde JSON, para o frontend conseguir mostrar a mensagem
    if isinstance(e, HTTPException):
        return jsonify({"message": e.description}), e.code
    return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    # host 0.0.0.0 para o tablet acessar pela rede; debug só com FLASK_DEBUG=1
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)),
            debug=os.getenv("FLASK_DEBUG") == "1")
