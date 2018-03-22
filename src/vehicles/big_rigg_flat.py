from road_vehicle import FlatHauler

consist = FlatHauler(id='big_rigg_flat',
                        base_numeric_id=660,
                        name='Big Rigg',
                        vehicle_life=40,
                        intro_date=1997)

consist.add_unit(capacity=20,
                 vehicle_length=5,
                 cargo_length=3,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=20,
                 vehicle_length=4,
                 cargo_length=4)
