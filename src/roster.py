from rosters import registered_rosters

def register(roster):
    registered_rosters.append(roster)


class Roster(object):
    """
    Rosters compose a set of vehicles which is complete for gameplay.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.buy_menu_sort_order = kwargs.get('buy_menu_sort_order')
        # default speeds, determined by intro date; can be over-ridden per vehicle when needed
        self.default_truck_speeds = kwargs.get('truck_speeds')
        self.default_tram_speeds = kwargs.get('tram_speeds')
        register(self)

