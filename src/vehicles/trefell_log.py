from road_vehicle import LogHauler

consist = LogHauler(id='trefell_log',
                    base_numeric_id=480,
                    name='Trefell [Logging Truck]',
                    road_type='HAUL',
                    power=100,  # custom power
                    vehicle_life=40,
                    intro_date=1910)

consist.add_unit(capacity=0,
                 vehicle_length=4,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=40,
                 vehicle_length=6)

