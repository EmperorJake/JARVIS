from road_vehicle import BoxTruck, DieselRoadVehicle

consist = BoxTruck(id='quickset_box',
                   base_numeric_id=350,
                   name='Quickset',
                   semi_truck_so_redistribute_capacity=True,
                   vehicle_life=40,
                   gen=4)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=40,
                 vehicle_length=7)
