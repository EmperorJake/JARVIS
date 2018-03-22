from road_vehicle import BoxHauler

consist = BoxHauler(id='easywheal_box',
                    base_numeric_id=160,
                    name='Easywheal',
                    semi_truck_so_redistribute_capacity=True,
                    vehicle_life=40,
                    intro_date=1939)

consist.add_unit(capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 visual_effect='VISUAL_EFFECT_DIESEL',
                 always_use_same_spriterow=True)

consist.add_unit(capacity=30,
                 vehicle_length=5)


