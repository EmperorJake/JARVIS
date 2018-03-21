from road_vehicle import MailHauler

consist = MailHauler(id='foxley_mail',
                     base_numeric_id=190,
                     name='Foxley [Courier Tram]',
                     tram_type='ELRL',
                     power=240,  # custom HP
                     vehicle_life=40,
                     intro_date=1903)

consist.add_unit(capacity=15,
                 vehicle_length=4,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

