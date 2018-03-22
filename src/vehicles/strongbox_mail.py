from road_vehicle import MailHauler

consist = MailHauler(id='strongbox_mail',
                     base_numeric_id=830,
                     name='Strongbox',
                     tram_type='ELRL',
                     power=480,  # custom power
                     vehicle_life=40,
                     intro_date=1961)

consist.add_unit(capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

