from road_vehicle import DumpFeldbahnConsist, ElectricRoadVehicle
from base_platforms.feldbahn import OpenWagonFeldbahnGen3

consist = DumpFeldbahnConsist(id='hake_lake_dump',
                       base_numeric_id=620,
                       name='Hake Lake',
                       vehicle_life=40,
                       gen=3)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=0,
                 chassis='feldbahn_1_16px',
                 always_use_same_spriterow=True)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=7)
