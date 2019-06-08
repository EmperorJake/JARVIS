from road_vehicle import FlatbedTramConsist, ElectricVehicleUnit

consist = FlatbedTramConsist(id='rackwood_flat',
                      base_numeric_id=740,
                      name='Rackwood',
                         vehicle_life=40,
                      gen=2)

consist.add_unit(type=ElectricVehicleUnit,
                 capacity=30,
                 vehicle_length=8,
                 cargo_length=3,
                 repeat=2)
