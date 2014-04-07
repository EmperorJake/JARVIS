import global_constants
from road_vehicle import EngineConsist, MiningHauler

consist = EngineConsist(id = 'witch_hill',
              base_numeric_id = 340,
              title = 'Witch Hill [Mining Truck]',
              replacement_id = '-none',
              power = 1200,
              speed = 50,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1989,
              graphics_status = '')

consist.add_unit(MiningHauler(consist = consist,
                        weight = 60,
                        capacity_freight = 100,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
