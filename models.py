from flask_sqlalchemy import SQLAlchemy #ORM

#sets up ORM engine
db = SQLAlchemy()

#The Driver class maps to a PostgreSQL table called drivers
class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True) #auto-generated primary key
    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False) #unique license_number ID
    available = db.Column(db.Boolean, default=True) #whether the driver is currently available
