from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id='beerwoods_edibles_tanker',
                        base_numeric_id=420,
                        name='Beerwoods',
                        vehicle_life=40,
                        intro_date=1943)

consist.add_unit(capacity=15,
                 vehicle_length=5,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=15,
                 vehicle_length=4)

