import global_constants
from road_vehicle import RVConsist, LivestockHauler

consist = RVConsist(id = 'cowsleigh',
              base_numeric_id = 900,
              title = 'Cowsleigh [Livestock Truck]',
              replacement_id = '-none',
              vehicle_life = 40,
              intro_date = 1911)

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 15,
                        capacity = 0,
                        vehicle_length = 4,
                        visual_effect = 'VISUAL_EFFECT_STEAM',
                        spriterow_num = 0))

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 8,
                        capacity = 12,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 8,
                        capacity = 12,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
