from flask import Flask #API handling
from flask_jwt_extended import JWTManager
from models import db
from routes import bp
from config import DB_URI, JWT_SECRET

app = Flask(__name__)
#Configure Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET

#Initialize and create DB 
#This will create the drivers table if it doesn’t exist.
db.init_app(app)
with app.app_context():
    db.create_all()

#Register Blueprint and JWT
JWTManager(app)
app.register_blueprint(bp)

#Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
