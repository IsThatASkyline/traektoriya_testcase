from math import radians, cos, sin, asin, sqrt
import json

import requests

from models.convertors import convert_vehicle_json_to_model, convert_vehicle_model_to_json
from models.vehicle import Vehicle
from utils.params import FilterParams


class VehicleManager:
    def __init__(self, url: str):
        self.db_url = url

    def get_vehicles(self) -> list[Vehicle]:
        try:
            r = requests.get(f"{self.db_url}/vehicles")
            vehicle_list = [convert_vehicle_json_to_model(vehicle) for vehicle in json.loads(r.text)]
            return vehicle_list
        except Exception as ex:
            print("Error occurred while get_vehicles:", ex)

    def get_vehicle_by_id(self, id: int) -> Vehicle:
        try:
            r = requests.get(f"{self.db_url}/vehicles/{id}")
            vehicle = convert_vehicle_json_to_model(json.loads(r.text))
            return vehicle
        except Exception as ex:
            print("Error occurred while get_vehicle_by_id:", ex)

    def filter_vehicles(self, params: FilterParams) -> list[Vehicle]:
        vehicles = self.get_vehicles()
        try:
            filters = {(k, v) for k, v in params.items()}
            filtered_vehicles = []
            for vehicle in vehicles:
                if filters.issubset(vehicle.get_params_set()):
                    filtered_vehicles.append(vehicle)
            return filtered_vehicles
        except Exception as ex:
            print("Error occurred while filter_vehicles:", ex)

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        try:
            requests.post(f"{self.db_url}/vehicles", json=convert_vehicle_model_to_json(vehicle))
            return vehicle
        except Exception as ex:
            print("Error occurred while add_vehicle", ex)

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        try:
            requests.put(f"{self.db_url}/vehicles/{vehicle.id}", json=convert_vehicle_model_to_json(vehicle))
            return vehicle
        except Exception as ex:
            print("Error occurred while update_vehicle", ex)

    def delete_vehicle(self, id: int):
        try:
            requests.delete(f"{self.db_url}/vehicles/{id}")
        except Exception as ex:
            print("Error occurred while delete_vehicle", ex)

    def get_distance(self, id1: int, id2: int) -> float:
        vehicle_1 = self.get_vehicle_by_id(id1)
        vehicle_2 = self.get_vehicle_by_id(id2)
        try:
            return self._get_distance(vehicle_1=vehicle_1, vehicle_2=vehicle_2)
        except Exception as ex:
            print("Error occurred while get_distance", ex)

    def get_nearest_vehicle(self, id: int) -> Vehicle:
        vehicles = self.get_vehicles()
        try:
            target_vehicle = [vehicle for vehicle in vehicles if vehicle.id == id][0]
            other_vehicles = [vehicle for vehicle in vehicles if vehicle.id != id]
            nearest_distance = None
            nearest_vehicle = None

            for vehicle in other_vehicles:
                if not nearest_distance:
                    nearest_distance = self._get_distance(vehicle_1=target_vehicle, vehicle_2=vehicle)
                    nearest_vehicle = vehicle
                elif distance := self._get_distance(vehicle_1=target_vehicle, vehicle_2=vehicle) < nearest_distance:
                    nearest_distance = distance
                    nearest_vehicle = vehicle

            return nearest_vehicle
        except Exception as ex:
            print("Error occurred while get_nearest_vehicle", ex)

    @staticmethod
    def _get_distance(vehicle_1: Vehicle, vehicle_2: Vehicle) -> float:
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [vehicle_1.longitude, vehicle_1.latitude,
                                               vehicle_2.longitude, vehicle_2.latitude])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r * 1000
