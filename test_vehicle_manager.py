from vehicle_manager import VehicleManager, Vehicle


def main():
    manager = VehicleManager(url="https://test.tspb.su/test-task")
    print(manager.get_vehicles())  # [<Vehicle: Toyota Camry 2021 red 21000>, ...]
    print(manager.filter_vehicles(params={"name": "Toyota"}))  # [<Vehicle: Toyota Camry 2021 red 21000>]
    print(manager.get_vehicle_by_id(1))  # <Vehicle: Toyota Camry 2021 red 21000>
    print(manager.add_vehicle(  # <Vehicle: Toyota Camry 2021 red 21000>
        vehicle=Vehicle(
            name='Toyota',
            model='Camry',
            year=2021,
            color='red',
            price=21000,
            latitude=55.753215,
            longitude=37.620393,
        )
    ))
    print(manager.update_vehicle(  # <Vehicle: Toyota Camry 2021 red 21000>
        vehicle=Vehicle(
            id=1,
            name='Toyota',
            model='Camry',
            year=2021,
            color='red',
            price=21000,
            latitude=55.753215,
            longitude=37.620393
        )
    ))
    manager.delete_vehicle(id=1)
    print(manager.get_distance(id1=1, id2=2))  # 638005.0864183258
    print(manager.get_nearest_vehicle(id=1))


if __name__ == "__main__":
    main()
