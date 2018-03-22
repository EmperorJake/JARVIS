import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

import math
import inspect # only used for deprecated attempt at partial compiles, remove (and vehicle_module_path var)

from chameleon import PageTemplateLoader # chameleon used in most template cases
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, 'src', 'templates'))

import global_constants # expose all constants for easy passing to templates
import utils

from graphics_processor.gestalt_graphics import GestaltGraphics, GestaltGraphicsVisibleCargo, GestaltGraphicsLiveryOnly, GestaltGraphicsCustom
import graphics_processor.graphics_constants as graphics_constants

from rosters import registered_rosters
from vehicles import numeric_id_defender

class Consist(object):
    """
       'Vehicles' (appearing in buy menu) are composed as articulated consists.
       Each consist comprises one or more vehicle 'units'.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.vehicle_module_path = inspect.stack()[2][1]
        # setup properties for this consist (props either shared for all vehicles, or placed on lead vehicle of consist)
        self._name = kwargs.get('name', None) # private as 'name' is an @property method to add type substring
        self.base_numeric_id = kwargs.get('base_numeric_id', None)
        self.road_type = kwargs.get('road_type', None)
        self.tram_type = kwargs.get('tram_type', None)
        if self.road_type is not None and self.tram_type is not None:
            utils.echo_message("Error: " + self.id + ". Vehicles must not have both road_type and tram_type properties set.  Set one of these only")
        self.roadveh_flag_tram = True if self.tram_type is not None else None
        self.intro_date = kwargs.get('intro_date', None)
        self.vehicle_life = kwargs.get('vehicle_life', None)
        self._power = kwargs.get('power', None)
        self._sound_effect = kwargs.get('sound_effect', None)
        # option for multiple default cargos, cascading if first cargo(s) are not available
        self.default_cargos = []
        # semi-trucks need some redistribution of capacity to get correct TE (don't use this of other magic, bad idea)
        self.semi_truck_so_redistribute_capacity = kwargs.get('semi_truck_so_redistribute_capacity', False)
        self._speed = kwargs.get('speed', None)
        self.class_refit_groups = []
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.autorefit = False
        self.loading_speed_multiplier = kwargs.get('loading_speed_multiplier', 1)
        self.cargo_age_period = kwargs.get('cargo_age_period', global_constants.CARGO_AGE_PERIOD)
        # arbitrary adjustments of points that can be applied to adjust buy cost and running cost, over-ride in consist as needed
        # values can be -ve or +ve to dibble specific vehicles (but total calculated points cannot exceed 255)
        self.type_base_buy_cost_points = kwargs.get('type_base_buy_cost_points', 0)
        self.type_base_running_cost_points = kwargs.get('type_base_running_cost_points', 0)
        # multiplier of capacity, used to set consist weight, over-ride in vehicle sub-class as needed
        # set this to the value for road vehicles...trams will be automatically adjusted
        self.weight_multiplier = 0.4
        # create structure to hold the units
        self.units = []
        # create a structure for cargo /livery graphics options
        self.gestalt_graphics = GestaltGraphics()
        # roster is set when the vehicle is registered to a roster, only one roster per vehicle
        self.roster_id = None

    def add_unit(self, repeat=1, **kwargs):
        # how many unique units? (units can be repeated, we are using count for numerid ID, so we want uniques)
        count = len(set(self.units))

        unit = RoadVehicle(consist=self, **kwargs)

        if count == 0:
            unit.id = self.id # first vehicle gets no numeric id suffix - for compatibility with buy menu list ids etc
        else:
            unit.id = self.id + '_' + str(count)
        unit.numeric_id = self.get_and_verify_numeric_id(count)

        if self.semi_truck_so_redistribute_capacity:
            if count == 0 and kwargs.get('capacity', 0) != 0:
                # guard against lead unit having capacity set in declared props (won't break, just wrong)
                utils.echo_message("Error: " + self.id + ".  First unit of semi-truck must have capacity 0")
            if count == 1:
                # semi-trucks need some capacity moved to lead unit to gain sufficient TE
                # this automagically does that, allowing capacities to be defined simply on the trailer in the vehicle definition
                # sometimes a greater good requires a small evil, although this will probably go wrong eh?
                if repeat != 1:
                    # guard against unintended application of this to anything except first trailer
                    utils.echo_message("Error: " + self.id + ".  Semi-truck cannot repeat first trailer in consist")
                specified_capacities = unit.capacities
                unit.capacities = [int(math.floor(0.5 * capacity)) for capacity in specified_capacities]
                self.units[0].capacities = [int(math.ceil(0.5 * capacity)) for capacity in specified_capacities]

        for repeat_num in range(repeat):
            self.units.append(unit)

    @property
    def unique_units(self):
        # units may be repeated in the consist, sometimes we need an ordered list of unique units
        # set() doesn't preserve list order, which matters, so do it the hard way
        unique_units = []
        for unit in self.units:
            if unit not in unique_units:
                unique_units.append(unit)
        return unique_units

    def get_and_verify_numeric_id(self, offset):
        numeric_id = self.base_numeric_id + offset
        # guard against the ID being too large to build in an articulated consist
        if numeric_id > 16383:
            utils.echo_message("Error: numeric_id " + str(numeric_id) + " for " + self.id + " can't be used (16383 is max ID for articulated vehicles)")
        # non-blocking guard on duplicate IDs
        for id in numeric_id_defender:
            if id == numeric_id:
                utils.echo_message("Error: consist " + self.id + " unit id collides (" + str(numeric_id) + ") with units in another consist")
        numeric_id_defender.append(numeric_id)
        return numeric_id

    def get_num_spritesets(self):
        print("remove get_num_spritesets")
        return 1

    def get_str_name_suffix(self):
        # used in vehicle name string only, relies on name property value being in format "Foo [Bar]" for Name [Type Suffix]
        # Iron Horse has a cleaner implementation of this, dropping the [STUFF] faff, getting it from vehicle subclass instead
        type_suffix = self._name.split('[')[1].split(']')[0]
        type_suffix = type_suffix.upper()
        type_suffix = '_'.join(type_suffix.split(' '))
        return 'STR_NAME_SUFFIX_' + type_suffix

    @property
    def name(self):
        return "string(STR_NAME_CONSIST, string(STR_NAME_" + self.id + "), string(" + "STR_EMPTY" + "))"

    def get_spriterows_for_consist_or_subpart(self, units):
        # pass either list of all units in consist, or a slice of the consist starting from front (arbitrary slices not useful)
        # spriterow count is number of output sprite rows from graphics processor, to be used by nml sprite templating
        result = []
        for unit in units:
            unit_rows = []
            if unit.always_use_same_spriterow:
                unit_rows.append(('always_use_same_spriterow', 1))
            else:
                # assumes visible_cargo is used to handle any other rows, no other cases at time of writing, could be changed eh?
                unit_rows.extend(self.gestalt_graphics.get_output_row_counts_by_type())
            result.append(unit_rows)
        return result

    def get_engine_cost_points(self):
        # Up to 20 points for power. 1 point per 100hp
        # Power is therefore capped at 2000hp by design, this isn't a hard limit, but raise a warning
        if self.power > 2000:
            utils.echo_message("Consist " + self.id + " has power > 2000hp, which is too much")
        power_cost_points = self.power / 100

        # Up to 30 points for speed above up to 90mph. 1 point per 3mph
        if self.speed > 90:
            utils.echo_message("Consist " + self.id + " has speed > 90, which is too much")
        speed_cost_points = min(self.speed, 90) / 3

        # Up to 20 points for intro date after 1870. 1 point per 8 years.
        # Intro dates capped at 2030, this isn't a hard limit, but raise a warning
        if self.intro_date > 2030:
            utils.echo_message("Consist " + self.id + " has intro_date > 2030, which is too much")
        date_cost_points = max((self.intro_date - 1870), 0) / 8

        # Up to 20 points for capacity. 1 point per 8t.
        # Capacity capped at 160, this isn't a hard limit, but raise a warning
        if self.total_capacities[1] > 160:
            utils.echo_message("Consist " + self.id + " has capacity > 160, which is too much")
        consist_capacity_points = min(self.total_capacities[1], 160)

        return power_cost_points + speed_cost_points + date_cost_points + consist_capacity_points

    @property
    def buy_cost(self):
        # type_base_buy_cost_points is an arbitrary adjustment that can be applied on a type-by-type basis,
        # there is an arbitrary multiplier applied to get sensible costs in range with Iron Horse
        return 0.5 * self.get_engine_cost_points() + self.type_base_buy_cost_points

    @property
    def running_cost(self):
        # type_base_running_cost_points is an arbitrary adjustment that can be applied on a type-by-type basis,
        return self.get_engine_cost_points()  + self.type_base_running_cost_points

    @property
    def weight(self):
        mult = self.weight_multiplier
        # trams are 10% heavier per capacity
        if self.roadveh_flag_tram:
            mult = mult + 0.1
        consist_weight = mult * self.total_capacities[1]
        if consist_weight > 63:
            utils.echo_message("Error: consist weight is " + str(consist_weight) + "t for " + self.id + "; must be < 63t")
        return min(consist_weight, 63)

    @property
    def tractive_effort_coefficient(self):
        # vehicles cannot set their own TE coefficients, shouldn't be needed
        # vehicle classes can do it by over-riding this property in their class
        if self.roadveh_flag_tram:
            # for trams, reduced TE compared to rubber-tyred vehicles
            return 0.3
        else:
            # for RVs TE is dibbled up substantially higher than the default 0.3 because RV performance sucks otherwise
            return 0.7

    @property
    def total_capacities(self):
        # total capacity of consist, summed from vehicles (with variants for capacity multipler param)
        # convenience function used only when the total consist capacity is needed rather than per-unit
        result = []
        for i in range(3):
            consist_capacity = 0
            for unit in self.units:
                # possibly fragile assumption that mail vehicles will always have to put mail first in default cargo list
                if self.default_cargos[0] == 'MAIL':
                    consist_capacity += int(global_constants.mail_multiplier * unit.capacities[i])
                else:
                    consist_capacity += unit.capacities[i]
            result.append(consist_capacity)
        return result

    @property
    def refittable_classes(self):
        cargo_classes = []
        # maps lists of allowed classes.  No equivalent for disallowed classes, that's overly restrictive and damages the viability of class-based refitting
        for i in self.class_refit_groups:
            [cargo_classes.append(cargo_class) for cargo_class in global_constants.base_refits_by_class[i]]
        return ','.join(set(cargo_classes)) # use set() here to dedupe

    def get_label_refits_allowed(self):
        # allowed labels, for fine-grained control in addition to classes
        return ','.join(self.label_refits_allowed)

    def get_label_refits_disallowed(self):
        # disallowed labels, for fine-grained control, knocking out cargos that are allowed by classes, but don't fit for gameplay reasons
        return ','.join(self.label_refits_disallowed)

    @property
    def speed(self):
        if self._speed is None:
            if self.roadveh_flag_tram is True:
                speeds = self.roster.default_tram_speeds
            else:
                speeds = self.roster.default_truck_speeds
            speed = speeds[max([year for year in speeds if self.intro_date >= year])]
            return speed
        else:
            return self._speed

    @property
    def power(self):
        # only trucks have standard power bands, trams are custom
        if self._power is None:
            if self.roadveh_flag_tram is True:
                power_bands = self.roster.default_tram_power_bands
            else:
                power_bands = self.roster.default_truck_power_bands
            power = power_bands[max([year for year in power_bands if self.intro_date >= year])]
            return power
        else:
            return self._power

    @property
    def adjusted_model_life(self):
        similar_consists = []
        for consist in self.roster.consists:
            if type(consist) == type(self):
                if consist.roadveh_flag_tram == self.roadveh_flag_tram:
                    # !! this will need to account for roadtypes ^^
                    utils.echo_message("adjusted_model_life will need to account for roadtype, not just tram flag")
                    similar_consists.append(consist)
        replacement_consist = None
        for consist in sorted(similar_consists, key=lambda consist: consist.intro_date):
            if consist.intro_date > self.intro_date:
                replacement_consist = consist
                break
        if replacement_consist is None:
            return 'VEHICLE_NEVER_EXPIRES'
        else:
            return replacement_consist.intro_date - self.intro_date

    @property
    def retire_early(self):
        # affects when vehicle is removed from buy menu (in combination with model life)
        # to understand why this is needed see https://newgrf-specs.tt-wiki.net/wiki/NML:Vehicles#Engine_life_cycle
        return -10 # retire at end of model life + 10 (fudge factor - no need to be more precise than that)


    @property
    def sound_effect(self):
        # allow custom sound effects (set per subclass or vehicle)
        if self._sound_effect:
            return self._sound_effect
        # is this vehicle steam? (relies on visual effect being set correctly)
        for unit in self.units:
            if len(unit.effects) > 0:
                if 'STEAM' in unit.effects[0]:
                    return 'SOUND_FACTORY_WHISTLE'
        # otherwise
        if self.roadveh_flag_tram:
            return 'SOUND_CAR_HORN'
        else:
            # possibly fragile assumption that pax vehicles will put PASS first in default cargos list
            if self.default_cargos[0] == 'PASS':
                return 'SOUND_BUS_START_PULL_AWAY'
            else:
                return 'SOUND_TRUCK_START_2'

    @property
    def buy_menu_width (self):
        # max sensible width in buy menu is 64px, but RH templates currently drawn at 36px - legacy stuff
        consist_length = 4 * sum([unit.vehicle_length for unit in self.units])
        #print(self.id, consist_length)
        if consist_length < global_constants.buy_menu_sprite_width:
            return consist_length
        else:
            return global_constants.buy_menu_sprite_width

    @property
    def roster(self):
        for roster in registered_rosters:
            if roster.id == self.roster_id:
                return roster

    def get_expression_for_roster(self):
        # the working definition is one and only one roster per vehicle
        roster = self.roster
        return 'param[1]==' + str(roster.numeric_id - 1)

    def get_nml_expression_for_default_cargos(self):
        # sometimes first default cargo is not available, so we use a list
        # this avoids unwanted cases like box cars defaulting to mail when goods cargo not available
        # if there is only one default cargo, the list just has one entry, that's no problem
        if len(self.default_cargos) == 1:
            return self.default_cargos[0]
        else:
            # build stacked ternary operators for cargos
            result = self.default_cargos[-1]
            for cargo in reversed(self.default_cargos[0:-1]):
                result = 'cargotype_available("' + cargo + '")?' + cargo + ':' + result
            return result

    def render_articulated_switch(self):
        template = templates["add_articulated_parts.pynml"]
        nml_result = template(consist=self, global_constants=global_constants)
        return nml_result

    def render(self):
        # templating
        nml_result = ''
        nml_result = nml_result + self.render_articulated_switch()
        for unit in set(self.units):
            nml_result = nml_result + unit.render()
        return nml_result


class RoadVehicle(object):
    """Base class for all types of road vehicles"""
    def __init__(self, **kwargs):
        self.consist = kwargs.get('consist')

        # setup properties for this road vehicle
        self.numeric_id = kwargs.get('numeric_id', None)
        self.vehicle_length = kwargs.get('vehicle_length', None)
        self.semi_truck_shift_offset_jank = kwargs.get('semi_truck_shift_offset_jank', None)
        # capacities variable by parameter
        self.capacities = self.get_capacity_variations(kwargs.get('capacity', 0))
        # optional - some consists have sequences like A1-B-A2, where A1 and A2 look the same but have different IDs for implementation reasons
        # avoid duplicating sprites on the spritesheet by forcing A2 to use A1's spriterow_num, fiddly eh?
        # ugly, but eh.  Zero-indexed, based on position in units[]
        # watch out for repeated vehicles in the consist when calculating the value for this)
        # !! I don't really like this solution, might be better to have the graphics processor duplicate this?, with a simple map of [source:duplicate_to]
        self.unit_num_providing_spriterow_num = kwargs.get('unit_num_providing_spriterow_num', None)
        # optional - force always using same spriterow
        # for cases where the template handles cargo, but some units in the consist might not show cargo, e.g. tractor units etc
        # can also be used to suppress compile failures during testing when spritesheet is unfinished (missing rows etc)
        self.always_use_same_spriterow = kwargs.get('always_use_same_spriterow', False)
        # only set if the graphics processor requires it to generate cargo sprites
        # defines the size of cargo sprite to use
        # if the vehicle cargo area is not an OTTD unit length, use the next size up and the masking will sort it out
        # some longer vehicles may place multiple shorter cargo sprites, e.g. 7/8 vehicle, 2 * 4/8 cargo sprites (with some overlapping)
        self.cargo_length = kwargs.get('cargo_length', None)
        self._effect_spawn_model = kwargs.get('effect_spawn_model', None)
        self.effects = kwargs.get('effects', []) # default for effects is an empty list

    def get_capacity_variations(self, capacity):
        # capacity is variable, controlled by a newgrf parameter
        # we cache the available variations on the vehicle instead of working them out every time - easier
        # allow that integer maths is needed for newgrf cb results; round up for safety
        return [int(math.ceil(capacity * multiplier)) for multiplier in global_constants.capacity_multipliers]

    def get_loading_speed(self, cargo_type, capacity_param):
        # ottd vehicles load at different rates depending on type,
        # normalise default loading time for this set to 240 ticks, regardless of capacity
        # openttd loading rates vary by transport type, look them up in wiki to find value to use here to normalise loading time to 240 ticks
        transport_type_rate = 12 # this is (240 / loading frequency in ticks for transport type) from wiki
        capacity = self.capacities[capacity_param]
        if cargo_type == 'mail':
            capacity = int(global_constants.mail_multiplier * capacity)
        result = int(self.consist.loading_speed_multiplier * math.ceil(capacity / transport_type_rate))
        return max(result, 1)

    @property
    def availability(self):
        # only show vehicle in buy menu if it is first vehicle in consist
        if self.is_lead_unit_of_consist:
            return "ALL_CLIMATES"
        else:
            return "NO_CLIMATE"

    @property
    def effect_spawn_model(self):
        if self._effect_spawn_model:
            return self._effect_spawn_model
        else:
            if self.consist.roadveh_flag_tram == True:
                # trams electric by default, over-ride in vehicle as needed
                return 'EFFECT_SPAWN_MODEL_ELECTRIC'
            else:
                # other vehicles diesel by default, over-ride in vehicle as needed
                return 'EFFECT_SPAWN_MODEL_DIESEL'

    @property
    def is_lead_unit_of_consist(self):
        # could be refactored - 'if self.consist.units.index(self.id) == 0:'
        if self.numeric_id == self.consist.base_numeric_id:
            return True
        else:
            return False

    @property
    def special_flags(self):
        special_flags = ['ROADVEH_FLAG_2CC']
        if self.consist.autorefit == True:
            special_flags.append('ROADVEH_FLAG_AUTOREFIT')
        if self.consist.roadveh_flag_tram == True:
            special_flags.append('ROADVEH_FLAG_TRAM')
        return ','.join(special_flags)

    @property
    def offsets(self):
        if self.semi_truck_shift_offset_jank:
            result = []
            for i in range (0, 8):
                base_offsets = global_constants.default_road_vehicle_offsets[str(self.vehicle_length)][i]
                offset_deltas = [self.semi_truck_shift_offset_jank * offset for offset in global_constants.semi_truck_offset_jank[i]]
                result.append([base_offsets[0] + offset_deltas[0], base_offsets[1] + offset_deltas[1]])
            return result
        else:
            return global_constants.default_road_vehicle_offsets[str(self.vehicle_length)]

    @property
    def spriterow_num(self):
        # ugly forcing of over-ride for out-of-sequence repeating vehicles
        if self.unit_num_providing_spriterow_num is not None:
            return self.unit_num_providing_spriterow_num

        preceding_spriterows = self.consist.get_spriterows_for_consist_or_subpart(self.consist.units[0:self.consist.units.index(self)])
        result = []
        for unit_rows in preceding_spriterows:
            result.append(sum([unit_row[1] for unit_row in unit_rows]))
        return sum(result)

    @property
    def vehicle_nml_template(self):
        if not self.always_use_same_spriterow:
            if self.consist.gestalt_graphics.nml_template:
                return self.consist.gestalt_graphics.nml_template
        # default case
        return 'vehicle_default.pynml'

    def get_cargo_suffix(self):
        return 'string(' + self.cargo_units_refit_menu + ')'

    def assert_cargo_labels(self, cargo_labels):
        for i in cargo_labels:
            if i not in global_constants.cargo_labels:
                utils.echo_message("Warning: vehicle " + self.id + " references cargo label " + i + " which is not defined in the cargo table")

    def get_expression_for_effects(self):
        # provides part of nml switch for effects (smoke), or none if no effects defined
        if len(self.effects) > 0:
            result = []
            for index, effect in enumerate(self.effects):
                 result.append('STORE_TEMP(create_effect(' + effect + '), 0x10' + str(index) + ')')
            return '[' + ','.join(result) + ']'
        else:
            return 0

    def get_nml_expression_for_cargo_variant_random_switch(self, cargo_id=None):
        switch_id = self.id + "_switch_graphics" + ('_' + str(cargo_id) if cargo_id is not None else '')
        return "SELF," + switch_id + ", bitmask(TRIGGER_VEHICLE_ANY_LOAD)"

    def render(self):
        # integrity tests
        self.assert_cargo_labels(self.consist.label_refits_allowed)
        self.assert_cargo_labels(self.consist.label_refits_disallowed)
        # templating
        template_name = self.vehicle_nml_template
        template = templates[template_name]
        nml_result = template(vehicle=self, consist=self.consist, global_constants=global_constants)
        return nml_result


class BoxHauler(Consist):
    """
    Box tram or truck - refits express, piece goods cargos, other selected cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['packaged_freight']
        self.label_refits_allowed = ['MAIL', 'GRAI', 'WHEA', 'MAIZ', 'FRUT', 'BEAN', 'NITR'] # Iron Horse compatibility
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_freight_special_cases']
        self.default_cargos = global_constants.default_cargos['box']
        self.weight_multiplier = 0.45


class CoveredHopperHauler(Consist):
    """
    Covered hopper truck or tram for bulk powder cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['covered_hopper_freight']
        self.label_refits_allowed = ['GRAI', 'WHEA', 'MAIZ', 'SUGR', 'FMSP', 'RFPR', 'CLAY', 'BDMT', 'BEAN', 'NITR', 'RUBR', 'SAND', 'POTA', 'QLME', 'SASH', 'CMNT', 'KAOL', 'FERT', 'SALT']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['covered_hopper']
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45


class DumpHauler(Consist):
    """
    Tram or truck for limited set of bulk (mineral) cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['dump_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_dump_bulk']
        self.default_cargos = global_constants.default_cargos['dump']
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsVisibleCargo(bulk=True)


class EdiblesTanker(Consist):
    """
    Wine, milk, water etc.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        self.label_refits_allowed = ['MILK', 'FOOD']
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_edible_liquids']
        self.default_cargos = global_constants.default_cargos['edibles_tank']
        self.loading_speed_multiplier = 2
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.5


class FlatHauler(Consist):
    """
    Flatbed tram or truck - refits most cargos, not bulk.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['flatbed_freight']
        self.label_refits_allowed = ['GOOD']
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_flatbed_freight']
        self.default_cargos = global_constants.default_cargos['flat']
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsVisibleCargo(piece='flat')


class FruitVegHauler(Consist):
    """
    Fruit and vegetables truck or tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['FRUT', 'BEAN', 'CASS', 'JAVA', 'NUTS']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['fruit_veg']
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.45


class IntermodalHauler(Consist):
    """
    Specialist intermodal (container) truck, limited range of cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        # maintain other sets (e.g. IH etc) when changing container refits
        self.class_refit_groups = ['express_freight','packaged_freight']
        self.label_refits_allowed = ['FRUT','WATR']
        self.label_refits_disallowed = ['FISH','LVST','OIL_','TOUR','WOOD']
        self.default_cargos = global_constants.default_cargos['intermodal']
        self.loading_speed_multiplier = 2


class LivestockHauler(Consist):
    """
    Livestock truck or tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['LVST']
        self.label_refits_disallowed = []
        self.default_cargos = ['LVST'] # no need for fallbacks, only one cargo
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.45


class LogHauler(Consist):
    """
    Gets wood.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['WOOD']
        self.label_refits_disallowed = []
        self.default_cargos = ['WOOD'] # no need for fallbacks, only one cargo
        self.loading_speed_multiplier = 2
        # Cargo graphics
        self.gestalt_graphics = GestaltGraphicsCustom({'WOOD': [0]},
                                                'vehicle_with_visible_cargo.pynml',
                                                generic_rows = [0])


class MailHauler(Consist):
    """
    Truck or tram for mail, valuables etc.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['mail', 'express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = ['TOUR']
        self.default_cargos = global_constants.default_cargos['mail']
        self.weight_multiplier = 0.2


class MetalHauler(Consist):
    """
    Specialist heavy haul tram / truck, e.g. multiwheel platform, steel mill hauler etc.
    High capacity, not very fast, refits to small subset of finished metal cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['STEL', 'COPR', 'IRON', 'SLAG']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['metal']
        self.loading_speed_multiplier = 2


class OpenHauler(Consist):
    """
    General cargo tram or truck - refits everything except mail, pax.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['all_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = ['TOUR']
        self.default_cargos = global_constants.default_cargos['open']
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsVisibleCargo(bulk=True,
                                                            piece='open')


class PaxHaulerBase(Consist):
    """
    Common base class for pax vehicles.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['pax']
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['pax']


class PaxHauler(PaxHaulerBase):
    """
    Bus or tram for pax.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading_speed_multiplier = 3
        self.weight_multiplier = 0.17


class PaxExpressHauler(PaxHaulerBase):
    """
    Coach or express tram for pax.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.2


class RefrigeratedHauler(Consist):
    """
    Refrigerated truck or tram.
    Refits to limited range of refrigerated cargos, with 'improved' cargo decay rate.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['refrigerated_freight']
        self.label_refits_allowed = [] # no specific labels needed, refits all cargos that have refrigerated class
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['reefer']
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.5


class SuppliesHauler(Consist):
    """
    Specialist tram / truck with flatbed + crane, supplies and building materials.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['ENSP', 'FMSP', 'VEHI', 'BDMT']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['supplies']
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.5
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsCustom({'ENSP': [0], 'FMSP': [0], 'VEHI': [0]},
                                                       'vehicle_with_visible_cargo.pynml',
                                                       generic_rows = [0])


class Tanker(Consist):
    """
    Ronseal ("does what it says on the tin", for those without extensive knowledge of UK advertising).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # tankers are unrealistically autorefittable, and at no cost
        # Pikka: if people complain that it's unrealistic, tell them "don't do it then"
        # they also change livery at stations if refitted between certain cargo types <shrug>
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        self.label_refits_allowed = []
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['edible_liquids']
        self.default_cargos = global_constants.default_cargos['tank']
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsLiveryOnly(recolour_maps=graphics_constants.tanker_livery_recolour_maps)


