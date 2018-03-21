from road_vehicle import MailHauler

consist = MailHauler(id='singing_river_mail',
                     base_numeric_id=850,
                     name='Singing River [Courier Tram]',
                     tram_type='ELRL',
                     power=600,
                     vehicle_life=40,
                     intro_date=1990)

consist.add_unit(capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

