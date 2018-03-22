from road_vehicle import EdiblesTanker

consist = EdiblesTanker(id='flow_edge_edibles_tanker',
                        base_numeric_id=930,
                        name='Flow Edge',
                        vehicle_life=40,
                        intro_date=1912)

consist.add_unit(capacity=12,
                 vehicle_length=5,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=12,
                 vehicle_length=4)

