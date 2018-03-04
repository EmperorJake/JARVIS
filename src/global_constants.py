from polar_fox import base_refits_by_class, cargo_labels, disallowed_refits_by_label, chameleon_cache_dir, generated_files_dir, graphics_path, mail_multiplier, max_game_date

# capacity multipliers for capacity parameter
capacity_multipliers = (0.67, 1, 1.33)

grfid = r"\97\87\EA\FE"

# cargo aging constant - OTTD default is 185
CARGO_AGE_PERIOD = 185

# cost constants
FIXED_RUN_COST = 500.0
FUEL_RUN_COST = 10.0

# standard offsets for vehicle
# 3/8, 4/8, 5/8, 6/8, 7/8 and 8/8 were adjusted June 2016, tested, all looked correct
default_road_vehicle_offsets = {'1': ((-6, -23), (0, -17), (12, -10), (6, -11), (-6, -12), (-14, -10), (-14, -10), (-8, -16)), # may need fix
                                '2': ((-6, -23), (-2, -16), (8, -10), (4, -11), (-6, -12), (-14, -10), (-16, -10), (-8, -14)),
                                '3': ((-6, -22), (-4, -15), (2, -10), (2, -11), (-6, -15), (-14, -10), (-14, -10), (-8, -15)),
                                '4': ((-6, -20), (-6, -14), (0, -10), (0, -11), (-6, -12), (-14, -10), (-14, -10), (-8, -14)),
                                '5': ((-6, -17), (-8, -13), (-6, -10), (-2, -11), (-6, -12), (-14, -10), (-14, -10), (-8, -13)),
                                '6': ((-6, -16), (-10, -12), (-8, -10), (-4, -11), (-6, -15), (-14, -10), (-14, -10), (-8, -12)),
                                '7': ((-6, -15), (-12, -11), (-14, -10), (-6, -11), (-6, -15), (-14, -10), (-14, -10), (-8, -11)),
                                '8': ((-6, -13), (-14, -10), (-18, -10), (-8, -11), (-6, -13), (-14, -10), (-14, -10), (-8, -10))}

semi_truck_offset_jank = ((0, 1), (-2, 1), (-5, 0), (-2, 1), (0, 0), (-2, 1), (-1, 0), (-1, 1))

# spritesheet bounding boxes, each defined by a 3 tuple (left x, width, height);
# upper y is determined by spritesheet row position, so isn't defined as a constant
spritesheet_bounding_boxes = ((60, 12, 24), (92, 26, 20), (124, 36, 16), (172, 26, 20),
                              (204, 12, 24), (236, 26, 20), (268, 36, 16), (316, 26, 20))

buy_menu_sprite_width = 36 # 36 is correct, but some spritesheets might have wrong widths due to copy-pasteo etc
buy_menu_sprite_height = 16

