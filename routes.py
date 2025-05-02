from flask import Blueprint, request, jsonify
from models import db, Driver
from flask_jwt_extended import jwt_required
from config import BOOKING_SERVICE_URL
import requests

#Blueprint lets us organize routes into modular files.
bp = Blueprint("driver_bp", __name__)

#/register – Add a driver
@bp.route("/register", methods=["POST"])
@jwt_required()
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

# /drivers – Get all drivers list
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

''''
Fetch active bookings
Build a set of booked driver_ids
Show only free drivers.
'''
@bp.route('/free-drivers', methods=['GET'])
@jwt_required()
def free_drivers():
    all_drivers = Driver.query.all()
    response = requests.get(f"{BOOKING_SERVICE_URL}/active-bookings", timeout=5)
    
    if response.status_code != 200:
        return jsonify({"error": "Could not fetch bookings"}), 500

    bookings = response.json()
    booked_driver_ids = {b["driver_id"] for b in bookings}

    free_drivers = []
    for driver in all_drivers:
        if driver.id not in booked_driver_ids:
            free_drivers.append({
                "id": driver.id,
                "name": driver.name,
                "license_number": driver.license_number
            })

    return jsonify(free_drivers)

# GET /drivers/<id>
@bp.route("/drivers/<int:driver_id>", methods=["GET"])
def get_driver_by_id(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404
    return jsonify(driver.to_dict())
