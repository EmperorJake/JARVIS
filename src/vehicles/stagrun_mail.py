from road_vehicle import MailHauler

consist = MailHauler(id='stagrun_mail',
                     base_numeric_id=840,
                     name='Stagrun [Courier Tram]',
                     tram_type='ELRL',
                     power=360,  # custom power
                     vehicle_life=40,
                     intro_date=1932)

consist.add_unit(capacity=18,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

