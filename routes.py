from flask import Blueprint, request, jsonify
from models import db, Driver

#Blueprint lets us organize routes into modular files.
bp = Blueprint("driver_bp", __name__)

#/register – Add a driver






@bp.route("/register", methods=["POST"])
def register_driver():
    #Receives a JSON like { "name": "John", "license_number": "DL123" }
    data = request.get_json() 
    #Checks if driver with same license already exists
    if Driver.query.filter_by(license_number=data["license_number"]).first():
        return jsonify({"message": "Driver already registered"}), 400
    
    0#If not, adds to DB and returns 201 Created
    driver = Driver(
        name=data["name"],
        license_number=data["license_number"],
        available=data.get("available", True)
    )
    db.session.add(driver)
    db.session.commit()
    return jsonify({"message": "Driver registered"}), 201

#/drivers – Get all drivers
@bp.route("/drivers", methods=["GET"])
def list_drivers():
    #Reads all drivers from DB
    drivers = Driver.query.all()
    #Returns a JSON list
    return jsonify([{
        "id": d.id,
        "name": d.name,
        "license_number": d.license_number,
        "available": d.available
    } for d in drivers])
