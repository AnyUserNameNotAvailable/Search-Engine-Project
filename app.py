from flask import Flask
from routes import search_routes

app = Flask(__name__)

# register routes
app.register_blueprint(search_routes)

if __name__ == '__main__':
    app.run(debug=True)
