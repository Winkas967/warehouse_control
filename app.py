from flask import Flask
from routes.product_controller import product_route
from routes.contributor_controller import contributor_route
from routes.sector_controller import sector_route
from routes.transaction_controller import transaction_route

app = Flask(__name__)

app.register_blueprint(product_route)
app.register_blueprint(contributor_route)
app.register_blueprint(sector_route)
app.register_blueprint(transaction_route)

app.run(debug = True)