import global_constants
from road_vehicle import DumpHauler

consist = DumpHauler(id = 'nettlebridge',
                base_numeric_id = 310,
                title = 'Nettlebridge [Dump Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1944)

consist.add_unit(weight = 15,
                capacity = 0,
                vehicle_length = 4,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                always_use_same_spriterow = True)

consist.add_unit(weight = 10,
                capacity = 36,
                vehicle_length = 6,
                repeat = 2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=consist.graphics_processors[0])
