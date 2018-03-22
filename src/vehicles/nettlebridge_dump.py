from road_vehicle import DumpHauler

consist = DumpHauler(id='nettlebridge_dump',
                     base_numeric_id=310,
                     name='Nettlebridge',
                     tram_type='ELRL',
                     vehicle_life=40,
                     intro_date=1944)

consist.add_unit(capacity=0,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=36,
                 vehicle_length=6,
                 repeat=2)
