import global_constants
from road_vehicle import RVConsist, BoxHauler

consist = RVConsist(vehicle_type = BoxHauler,
                id = 'runwell',
                base_numeric_id = 890,
                title = 'Runwell [Open Truck]',
                replacement_id = '-none',
                semi_truck_so_redistribute_capacity = True,
                vehicle_life = 40,
                intro_date = 1910)

consist.add_unit(weight = 6,
                capacity = 0,
                vehicle_length = 2,
                semi_truck_shift_offset_jank = 2,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                always_use_same_spriterow = True)

consist.add_unit(weight = 6,
                capacity = 24,
                vehicle_length = 5)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
