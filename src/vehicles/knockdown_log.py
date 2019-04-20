from road_vehicle import LogTruck, DieselRoadVehicle

consist = LogTruck(id='knockdown_log',
                   base_numeric_id=250,
                   name='Knockdown',
                   road_type='HAUL',
                   power=250,  # custom power
                   speed=50,
                   vehicle_life=40,
                   gen=4,
                   intro_date=1950)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=30,
                 vehicle_length=7)

consist.add_unit(capacity=30,
                 vehicle_length=6)
