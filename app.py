from flask import Flask
from routes import search_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
# register routes
app.register_blueprint(search_routes)

if __name__ == '__main__':
    app.run(debug=True)
