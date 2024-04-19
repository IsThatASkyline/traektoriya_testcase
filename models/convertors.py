import json

from models.vehicle import Vehicle


def convert_vehicle_json_to_model(data: dict):
    return Vehicle(
        id=data["id"],
        name=data["name"],
        model=data["model"],
        year=data["year"],
        color=data["color"],
        price=data["price"],
        latitude=data["latitude"],
        longitude=data["longitude"]
    )


def convert_vehicle_model_to_json(vehicle: Vehicle):
    return json.dumps(vehicle.to_dict())
